"""Point d'entrée du problème 1 : lancer ce fichier avec le bouton ▶ de l'IDE."""

from pathlib import Path

from scripts.view_instance import print_instance
from src.model_setup import prepare_model_data
from src.model_variables import build_gurobi_model, variable_counts


PROJECT_ROOT = Path(__file__).resolve().parent

# Modifier ce nom pour utiliser une autre instance du dossier data/instances/mcd.
INSTANCE_NAME = "mcd-10-1-3-5-1-1.dat"
SECURITY_STOCK = 0.0
MAX_ROUTES_PER_VEHICLE = 1


def main() -> None:
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

    model, variables = build_gurobi_model(data)
    try:
        print("\nÉtape 2 - variables Gurobi déclarées")
        for name, count in variable_counts(variables).items():
            print(f"{name:20s}: {count}")
        print(f"Variables Gurobi dans le modèle : {model.NumVars}")
        print("\nExécution terminée. Les contraintes et l'objectif restent à ajouter ; "
              "aucune optimisation n'a été lancée.")
    finally:
        model.dispose()


if __name__ == "__main__":
    main()
