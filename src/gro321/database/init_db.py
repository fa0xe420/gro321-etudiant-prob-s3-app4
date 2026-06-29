"""
Script d'initialisation de la base de données.

Charge le schéma de départ (clients et robots normalisés, table bons_travail
laissée comme preuve de concept) ainsi que ses données d'exemple.
"""

import sqlite3
from pathlib import Path


def init_database(schema_file, data_file=None, db_path="data/gro321.db"):
    """
    Initialise la base de données avec un schéma et des données optionnelles.

    Args:
        schema_file: Chemin vers le fichier SQL de schéma
        data_file: Chemin vers le fichier SQL de données (optionnel)
        db_path: Chemin vers le fichier de base de données
    """
    # Créer le répertoire data si nécessaire
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Supprimer la base existante si elle existe
    if db_path.exists():
        print(f"Suppression de l'ancienne base: {db_path}")
        db_path.unlink()

    print(f"Création de la base de données: {db_path}")

    # Connexion et création du schéma
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Exécuter le schéma
        print(f"Exécution du schéma: {schema_file}")
        with open(schema_file, "r", encoding="utf-8") as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)

        # Exécuter les données si fournies
        if data_file:
            print(f"Insertion des données: {data_file}")
            with open(data_file, "r", encoding="utf-8") as f:
                data_sql = f.read()
                cursor.executescript(data_sql)

        conn.commit()
        print("Base de données initialisée avec succès!")

    except Exception as e:
        print(f"Erreur lors de l'initialisation: {e}")
        conn.rollback()
        raise

    finally:
        conn.close()


def main():
    """
    Point d'entrée principal.
    Usage: init-db [--db CHEMIN] [--sans-donnees]
    """
    import argparse

    parser = argparse.ArgumentParser(description="Initialise la base de données GMAO")
    parser.add_argument(
        "--db",
        default="data/gro321.db",
        help="Chemin vers la base de données (défaut: data/gro321.db)",
    )
    parser.add_argument(
        "--sans-donnees",
        action="store_true",
        help="Ne pas insérer les données d'exemple",
    )

    args = parser.parse_args()

    # Le code de départ charge le schéma de départ et ses données d'exemple.
    base_path = Path(__file__).parent
    schema_file = base_path / "schema_depart.sql"
    data_file = base_path / "donnees_depart.sql"

    if args.sans_donnees:
        data_file = None

    print("Initialisation de la base (schéma de départ)...")
    init_database(schema_file, data_file, args.db)


if __name__ == "__main__":
    main()
