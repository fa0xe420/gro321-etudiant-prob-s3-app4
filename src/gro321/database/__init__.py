"""
Module database - Gestion de la base de données et opérations CRUD.
"""

from .connexion import DatabaseConnection, get_connection
from .crud_bons import (
    creer_bon_diagnostic,
    creer_bon_mise_a_jour,
    creer_bon_reparation,
    lire_bon,
    lister_bons,
    modifier_statut_bon,
    supprimer_bon,
)
from .crud_clients import (
    creer_client,
    lire_client,
    lister_clients,
    modifier_client,
    supprimer_client,
)
from .crud_robots import (
    creer_robot,
    lire_robot,
    lister_robots,
    modifier_robot,
    supprimer_robot,
)

__all__ = [
    "get_connection",
    "DatabaseConnection",
    "creer_bon_diagnostic",
    "creer_bon_mise_a_jour",
    "creer_bon_reparation",
    "lire_bon",
    "lister_bons",
    "modifier_statut_bon",
    "supprimer_bon",
    "creer_client",
    "lire_client",
    "lister_clients",
    "modifier_client",
    "supprimer_client",
    "creer_robot",
    "lire_robot",
    "lister_robots",
    "modifier_robot",
    "supprimer_robot",
]
