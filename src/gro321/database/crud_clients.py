"""
Module CRUD pour les clients.
Fournit les opérations Create, Read, Update, Delete pour les clients.
"""

from ..models import Client
from .connexion import get_connection


def creer_client(nom, contact, adresse, db_path="data/gro321.db"):
    """
    Crée un nouveau client dans la base de données.

    Args:
        nom: Nom de l'établissement
        contact: Numéro de téléphone
        adresse: Adresse complète
        db_path: Chemin vers la base de données

    Returns:
        ID du client créé
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO clients (nom, contact, adresse)
            VALUES (?, ?, ?)
        """,
            (nom, contact, adresse),
        )
        return cursor.lastrowid


def lire_client(client_id, db_path="data/gro321.db"):
    """
    Récupère un client par son ID.

    Args:
        client_id: Identifiant du client
        db_path: Chemin vers la base de données

    Returns:
        Objet Client ou None si non trouvé
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT client_id, nom, contact, adresse
            FROM clients
            WHERE client_id = ?
        """,
            (client_id,),
        )

        row = cursor.fetchone()
        if not row:
            return None

        return Client(
            client_id=row["client_id"],
            nom=row["nom"],
            contact=row["contact"],
            adresse=row["adresse"],
        )


def lister_clients(db_path="data/gro321.db"):
    """
    Liste tous les clients.

    Args:
        db_path: Chemin vers la base de données

    Returns:
        Liste d'objets Client
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT client_id, nom, contact, adresse
            FROM clients
            ORDER BY nom
        """)

        clients = []
        for row in cursor.fetchall():
            clients.append(
                Client(
                    client_id=row["client_id"],
                    nom=row["nom"],
                    contact=row["contact"],
                    adresse=row["adresse"],
                )
            )

        return clients


def modifier_client(
    client_id, nom=None, contact=None, adresse=None, db_path="data/gro321.db"
):
    """
    Modifie les informations d'un client.
    Seuls les paramètres non-None sont modifiés.

    Args:
        client_id: Identifiant du client
        nom: Nouveau nom (optionnel)
        contact: Nouveau contact (optionnel)
        adresse: Nouvelle adresse (optionnel)
        db_path: Chemin vers la base de données

    Returns:
        True si modifié, False sinon
    """
    updates = []
    params = []

    if nom is not None:
        updates.append("nom = ?")
        params.append(nom)

    if contact is not None:
        updates.append("contact = ?")
        params.append(contact)

    if adresse is not None:
        updates.append("adresse = ?")
        params.append(adresse)

    if not updates:
        return False

    params.append(client_id)

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE clients
            SET {", ".join(updates)}
            WHERE client_id = ?
        """,
            params,
        )

        return cursor.rowcount > 0


def supprimer_client(client_id, db_path="data/gro321.db"):
    """
    Supprime un client.
    ATTENTION: Cela supprimera aussi tous les robots et bons associés (CASCADE).

    Args:
        client_id: Identifiant du client
        db_path: Chemin vers la base de données

    Returns:
        True si supprimé, False sinon
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
        return cursor.rowcount > 0
