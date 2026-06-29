"""
Module models - Classes représentant les entités du système de gestion.
"""

from .bon_travail import BonTravail
from .bon_diagnostic import BonDiagnostic
from .bon_mise_a_jour import BonMiseAJour
from .bon_reparation import BonReparation
from .client import Client
from .robot import Robot

__all__ = [
    "Client",
    "Robot",
    "BonTravail",
    "BonDiagnostic",
    "BonMiseAJour",
    "BonReparation",
]
