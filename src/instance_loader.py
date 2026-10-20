"""Lecture des instances MCD de réapprovisionnement en carburant."""

from dataclasses import dataclass
from math import hypot
from pathlib import Path
from typing import List, Tuple, Union


@dataclass
class Instance:
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
    distances: List[List[int]]
    station_order: List[int]

    @property
    def vehicles(self) -> int:
        return self.k

    @property
    def periods(self) -> int:
        return self.h


def _rounded_euclidean(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return int(hypot(a[0] - b[0], a[1] - b[1]) + 0.5)


def _order_stations(instance: Instance, option: int) -> List[int]:
    """0 fichier, 1 demande totale, 2 produit 1,
    3 distance croissante, 4 distance décroissante."""
    stations = list(range(1, instance.n + 1))
    if option == 0:
        return stations
    if option == 1:
        return sorted(stations, key=lambda i: sum(
            instance.demand[i][p][t]
            for p in range(1, instance.m + 1)
            for t in range(1, instance.h + 1)), reverse=True)
    if option == 2:
        return sorted(stations, key=lambda i: sum(
            instance.demand[i][1][t]
            for t in range(1, instance.h + 1)), reverse=True)
    if option == 3:
        return sorted(stations, key=lambda i: instance.distances[0][i])
    if option == 4:
        return sorted(stations, key=lambda i: instance.distances[0][i], reverse=True)
    raise ValueError("option doit valoir 0, 1, 2, 3 ou 4")


def _reorder(instance: Instance, station_order: List[int]) -> Instance:
    order = [0] + station_order
    return Instance(
        n=instance.n, m=instance.m, comps=instance.comps,
        k=instance.k, h=instance.h,
        coordinates=[instance.coordinates[i] for i in order],
        compartment_sizes=instance.compartment_sizes,
        initial_inventory=[instance.initial_inventory[i][:] for i in order],
        demand=[[product[:] for product in instance.demand[i]] for i in order],
        tank_capacity=[instance.tank_capacity[i][:] for i in order],
        holding_cost=[instance.holding_cost[i][:] for i in order],
        distances=[[instance.distances[i][j] for j in order] for i in order],
        station_order=station_order,
    )


def load_instance(path: Union[str, Path], option: int = 0) -> Instance:
    """Charge un fichier .dat et applique l'option de tri demandée."""
    path = Path(path)
    try:
        tokens = path.read_text(encoding="utf-8").split()
    except OSError as exc:
        raise FileNotFoundError(f"Impossible d'ouvrir {path}") from exc
    cursor = 0

    def take_int() -> int:
        nonlocal cursor
        if cursor >= len(tokens):
            raise ValueError(f"Fichier incomplet à la position {cursor}")
        value = int(tokens[cursor])
        cursor += 1
        return value

    def take_float() -> float:
        nonlocal cursor
        if cursor >= len(tokens):
            raise ValueError(f"Fichier incomplet à la position {cursor}")
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
    demand = [[[0] * (h + 2) for _ in range(m + 1)] for _ in range(n + 1)]
    tank_capacity = [[0] * (m + 1) for _ in range(n + 1)]
    holding_cost = [[0.0] * (m + 1) for _ in range(n + 1)]
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
        raise ValueError(f"{len(tokens) - cursor} valeur(s) inattendue(s) à la fin")

    distances = [[_rounded_euclidean(coordinates[i], coordinates[j])
                  for j in range(n + 1)] for i in range(n + 1)]
    raw = Instance(n, m, comps, k, h, coordinates, compartment_sizes,
                   initial_inventory, demand, tank_capacity, holding_cost,
                   distances, list(range(1, n + 1)))
    return _reorder(raw, _order_stations(raw, option))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Inspecter une instance MCD")
    parser.add_argument("instance")
    parser.add_argument("--option", type=int, default=0, choices=range(5))
    args = parser.parse_args()
    data = load_instance(args.instance, args.option)
    print(f"stations={data.n}, produits={data.m}, compartiments={data.comps}, "
          f"vehicules={data.k}, periodes={data.h}")
    print(f"ordre des stations: {data.station_order}")
    print(f"coordonnees du depot: {data.coordinates[0]}")
