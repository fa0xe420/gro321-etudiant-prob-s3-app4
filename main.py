"""
Point d'entrée de démonstration pour le projet GRO321.

Les commandes utiles du projet sont exposées via uv:
  - uv run init-db        : initialise la base de données
  - uv run gro321-server  : démarre le serveur web
"""

from gro321 import database
from gro321 import models

def main():
    print("Projet GRO321 - Système de gestion de maintenance (GMAO)")
    print("Initialiser la base : uv run init-db")
    print("Démarrer le serveur : uv run gro321-server")

    # les tests
    print("===============SECTION TEST===============")
    # creer_bon_diagnostic
    nouveau_diagnostic = database.creer_bon_diagnostic('SN-2026-DIAG', 'symptomes_testing', 'diagnostic_testing')
    assert nouveau_diagnostic is not None, "creer_bon_diagnostic devrait retrouner le bon_id"
    print(f"bon de diagnostic ajouté avec l'ID {nouveau_diagnostic}")

    # creer_bon_mise_a_jour
    nouveau_mise_a_jour = database.creer_bon_mise_a_jour('SN-2026-MISE', 'ver_act', 'ver_cib', '1')
    assert nouveau_mise_a_jour is not None, "creer_bon_mise_a_jour devrait retrouner le bon_id"
    print(f"bon de diagnostic ajouté avec l'ID {nouveau_mise_a_jour}")

    # creer_bon_reparation
    nouveau_reparation = database.creer_bon_reparation('SN-2026-REPA', 'composant_test', 'probleme_test', '{"pieces_utilisees": TEST}')
    assert nouveau_reparation is not None, "creer_bon_reparation devrait retrouner le bon_id"
    print(f"bon de diagnostic ajouté avec l'ID {nouveau_reparation}")

    # lire
    bon = database.lire_bon(nouveau_diagnostic)
    assert isinstance(bon, models.bon_diagnostic.BonDiagnostic), "lire_bon devrait reconstruire un BonDiagnostic"
    assert bon.symptomes == 'symptomes_testing', "symptomes devrait symptomes_testing"
    assert bon.diagnostic == 'diagnostic_testing', "diagnostic devrait diagnostic_testing"
    assert bon.type_bon == 'diagnostic', "type_bon devrait diagnostic"
    print(f"symptomes: {bon.symptomes}, diagnostic: {bon.diagnostic}, type de bon: {bon.type_bon}")

    # modifier
    assert database.modifier_statut_bon(nouveau_mise_a_jour, 'en_cours'), "modifier_statut_bon devrait retouner True"
    bon = database.lire_bon(nouveau_mise_a_jour)
    assert bon.statut == "en_cours"
    print(f"type de bon modifier: {bon.type_bon}")

    # supprimer
    assert database.supprimer_bon(nouveau_diagnostic), "supprimer_bon devrait retourner True"
    assert database.lire_bon(nouveau_diagnostic) is None, "BonReparation ne devrait plus exister"
    assert not database.supprimer_bon(nouveau_diagnostic), "Supprimer deux fois devrait retourner False"

    print("Tous les tests ont réussi!")

if __name__ == "__main__":
    main()
