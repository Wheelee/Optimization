"""Lecture des instances MCD de réapprovisionnement en carburant."""

from dataclasses import dataclass
from math import hypot
from pathlib import Path
from typing import List, Tuple, Union


@dataclass
class Instance:
    """Regroupe les dimensions et tableaux lus dans une instance MCD.

    Le dépôt porte l'indice 0 ; stations, produits, camions, compartiments et
    périodes commencent à 1. station_order conserve les identifiants d'origine
    des stations après un éventuel réordonnancement.
    """
    n: int
    m: int
    comps: int
    k: int
    h: int
    coordinates: List[Tuple[int, int]]
    compartment_sizes: List[List[int]]
    initial_inventory: List[List[int]]
    demand: List[List[List[int]]]
    tank_capacity: List[List[int]]
    holding_cost: List[List[float]]
    safety_stock: List[List[int]]
    max_trips: int
    distances: List[List[int]]
    station_order: List[int]

    @property
    def vehicles(self) -> int:
        """Renvoie le nombre de camions (alias lisible du paramètre k)."""
        return self.k

    @property
    def periods(self) -> int:
        """Renvoie le nombre de périodes (alias lisible du paramètre h)."""
        return self.h


def _rounded_euclidean(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Calcule la distance euclidienne, arrondie à l'entier (0,5 vers le haut)."""
    return int(hypot(a[0] - b[0], a[1] - b[1]) + 0.5)


def _order_stations(instance: Instance, option: int) -> List[int]:
    """Renvoie les identifiants des stations dans l'ordre choisi, sans les modifier.

    Options : 0 = ordre du fichier ; 1 = demande totale décroissante ;
    2 = demande du produit 1 décroissante ; 3/4 = distance au dépôt
    croissante/décroissante. Une option inconnue déclenche ValueError.
    """
    stations = list(range(1, instance.n + 1))

    if option == 0:
        return stations

    if option == 1:
        return sorted(
            stations,
            key=lambda i: sum(
                instance.demand[i][p][t]
                for p in range(1, instance.m + 1)
                for t in range(1, instance.h + 1)
            ),
            reverse=True,
        )

    if option == 2:
        return sorted(
            stations,
            key=lambda i: sum(
                instance.demand[i][1][t]
                for t in range(1, instance.h + 1)
            ),
            reverse=True,
        )

    if option == 3:
        return sorted(
            stations,
            key=lambda i: instance.distances[0][i],
        )

    if option == 4:
        return sorted(
            stations,
            key=lambda i: instance.distances[0][i],
            reverse=True,
        )

    raise ValueError("option doit valoir 0, 1, 2, 3 ou 4")


def _reorder(instance: Instance, station_order: List[int]) -> Instance:
    """Crée une instance réindexée selon station_order en conservant le dépôt à 0.

    Réordonne les données des stations et les deux axes de la matrice des
    distances. Les caractéristiques des camions restent identiques.
    """
    order = [0] + station_order

    return Instance(
        n=instance.n,
        m=instance.m,
        comps=instance.comps,
        k=instance.k,
        h=instance.h,
        coordinates=[instance.coordinates[i] for i in order],
        compartment_sizes=instance.compartment_sizes,
        initial_inventory=[instance.initial_inventory[i][:] for i in order],
        demand=[[product[:] for product in instance.demand[i]] for i in order],
        tank_capacity=[instance.tank_capacity[i][:] for i in order],
        holding_cost=[instance.holding_cost[i][:] for i in order],
        safety_stock=[instance.safety_stock[i][:] for i in order],
        max_trips=instance.max_trips,
        distances=[
            [instance.distances[i][j] for j in order]
            for i in order
        ],
        station_order=station_order,
    )


def load_instance(
    path: Union[str, Path],
    option: int = 0,
    max_trips: int = 1,
) -> Instance:
    """Lit un fichier .dat MCD et renvoie une Instance prête à être exploitée.

    Lit les dimensions, le dépôt, les compartiments puis les stations ; calcule
    les distances et applique le tri demandé. Signale un fichier inaccessible,
    incomplet ou contenant des valeurs supplémentaires. La validation physique
    des données est effectuée séparément par validate_instance.

    Le stock de sécurité n'est pas fourni dans les fichiers du benchmark.
    Il est fixé à zéro afin de reproduire la configuration de référence.
    Pour le problème général, il peut être remplacé par des valeurs positives
    ou lu depuis un fichier d'instance complémentaire.
    """
    path = Path(path)

    try:
        tokens = path.read_text(encoding="utf-8").split()
    except OSError as exc:
        raise FileNotFoundError(f"Impossible d'ouvrir {path}") from exc

    cursor = 0

    def take_int() -> int:
        """Lit le prochain entier et avance le curseur ; signale une fin prématurée."""
        nonlocal cursor
        if cursor >= len(tokens):
            raise ValueError(
                f"Fichier incomplet à la position {cursor}"
            )
        value = int(tokens[cursor])
        cursor += 1
        return value

    def take_float() -> float:
        """Lit le prochain réel et avance le curseur ; signale une fin prématurée."""
        nonlocal cursor
        if cursor >= len(tokens):
            raise ValueError(
                f"Fichier incomplet à la position {cursor}"
            )
        value = float(tokens[cursor])
        cursor += 1
        return value

    n, m, comps, k, h = (take_int() for _ in range(5))

    coordinates = [(take_int(), take_int())]

    compartment_sizes = [[0] * (comps + 1) for _ in range(k + 1)]

    for vehicle in range(1, k + 1):
        for compartment in range(1, comps + 1):
            compartment_sizes[vehicle][compartment] = take_int()

    initial_inventory = [[0] * (m + 1) for _ in range(n + 1)]
    demand = [
        [[0] * (h + 2) for _ in range(m + 1)]
        for _ in range(n + 1)
    ]
    tank_capacity = [[0] * (m + 1) for _ in range(n + 1)]
    holding_cost = [[0.0] * (m + 1) for _ in range(n + 1)]
    safety_stock = [[0] * (m + 1) for _ in range(n + 1)]

    for station in range(1, n + 1):
        coordinates.append((take_int(), take_int()))

        for product in range(1, m + 1):
            initial_inventory[station][product] = take_int()

        for product in range(1, m + 1):
            for period in range(1, h + 1):
                demand[station][product][period] = take_int()

        for product in range(1, m + 1):
            tank_capacity[station][product] = take_int()
            holding_cost[station][product] = take_float()

    if cursor != len(tokens):
        raise ValueError(
            f"{len(tokens) - cursor} valeur(s) inattendue(s) à la fin"
        )

    distances = [
        [
            _rounded_euclidean(coordinates[i], coordinates[j])
            for j in range(n + 1)
        ]
        for i in range(n + 1)
    ]

    raw = Instance(
        n=n,
        m=m,
        comps=comps,
        k=k,
        h=h,
        coordinates=coordinates,
        compartment_sizes=compartment_sizes,
        initial_inventory=initial_inventory,
        demand=demand,
        tank_capacity=tank_capacity,
        holding_cost=holding_cost,
        safety_stock=safety_stock,
        max_trips=max_trips,
        distances=distances,
        station_order=list(range(1, n + 1)),
    )

    return _reorder(raw, _order_stations(raw, option))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Inspecter une instance MCD"
    )

    parser.add_argument("instance")
    parser.add_argument(
        "--option",
        type=int,
        default=0,
        choices=range(5),
    )
    parser.add_argument(
        "--trips",
        type=int,
        default=1,
        help="Nombre maximal de tournées par camion et par période.",
    )

    args = parser.parse_args()

    data = load_instance(
        args.instance,
        args.option,
        max_trips=args.trips,
    )

    print(
        f"stations={data.n}, produits={data.m}, "
        f"compartiments={data.comps}, vehicules={data.k}, "
        f"periodes={data.h}"
    )
    print(f"ordre des stations: {data.station_order}")
    print(f"coordonnees du depot: {data.coordinates[0]}")
    print(f"tournées maximales par camion et période: {data.max_trips}")