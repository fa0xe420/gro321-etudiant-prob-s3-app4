"""
Module CRUD pour les robots.
Fournit les opérations Create, Read, Update, Delete pour les robots.
"""

from ..models import Robot
from .connexion import get_connection


def creer_robot(
    modele, numero_serie, client_id, statut="operationnel", db_path="data/gro321.db"
):
    """
    Crée un nouveau robot dans la base de données.

    Args:
        modele: Modele du robot
        numero_serie: Numero de serie unique
        client_id: Identifiant du client proprietaire
        statut: Statut opérationnel
        db_path: Chemin vers la base de données

    Returns:
        ID du robot créé
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO robots (modele, numero_serie, client_id, statut)
            VALUES (?, ?, ?, ?)
        """,
            (modele, numero_serie, client_id, statut),
        )
        return cursor.lastrowid


def lire_robot(robot_id, db_path="data/gro321.db"):
    """
    Récupère un robot par son ID.

    Args:
        robot_id: Identifiant du robot
        db_path: Chemin vers la base de données

    Returns:
        Objet Robot ou None si non trouvé
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT robot_id, modele, numero_serie, client_id, statut
            FROM robots
            WHERE robot_id = ?
        """,
            (robot_id,),
        )

        row = cursor.fetchone()
        if not row:
            return None

        return Robot(
            robot_id=row["robot_id"],
            modele=row["modele"],
            numero_serie=row["numero_serie"],
            client_id=row["client_id"],
            statut=row["statut"],
        )


def lister_robots(client_id=None, statut=None, db_path="data/gro321.db"):
    """
    Liste les robots avec filtres optionnels.

    Args:
        client_id: Filtre par client (optionnel)
        statut: Filtre par statut (optionnel)
        db_path: Chemin vers la base de données

    Returns:
        Liste d'objets Robot
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()

        query = "SELECT robot_id, modele, numero_serie, client_id, statut FROM robots WHERE 1=1"
        params = []

        if client_id is not None:
            query += " AND client_id = ?"
            params.append(client_id)

        if statut is not None:
            query += " AND statut = ?"
            params.append(statut)

        query += " ORDER BY robot_id"

        cursor.execute(query, params)

        robots = []
        for row in cursor.fetchall():
            robots.append(
                Robot(
                    robot_id=row["robot_id"],
                    modele=row["modele"],
                    numero_serie=row["numero_serie"],
                    client_id=row["client_id"],
                    statut=row["statut"],
                )
            )

        return robots


def modifier_robot(
    robot_id, modele=None, statut=None, client_id=None, db_path="data/gro321.db"
):
    """
    Modifie les informations d'un robot.
    Seuls les parametres non-None sont modifiés.

    Args:
        robot_id: Identifiant du robot
        modele: Nouveau modele (optionnel)
        statut: Nouveau statut (optionnel)
        client_id: Nouveau client (optionnel)
        db_path: Chemin vers la base de données

    Returns:
        True si modifié, False sinon
    """
    updates = []
    params = []

    if modele is not None:
        updates.append("modele = ?")
        params.append(modele)

    if statut is not None:
        statuts_valides = ["operationnel", "en_maintenance", "hors_service"]
        if statut not in statuts_valides:
            raise ValueError(f"Statut invalide: {statut}")
        updates.append("statut = ?")
        params.append(statut)

    if client_id is not None:
        updates.append("client_id = ?")
        params.append(client_id)

    if not updates:
        return False

    params.append(robot_id)

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE robots
            SET {", ".join(updates)}
            WHERE robot_id = ?
        """,
            params,
        )

        return cursor.rowcount > 0


def supprimer_robot(robot_id, db_path="data/gro321.db"):
    """
    Supprime un robot.
    ATTENTION: Cela supprimera aussi tous les bons de travail associés (CASCADE).

    Args:
        robot_id: Identifiant du robot
        db_path: Chemin vers la base de données

    Returns:
        True si supprimé, False sinon
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM robots WHERE robot_id = ?", (robot_id,))
        return cursor.rowcount > 0
