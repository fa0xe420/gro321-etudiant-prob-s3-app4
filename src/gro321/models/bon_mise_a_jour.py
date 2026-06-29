from .bon_travail import BonTravail

class BonMiseAJour(BonTravail):
    """
    Initialise Mise a jour enfant de bon de travail.

    Args ajoutés:
        version_actuelle: version actuelle du robot
        version_cible: version cible du robot
        mise_a_jour_reussie: status de mise a jour
    """   
    def __init__(self, version_actuelle, version_cible, mise_a_jour_reussie, bon_id, numero_serie, date_creation=None, statut="ouvert"):
        super().__init__(bon_id, numero_serie, date_creation, statut)
        
        self.version_actuelle = version_actuelle
        self.version_cible = version_cible
        self.mise_a_jour_reussie = mise_a_jour_reussie
        self.type_bon = "mise_a_jour"

    def obtenir_description(self):
        if self.mise_a_jour_reussie is None:
            return f"Bon de mise à jour #{self.bon_id} pour le robot {self.numero_serie} - Passage de la version {self.version_actuelle} à {self.version_cible}. Mise à jour en cours."
        elif self.mise_a_jour_reussie == 1:
            return f"Bon de mise à jour #{self.bon_id} pour le robot {self.numero_serie} - Mise à jour réussie de la version {self.version_actuelle} à {self.version_cible}."
        else:
            return f"Bon de mise à jour #{self.bon_id} pour le robot {self.numero_serie} - Échec de la mise à jour de la version {self.version_actuelle} vers {self.version_cible}."