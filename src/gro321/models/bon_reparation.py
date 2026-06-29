from .bon_travail import BonTravail

class BonReparation(BonTravail):
    """
    Initialise Reparation enfant de bon de travail.

    Args ajoutés:
        composant: composant défaut
        probleme: le problème du composant
        piece_utilisees: pièce utilisées pour réparer le robot
    """   
    def __init__(self, composant, probleme, pieces_utilisees, bon_id, numero_serie, date_creation=None, statut="ouvert"):
        super().__init__(bon_id, numero_serie, date_creation, statut)

        self.composant = composant
        self.probleme = probleme
        self.pieces_utilisees = pieces_utilisees
        self.type_bon = "reparation"
    
    def obtenir_description(self):
        if self.pieces_utilisees is None:
            return f"Bon de réparation #{self.bon_id} pour le robot {self.numero_serie} - Composant concerné : {self.composant}. Problème décrit : {self.probleme}. Pièces utilisées non renseignées."
        else:
            return f"Bon de réparation #{self.bon_id} pour le robot {self.numero_serie} - Composant concerné : {self.composant}. Problème décrit : {self.probleme}. Pièces utilisées : {self.pieces_utilisees}."