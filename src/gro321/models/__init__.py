"""
Module models - Classes représentant les entités du système de gestion.
"""

from .bon_travail import BonTravail, BonDiagnostic, BonMiseAJour, BonReparation
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
