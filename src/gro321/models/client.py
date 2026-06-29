"""
Module contenant la classe Client pour représenter un client du service.
"""


class Client:
    """
    Représente un client possédant des robots de service.
    """

    def __init__(self, client_id, nom, contact, adresse):
        """
        Initialise un nouveau client.

        Args:
            client_id: Identifiant unique du client
            nom: Nom de l'établissement
            contact: Numéro de téléphone de contact
            adresse: Adresse complète de l'établissement
        """
        self.client_id = client_id
        self.nom = nom
        self.contact = contact
        self.adresse = adresse

    def modifier_contact(self, nouveau_contact):
        """
        Modifie le numéro de contact du client.

        Args:
            nouveau_contact: Nouveau numéro de téléphone
        """
        self.contact = nouveau_contact

    def modifier_adresse(self, nouvelle_adresse):
        """
        Modifie l'adresse du client.

        Args:
            nouvelle_adresse: Nouvelle adresse complète
        """
        self.adresse = nouvelle_adresse

    def __str__(self):
        """Retourne une représentation textuelle du client."""
        return f"Client {self.client_id}: {self.nom} - {self.contact}"

    def __repr__(self):
        """Retourne une représentation technique du client."""
        return f"Client(id={self.client_id}, nom='{self.nom}')"
