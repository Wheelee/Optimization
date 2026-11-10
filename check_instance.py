from instance_reader import load_instance


INSTANCE_PATH = "instances/mcd-10-1-3-5-3-1.dat"
MAX_TRIPS = 1


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_instance_summary(instance) -> None:
    print_header("RÉSUMÉ DE L'INSTANCE")

    print(f"Stations : {instance.n}")
    print(f"Produits : {instance.m}")
    print(f"Compartiments par camion : {instance.comps}")
    print(f"Camions : {instance.k}")
    print(f"Périodes : {instance.h}")
    print(f"Tournées maximales par camion et période : {instance.max_trips}")

    print(f"\nOrdre des stations : {instance.station_order}")
    print(f"Coordonnées du dépôt : {instance.coordinates[0]}")


def print_compartments(instance) -> None:
    print_header("CAPACITÉS DES COMPARTIMENTS")

    for vehicle in range(1, instance.k + 1):
        print(f"\nCamion {vehicle}")

        for compartment in range(1, instance.comps + 1):
            capacity = instance.compartment_sizes[vehicle][compartment]
            print(f"  Compartiment {compartment} : {capacity}")


def print_stations(instance) -> None:
    print_header("DONNÉES DES STATIONS")

    for station in range(1, instance.n + 1):
        x, y = instance.coordinates[station]

        print(f"\nStation {station}")
        print(f"  Coordonnées : ({x}, {y})")
        print(f"  Distance au dépôt : {instance.distances[0][station]}")

        for product in range(1, instance.m + 1):
            print(f"\n  Produit {product}")
            print(
                "    Stock initial : "
                f"{instance.initial_inventory[station][product]}"
            )
            print(
                "    Stock de sécurité : "
                f"{instance.safety_stock[station][product]}"
            )
            print(
                "    Capacité du réservoir : "
                f"{instance.tank_capacity[station][product]}"
            )
            print(
                "    Coût de stockage : "
                f"{instance.holding_cost[station][product]}"
            )

            print("    Consommations :")

            for period in range(1, instance.h + 1):
                consumption = instance.demand[station][product][period]
                print(f"      Période {period} : {consumption}")

            total_consumption = sum(
                instance.demand[station][product][period]
                for period in range(1, instance.h + 1)
            )

            print(f"      Total sur l'horizon : {total_consumption}")


def print_distances(instance) -> None:
    print_header("MATRICE DES DISTANCES")

    print("      ", end="")

    for station in range(instance.n + 1):
        print(f"{station:>8}", end="")

    print()

    for i in range(instance.n + 1):
        print(f"{i:>6}", end="")

        for j in range(instance.n + 1):
            print(f"{instance.distances[i][j]:>8}", end="")

        print()


def main() -> None:
    instance = load_instance(
        INSTANCE_PATH,
        option=0,
        max_trips=MAX_TRIPS,
    )

    print_instance_summary(instance)
    print_compartments(instance)
    print_stations(instance)
    print_distances(instance)

    print("\nLecture de l'instance terminée sans erreur.")


if __name__ == "__main__":
    main()