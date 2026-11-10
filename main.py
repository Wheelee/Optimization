from instance_reader import load_instance
from model import build_model


INSTANCE_PATH = "instances/mcd-10-1-3-5-1-1.dat"
MAX_TRIPS = 1
TIME_LIMIT = 300


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_model_status(model) -> None:
    print_header("RÉSULTAT DU SOLVEUR")

    print(f"Statut : {model.status}")

    if model.SolCount == 0:
        print("Aucune solution n'a été trouvée.")
        return

    print(f"Valeur de la fonction objectif : {model.objVal:.2f}")
    print(f"Meilleure borne : {model.objBound:.2f}")
    print(f"Écart relatif : {model.MIPGap * 100:.4f} %")
    print(f"Temps de résolution : {model.Runtime:.2f} secondes")


def print_inventory(instance, variables) -> None:
    print_header("STOCKS EN FIN DE PÉRIODE")

    for i in range(1, instance.n + 1):
        for p in range(1, instance.m + 1):
            print(f"\nStation {i}, produit {p}")

            for t in range(1, instance.h + 1):
                stock = variables["I"][i, p, t].X
                print(f"  Période {t} : {stock:.2f}")


def print_deliveries(instance, variables) -> None:
    print_header("LIVRAISONS")

    found = False

    for i in range(1, instance.n + 1):
        for p in range(1, instance.m + 1):
            for t in range(1, instance.h + 1):
                quantity = variables["q"][i, p, t].X

                if quantity > 1e-6:
                    found = True
                    print(
                        f"Station {i}, produit {p}, période {t} : "
                        f"{quantity:.2f}"
                    )

    if not found:
        print("Aucune livraison n'a été effectuée.")


def print_visits(instance, variables) -> None:
    print_header("VISITES DES STATIONS")

    found = False

    for i in range(1, instance.n + 1):
        for t in range(1, instance.h + 1):
            visited = variables["y"][i, t].X > 0.5

            if visited:
                found = True
                print(f"Station {i} livrée pendant la période {t}.")

    if not found:
        print("Aucune station n'a été livrée.")


def print_routes(instance, variables) -> None:
    print_header("ROUTES UTILISÉES")

    found = False

    for k in range(1, instance.k + 1):
        for r in range(1, instance.max_trips + 1):
            for t in range(1, instance.h + 1):
                route = []

                for i in range(instance.n + 1):
                    for j in range(instance.n + 1):
                        if i == j:
                            continue

                        if variables["x"][k, r, i, j, t].X > 0.5:
                            route.append((i, j))

                if route:
                    found = True
                    print(
                        f"\nCamion {k}, tournée {r}, période {t} :"
                    )

                    for i, j in route:
                        print(f"  {i} -> {j}")

    if not found:
        print("Aucune tournée n'a été utilisée.")


def print_compartment_assignments(instance, variables) -> None:
    print_header("AFFECTATIONS AUX COMPARTIMENTS")

    found = False

    for k in range(1, instance.k + 1):
        for r in range(1, instance.max_trips + 1):
            for p in range(1, instance.m + 1):
                for l in range(1, instance.comps + 1):
                    for t in range(1, instance.h + 1):
                        assigned = variables["a"][k, r, p, l, t].X > 0.5

                        if assigned:
                            found = True
                            print(
                                f"Camion {k}, tournée {r}, période {t} : "
                                f"compartiment {l} -> produit {p}"
                            )

    if not found:
        print("Aucun compartiment n'a été affecté.")


def print_compartment_loads(instance, variables) -> None:
    print_header("CHARGEMENTS DES COMPARTIMENTS")

    found = False

    for k in range(1, instance.k + 1):
        for r in range(1, instance.max_trips + 1):
            for i in range(1, instance.n + 1):
                for p in range(1, instance.m + 1):
                    for l in range(1, instance.comps + 1):
                        for t in range(1, instance.h + 1):
                            quantity = variables["u"][
                                k, r, i, p, l, t
                            ].X

                            if quantity > 1e-6:
                                found = True
                                print(
                                    f"Camion {k}, tournée {r}, période {t} : "
                                    f"station {i}, produit {p}, "
                                    f"compartiment {l} : "
                                    f"{quantity:.2f}"
                                )

    if not found:
        print("Aucun compartiment n'a été chargé.")


def main() -> None:
    instance = load_instance(
        INSTANCE_PATH,
        option=0,
        max_trips=MAX_TRIPS,
    )

    model, variables = build_model(
        instance,
        time_limit=TIME_LIMIT,
    )

    model.optimize()

    print_model_status(model)

    if model.SolCount == 0:
        return

    print_deliveries(instance, variables)
    print_visits(instance, variables)
    print_inventory(instance, variables)
    print_routes(instance, variables)
    print_compartment_assignments(instance, variables)
    print_compartment_loads(instance, variables)


if __name__ == "__main__":
    main()