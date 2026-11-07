"""Affichage rapide d'une instance exemple.

Lancement :
    python3 view_instance.py

Pour changer d'instance, modifier DEFAULT_INSTANCE ci-dessous.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.instance_loader import load_instance


DEFAULT_INSTANCE = PROJECT_ROOT / "data/instances/mcd/mcd-10-1-3-5-1-1.dat"


def print_instance(path: Path) -> None:
    data = load_instance(path, option=0)

    print("=" * 70)
    print("INSTANCE DE RÉAPPROVISIONNEMENT")
    print("=" * 70)
    print(f"Fichier       : {path.name}")
    print(f"Stations      : {data.n}")
    print(f"Produits      : {data.m}")
    print(f"Compartiments : {data.comps}")
    print(f"Véhicules     : {data.k}")
    print(f"Périodes      : {data.h}")

    print("\nCAPACITÉS DES COMPARTIMENTS")
    for vehicle in range(1, data.k + 1):
        capacities = data.compartment_sizes[vehicle][1:]
        print(f"  Camion {vehicle}: {capacities}")

    print("\nSTATIONS")
    for station in range(1, data.n + 1):
        print(f"\n  Station {station}")
        print(f"    Coordonnées : {data.coordinates[station]}")
        print(f"    Distance dépôt : {data.distances[0][station]}")
        for product in range(1, data.m + 1):
            inventory = data.initial_inventory[station][product]
            capacity = data.tank_capacity[station][product]
            cost = data.holding_cost[station][product]
            demands = data.demand[station][product][1:data.h + 1]
            print(f"    Produit {product}:")
            print(f"      Stock initial : {inventory}")
            print(f"      Demandes      : {demands}")
            print(f"      Capacité cuve : {capacity}")
            print(f"      Coût stockage : {cost}")

    print("\nMATRICE DES DISTANCES")
    print("     " + " ".join(f"{j:4}" for j in range(data.n + 1)))
    for i, row in enumerate(data.distances):
        print(f"{i:3}  " + " ".join(f"{distance:4}" for distance in row))


if __name__ == "__main__":
    if not DEFAULT_INSTANCE.exists():
        raise FileNotFoundError(
            f"Instance exemple introuvable : {DEFAULT_INSTANCE}\n"
            "Modifie DEFAULT_INSTANCE dans view_instance.py."
        )
    print_instance(DEFAULT_INSTANCE)
