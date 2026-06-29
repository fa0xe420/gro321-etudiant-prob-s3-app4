"""
Module de gestion de la connexion à la base de données SQLite.
"""

import sqlite3
from pathlib import Path


class DatabaseConnection:
    """
    Gestionnaire de connexion à la base de données.
    Utilise le patron « gestionnaire de contexte » (with) pour gérer
    automatiquement la connexion.

    Au laboratoire, la plomberie était écrite à la main: on appelait
    get_connection(), on exécutait nos requêtes, on faisait commit() puis
    close() dans un bloc try/finally. Cette classe encapsule exactement cette
    plomberie. À l'entrée du bloc with, elle ouvre la connexion; à la sortie,
    elle fait automatiquement commit() si tout s'est bien passé, rollback() en
    cas d'exception, puis close() dans tous les cas. On écrit donc seulement les
    requêtes; l'ouverture, la validation et la fermeture sont prises en charge.
    """

    def __init__(self, db_path="data/gro321.db"):
        """
        Initialise la connexion à la base de données.

        Args:
            db_path: Chemin vers le fichier de base de données
        """
        self.db_path = Path(db_path)
        self.conn = None

    def __enter__(self):
        """Entre dans le contexte et retourne la connexion."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sort du contexte et ferme la connexion."""
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
        return False


def get_connection(db_path="data/gro321.db"):
    """
    Retourne un gestionnaire de connexion à la base de données.

    Args:
        db_path: Chemin vers le fichier de base de données

    Returns:
        DatabaseConnection instance

    Exemple:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients")
    """
    return DatabaseConnection(db_path)
