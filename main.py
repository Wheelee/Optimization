"""Point d'entrée du problème 1 : lancer ce fichier avec le bouton ▶ de l'IDE."""

from pathlib import Path

from scripts.view_instance import print_instance
from src.model_constraints import add_model_constraints
from src.model_setup import prepare_model_data
from src.model_variables import build_gurobi_model, variable_counts


PROJECT_ROOT = Path(__file__).resolve().parent

# Modifier ce nom pour utiliser une autre instance du dossier data/instances/mcd.
INSTANCE_NAME = "mcd-10-1-3-5-1-1.dat"
SECURITY_STOCK = 0.0
MAX_ROUTES_PER_VEHICLE = 1


def main() -> None:
    """Construit le modèle de l'instance configurée et affiche sa structure.

    Enchaîne le chargement des données, la création des variables et l'ajout
    des contraintes. Affiche leurs nombres par famille, puis libère le modèle,
    même en cas d'erreur après sa création. L'objectif et la résolution seront
    ajoutés dans une prochaine étape.
    """
    # ÉTAPE 1 — Données nécessaires aux contraintes : demandes, stocks initiaux,
    # capacités, ensembles d'indices, stock de sécurité et tournées possibles.
    instance_path = PROJECT_ROOT / "data/instances/mcd" / INSTANCE_NAME
    data = prepare_model_data(
        instance_path,
        security_stock=SECURITY_STOCK,
        max_routes_per_vehicle=MAX_ROUTES_PER_VEHICLE,
    )
    print_instance(instance_path)

    print("\nÉtape 1 - préparation des données terminée")
    print(f"Lieux : {data.locations}")
    print(f"Stations : {data.stations}")
    print(f"Produits : {data.products}")
    print(f"Camions : {data.vehicles}")
    print(f"Périodes : {data.periods}")
    print(f"Compartiments : {data.compartments}")
    print(f"Tournées : {data.routes}")
    print(f"Nombre d'arcs orientés : {len(data.arcs)}")
    print(f"Stock de sécurité utilisé : {SECURITY_STOCK}")

    # ÉTAPE 2 — Création des variables et de leurs domaines (section 6.5 du PDF).
    # Cet appel implémente aussi certaines bornes des contraintes :
    # (3) I <= capacité de cuve et (6) q >= 0, dans model_variables.py.
    model, variables = build_gurobi_model(data)
    try:
        print("\nÉtape 2 - variables Gurobi déclarées")
        for name, count in variable_counts(variables).items():
            print(f"{name:20s}: {count}")
        print(f"Variables Gurobi dans le modèle : {model.NumVars}")
        # ÉTAPE 3 — Ajout des contraintes (2) à (14) de « optimisation (2).pdf ».
        # L'appel ci-dessous exécute leur implémentation dans model_constraints.py :
        #   (2)-(4)   : bilan, limites de stock et capacité avant consommation ;
        #   (5)-(7)   : affectation des compartiments et lien livraison/visite ;
        #   (8)-(9)   : départ et retour au dépôt ;
        #   (10)-(12) : entrée/sortie des stations et activation des visites ;
        #   (13)-(14) : bornes d'ordre MTZ et élimination des sous-tours.
        # La borne supérieure de (3) a déjà été posée à l'étape 2.
        counts = add_model_constraints(model, data, variables)

        # Affichage du nombre de contraintes ajoutées par famille :
        # cette partie décrit le modèle construit, sans ajouter de contraintes.
        print("\nÉtape 3 - contraintes Gurobi ajoutées")
        for name, count in counts.items():
            print(f"{name:26s}: {count}")
        print(f"Contraintes Gurobi dans le modèle : {model.NumConstrs}")
        print("\nExécution terminée. La fonction objectif reste à ajouter ; "
              "aucune optimisation n'a été lancée.")
    finally:
        model.dispose()


if __name__ == "__main__":
    main()
