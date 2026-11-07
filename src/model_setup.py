"""Préparation des ensembles et paramètres du modèle MILP.

Cette étape ne crée encore aucune variable de décision. Elle vérifie l'instance
et construit les ensembles utilisés par la formulation mathématique.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.instance_loader import Instance, load_instance


# Hypothèses à confirmer avec l'énoncé du projet.
SECURITY_STOCK = 0.0
MAX_ROUTES_PER_VEHICLE = 1


@dataclass
class ModelData:
    """Rassemble l'instance, les ensembles d'indices et les stocks de sécurité.

    compartments et routes donnent les indices disponibles pour chaque camion.
    arcs contient les déplacements orientés entre lieux distincts, dépôt inclus.
    Ces données servent à créer les variables puis les contraintes Gurobi.
    """
    instance: Instance
    locations: List[int]
    stations: List[int]
    products: List[int]
    vehicles: List[int]
    periods: List[int]
    compartments: Dict[int, List[int]]
    routes: Dict[int, List[int]]
    arcs: List[Tuple[int, int]]
    security_stock: Dict[Tuple[int, int], float]


def validate_instance(instance: Instance) -> None:
    """Vérifie les dimensions principales, stocks, demandes et capacités.

    Lève ValueError si un contrôle échoue (par exemple un stock initial supérieur
    à la capacité de cuve). Ces contrôles ne garantissent pas la faisabilité
    globale des livraisons, qui sera déterminée par le solveur.
    """
    if instance.n < 1:
        raise ValueError("L'instance doit contenir au moins une station")
    if instance.m < 1 or instance.k < 1 or instance.h < 1:
        raise ValueError("Produits, camions et périodes doivent être positifs")

    for station in range(1, instance.n + 1):
        for product in range(1, instance.m + 1):
            initial = instance.initial_inventory[station][product]
            capacity = instance.tank_capacity[station][product]
            if initial < 0:
                raise ValueError(f"Stock initial négatif : station {station}, produit {product}")
            if capacity <= 0:
                raise ValueError(f"Capacité de cuve invalide : station {station}, produit {product}")
            if initial > capacity:
                raise ValueError(
                    f"Stock initial supérieur à la cuve : station {station}, produit {product}"
                )
            for period in range(1, instance.h + 1):
                if instance.demand[station][product][period] < 0:
                    raise ValueError(
                        f"Demande négative : station {station}, produit {product}, période {period}"
                    )

    for vehicle in range(1, instance.k + 1):
        for compartment in range(1, instance.comps + 1):
            if instance.compartment_sizes[vehicle][compartment] <= 0:
                raise ValueError(
                    f"Capacité de compartiment invalide : camion {vehicle}, "
                    f"compartiment {compartment}"
                )


def prepare_model_data(
    instance_path: str | Path,
    security_stock: float = SECURITY_STOCK,
    max_routes_per_vehicle: int = MAX_ROUTES_PER_VEHICLE,
) -> ModelData:
    """Charge et valide l'instance, puis renvoie les données du modèle dans ModelData.

    Conserve l'ordre des stations du fichier, construit les arcs sans boucles
    et attribue à chaque camion max_routes_per_vehicle tournées possibles par
    période. security_stock s'applique à tous les couples station-produit :
    il doit être positif ou nul et ne pas dépasser leur stock initial.
    Aucune variable ni contrainte Gurobi n'est créée à cette étape.
    """
    if security_stock < 0:
        raise ValueError("Le stock de sécurité ne peut pas être négatif")
    if max_routes_per_vehicle < 1:
        raise ValueError("Le nombre maximal de tournées doit être positif")

    instance = load_instance(instance_path, option=0)
    validate_instance(instance)
    for station in range(1, instance.n + 1):
        for product in range(1, instance.m + 1):
            if security_stock > instance.initial_inventory[station][product]:
                raise ValueError(
                    f"Stock de sécurité supérieur au stock initial : "
                    f"station {station}, produit {product}"
                )

    locations = list(range(instance.n + 1))
    stations = list(range(1, instance.n + 1))
    products = list(range(1, instance.m + 1))
    vehicles = list(range(1, instance.k + 1))
    periods = list(range(1, instance.h + 1))
    compartments = {
        vehicle: list(range(1, instance.comps + 1))
        for vehicle in vehicles
    }
    routes = {
        vehicle: list(range(1, max_routes_per_vehicle + 1))
        for vehicle in vehicles
    }
    arcs = [(i, j) for i in locations for j in locations if i != j]
    security_stocks = {
        (station, product): security_stock
        for station in stations
        for product in products
    }

    return ModelData(
        instance=instance,
        locations=locations,
        stations=stations,
        products=products,
        vehicles=vehicles,
        periods=periods,
        compartments=compartments,
        routes=routes,
        arcs=arcs,
        security_stock=security_stocks,
    )


if __name__ == "__main__":
    example = PROJECT_ROOT / "data/instances/mcd/mcd-10-1-3-5-1-1.dat"
    data = prepare_model_data(example)
    print("Étape 1 - préparation des données terminée")
    print(f"Lieux : {data.locations}")
    print(f"Stations : {data.stations}")
    print(f"Produits : {data.products}")
    print(f"Camions : {data.vehicles}")
    print(f"Périodes : {data.periods}")
    print(f"Compartiments : {data.compartments}")
    print(f"Tournées : {data.routes}")
    print(f"Nombre d'arcs orientés : {len(data.arcs)}")
    print(f"Stock de sécurité utilisé : {SECURITY_STOCK}")
