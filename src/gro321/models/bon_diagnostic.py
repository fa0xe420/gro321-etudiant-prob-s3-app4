from .bon_travail import BonTravail

class BonDiagnostic(BonTravail): 
    """
    Initialise Dianostic enfant de bon de travail.

    Args ajoutés:
        symptomes: symptomes du robot
        diagnostic: diagnostic pour le symptome
    """    
    def __init__(self, symptomes, diagnostic, bon_id, numero_serie, date_creation=None, statut="ouvert"):
        super().__init__(bon_id, numero_serie, date_creation, statut)
        self.symptomes = symptomes
        self.diagnostic = diagnostic
        self.type_bon = "diagnostic"

    def obtenir_description(self):
        if self.diagnostic is None:
            return f"Bon de diagnostic #{self.bon_id} pour le robot {self.numero_serie} - Symptômes rapportés : {self.symptomes}. Diagnostic en attente."
        else:
            return f"Bon de diagnostic #{self.bon_id} pour le robot {self.numero_serie} - Symptômes : {self.symptomes}. Diagnostic posé : {self.diagnostic}."