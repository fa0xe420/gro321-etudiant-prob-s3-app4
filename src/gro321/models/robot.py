"""
Module contenant la classe Robot pour représenter un robot de service.
"""


class Robot:
    """
    Représente un robot de service déployé chez un client.
    """

    def __init__(self, robot_id, modele, numero_serie, client_id, statut="operationnel"):
        """
        Initialise un nouveau robot.

        Args:
            robot_id: Identifiant unique du robot
            modele: Modèle du robot (ex: ServBot-2000)
            numero_serie: Numéro de série du fabricant
            client_id: Identifiant du client propriétaire
            statut: Statut opérationnel (operationnel, en_maintenance, hors_service)
        """
        self.robot_id = robot_id
        self.modele = modele
        self.numero_serie = numero_serie
        self.client_id = client_id
        self.statut = statut

    def changer_statut(self, nouveau_statut):
        """
        Modifie le statut opérationnel du robot.

        Args:
            nouveau_statut: Nouveau statut parmi (operationnel, en_maintenance,
                hors_service)
        """
        statuts_valides = ["operationnel", "en_maintenance", "hors_service"]
        if nouveau_statut not in statuts_valides:
            raise ValueError(f"Statut invalide. Doit être parmi: {statuts_valides}")
        self.statut = nouveau_statut

    def est_operationnel(self):
        """
        Vérifie si le robot est opérationnel.

        Returns:
            True si le robot est opérationnel, False sinon
        """
        return self.statut == "operationnel"

    def __str__(self):
        """Retourne une représentation textuelle du robot."""
        return f"Robot {self.robot_id}: {self.modele} ({self.numero_serie}) - {self.statut}"

    def __repr__(self):
        """Retourne une représentation technique du robot."""
        return f"Robot(id={self.robot_id}, modele='{self.modele}', statut='{self.statut}')"
