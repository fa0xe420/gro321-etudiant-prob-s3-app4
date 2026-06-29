"""
Module contenant la classe parente des bons de travail.

Objectif: Concevoir une hiérarchie de classes appropriée pour les bons de travail.

Vous pouvez vous inspirer des classes Client et Robot et de la classe Forme 
vue au laboratoire: la classe parente définit le contrat commun et lève
NotImplementedError pour les méthodes que les classes dérivées doivent
obligatoirement redéfinir (ici obtenir_description()).
"""

from datetime import datetime


class BonTravail:
    """
    Classe parente représentant un bon de travail générique.

    Cette classe regroupe les attributs et le comportement communs à tous les
    types de bons. Les classes dérivées (à créer) ajoutent les attributs
    spécifiques à chaque type et redéfinissent obtenir_description().

    Note: la table bons_travail étant une preuve de concept non normalisée, le
    robot est désigné par son numéro de série (numero_serie) et non par une
    clé étrangère.
    """

    STATUTS_VALIDES = ["ouvert", "en_cours", "termine", "annule"]

    def __init__(self, bon_id, numero_serie, date_creation=None, statut="ouvert"):
        """
        Initialise un bon de travail.

        Args:
            bon_id: Identifiant unique du bon
            numero_serie: Numéro de série du robot concerné
            date_creation: Date de création (datetime ou None pour maintenant)
            statut: Statut du bon (ouvert, en_cours, termine, annule)
        """
        self.bon_id = bon_id
        self.numero_serie = numero_serie
        self.date_creation = date_creation or datetime.now()
        self.statut = statut
        # self.type_bon = "generique"

    def changer_statut(self, nouveau_statut):
        """
        Modifie le statut du bon de travail.

        Args:
            nouveau_statut: Nouveau statut parmi STATUTS_VALIDES
        """
        if nouveau_statut not in self.STATUTS_VALIDES:
            raise ValueError(
                f"Statut invalide. Doit être parmi: {self.STATUTS_VALIDES}"
            )
        self.statut = nouveau_statut

    def est_termine(self):
        """
        Vérifie si le bon de travail est terminé.

        Returns:
            True si le bon est terminé, False sinon
        """
        return self.statut == "termine"

    def obtenir_description(self):
        """
        Retourne une description du bon de travail.

        Méthode à redéfinir obligatoirement dans chaque classe dérivée, à
        l'image de Forme.aire() vue au laboratoire.
        """
        raise NotImplementedError(
            "Les classes dérivées doivent redéfinir obtenir_description()."
        )

    def __str__(self):
        """Retourne une représentation textuelle du bon."""
        return (
            f"Bon {self.bon_id} ({self.type_bon}) - "
            f"Robot {self.numero_serie} - {self.statut}"
        )

    def __repr__(self):
        """Retourne une représentation technique du bon."""
        return (
            f"BonTravail(id={self.bon_id}, type='{self.type_bon}', "
            f"statut='{self.statut}')"
        )
    
