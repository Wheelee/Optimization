import gurobipy as gp
from gurobipy import GRB


def build_model(instance, time_limit: int = 300):
    """Construit le modèle MILP du Problème 1.

    Le modèle détermine :
    - les périodes de livraison de chaque station ;
    - les quantités livrées de chaque produit ;
    - l'affectation des produits aux compartiments ;
    - l'affectation des stations aux tournées ;
    - les tournées réalisées par les camions ;
    - les routes suivies par les camions.

    L'objectif minimise la distance totale parcourue sur l'horizon.
    """

    n = instance.n
    m = instance.m
    k = instance.k
    h = instance.h
    comps = instance.comps

    stations = range(1, n + 1)
    products = range(1, m + 1)
    vehicles = range(1, k + 1)
    periods = range(1, h + 1)
    compartments = range(1, comps + 1)
    trips = range(1, instance.max_trips + 1)

    depot = 0

    model = gp.Model("MultiPeriodPetrolStationIRP")

    model.Params.TimeLimit = time_limit
    model.Params.MIPGap = 0.0

    # ------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------

    # I[i, p, t] : stock du produit p à la station i en fin de période t
    I = model.addVars(
        [
            (i, p, t)
            for i in stations
            for p in products
            for t in periods
        ],
        vtype=GRB.CONTINUOUS,
        name="I",
    )

    # y[i, t] : 1 si la station i est livrée pendant la période t
    y = model.addVars(
        [
            (i, t)
            for i in stations
            for t in periods
        ],
        vtype=GRB.BINARY,
        name="y",
    )

    # q[i, p, t] : quantité du produit p livrée à la station i en période t
    q = model.addVars(
        [
            (i, p, t)
            for i in stations
            for p in products
            for t in periods
        ],
        vtype=GRB.CONTINUOUS,
        name="q",
    )

    # x[k, r, i, j, t] : 1 si le camion k réalise l'arc (i, j)
    # pendant sa tournée r à la période t
    x = model.addVars(
        [
            (k, r, i, j, t)
            for k in vehicles
            for r in trips
            for i in range(n + 1)
            for j in range(n + 1)
            if i != j
            for t in periods
        ],
        vtype=GRB.BINARY,
        name="x",
    )

    # z[k, r, i, t] : 1 si le camion k visite la station i
    # pendant sa tournée r à la période t
    z = model.addVars(
        [
            (k, r, i, t)
            for k in vehicles
            for r in trips
            for i in stations
            for t in periods
        ],
        vtype=GRB.BINARY,
        name="z",
    )

    # u[k, r, i, p, l, t] : quantité du produit p chargée dans le
    # compartiment l du camion k pour la station i pendant la période t
    u = model.addVars(
        [
            (k, r, i, p, l, t)
            for k in vehicles
            for r in trips
            for i in stations
            for p in products
            for l in compartments
            for t in periods
        ],
        vtype=GRB.CONTINUOUS,
        name="u",
    )

    # a[k, r, p, l, t] : 1 si le compartiment l du camion k contient
    # le produit p pendant la tournée r à la période t
    a = model.addVars(
        [
            (k, r, p, l, t)
            for k in vehicles
            for r in trips
            for p in products
            for l in compartments
            for t in periods
        ],
        vtype=GRB.BINARY,
        name="a",
    )

    # ------------------------------------------------------------------
    # Fonction objectif
    # ------------------------------------------------------------------

    model.setObjective(
        gp.quicksum(
            instance.distances[i][j] * x[k, r, i, j, t]
            for k in vehicles
            for r in trips
            for i in range(n + 1)
            for j in range(n + 1)
            if i != j
            for t in periods
        ),
        GRB.MINIMIZE,
    )

    # ------------------------------------------------------------------
    # Contraintes de stocks
    # ------------------------------------------------------------------

    for i in stations:
        for p in products:
            for t in periods:
                deliveries = gp.quicksum(
                    q[i, p, tau]
                    for tau in periods
                    if tau <= t
                )

                consumption = gp.quicksum(
                    instance.demand[i][p][tau]
                    for tau in periods
                    if tau <= t
                )

                model.addConstr(
                    I[i, p, t]
                    == instance.initial_inventory[i][p]
                    + deliveries
                    - consumption,
                    name=f"inventory_balance[{i},{p},{t}]",
                )

                model.addConstr(
                    I[i, p, t] >= instance.safety_stock[i][p],
                    name=f"safety_stock[{i},{p},{t}]",
                )

                model.addConstr(
                    I[i, p, t] <= instance.tank_capacity[i][p],
                    name=f"tank_capacity[{i},{p},{t}]",
                )

    # ------------------------------------------------------------------
    # Lien entre livraison et visite
    # ------------------------------------------------------------------

    for i in stations:
        for p in products:
            for t in periods:
                model.addConstr(
                    q[i, p, t]
                    <= instance.tank_capacity[i][p] * y[i, t],
                    name=f"delivery_requires_visit[{i},{p},{t}]",
                )

    # ------------------------------------------------------------------
    # Affectation des produits aux compartiments
    # ------------------------------------------------------------------

    for k in vehicles:
        for r in trips:
            for p in products:
                for l in compartments:
                    for t in periods:
                        model.addConstr(
                            gp.quicksum(
                                u[k, r, i, p, l, t]
                                for i in stations
                            )
                            <= instance.compartment_sizes[k][l]
                            * a[k, r, p, l, t],
                            name=(
                                f"compartment_capacity"
                                f"[{k},{r},{p},{l},{t}]"
                            ),
                        )

            # Un compartiment contient au plus un produit
            for l in compartments:
                for t in periods:
                    model.addConstr(
                        gp.quicksum(
                            a[k, r, p, l, t]
                            for p in products
                        )
                        <= 1,
                        name=(
                            f"one_product_per_compartment"
                            f"[{k},{r},{l},{t}]"
                        ),
                    )

    # ------------------------------------------------------------------
    # Cohérence entre livraisons et affectations
    # ------------------------------------------------------------------

    for i in stations:
        for p in products:
            for t in periods:
                model.addConstr(
                    q[i, p, t]
                    == gp.quicksum(
                        u[k, r, i, p, l, t]
                        for k in vehicles
                        for r in trips
                        for l in compartments
                    ),
                    name=(
                        f"delivery_equals_loading"
                        f"[{i},{p},{t}]"
                    ),
                )

    # ------------------------------------------------------------------
    # Contraintes de routage
    # ------------------------------------------------------------------

    for k in vehicles:
        for r in trips:
            for t in periods:
                # Une tournée ne peut être utilisée qu'une fois
                model.addConstr(
                    gp.quicksum(
                        x[k, r, depot, j, t]
                        for j in stations
                    )
                    <= 1,
                    name=(
                        f"one_departure"
                        f"[{k},{r},{t}]"
                    ),
                )

                model.addConstr(
                    gp.quicksum(
                        x[k, r, i, depot, t]
                        for i in stations
                    )
                    <= 1,
                    name=(
                        f"one_return"
                        f"[{k},{r},{t}]"
                    ),
                )

                # Si un camion part, il doit revenir
                model.addConstr(
                    gp.quicksum(
                        x[k, r, depot, j, t]
                        for j in stations
                    )
                    == gp.quicksum(
                        x[k, r, i, depot, t]
                        for i in stations
                    ),
                    name=(
                        f"departure_equals_return"
                        f"[{k},{r},{t}]"
                    ),
                )

                # Conservation du flux
                for i in stations:
                    model.addConstr(
                        gp.quicksum(
                            x[k, r, i, j, t]
                            for j in range(n + 1)
                            if j != i
                        )
                        == z[k, r, i, t],
                        name=(
                            f"flow_out"
                            f"[{k},{r},{i},{t}]"
                        ),
                    )

                    model.addConstr(
                        gp.quicksum(
                            x[k, r, j, i, t]
                            for j in range(n + 1)
                            if j != i
                        )
                        == z[k, r, i, t],
                        name=(
                            f"flow_in"
                            f"[{k},{r},{i},{t}]"
                        ),
                    )

                # Élimination des sous-tours
                for i in stations:
                    for j in stations:
                        if i < j:
                            model.addConstr(
                                x[k, r, i, j, t]
                                + x[k, r, j, i, t]
                                <= z[k, r, i, t],
                                name=(
                                    f"subtour_elimination"
                                    f"[{k},{r},{i},{j},{t}]"
                                ),
                            )

    # ------------------------------------------------------------------
    # Cohérence entre visites et livraisons
    # ------------------------------------------------------------------

    for i in stations:
        for t in periods:
            model.addConstr(
                y[i, t]
                <= gp.quicksum(
                    z[k, r, i, t]
                    for k in vehicles
                    for r in trips
                ),
                name=f"visit_required[{i},{t}]",
            )

            model.addConstr(
                gp.quicksum(
                    z[k, r, i, t]
                    for k in vehicles
                    for r in trips
                )
                <= 1,
                name=f"single_visit[{i},{t}]",
            )

    # ------------------------------------------------------------------
    # Contraintes de capacité des camions
    # ------------------------------------------------------------------

    for k in vehicles:
        for r in trips:
            for t in periods:
                model.addConstr(
                    gp.quicksum(
                        u[k, r, i, p, l, t]
                        for i in stations
                        for p in products
                        for l in compartments
                    )
                    <= gp.quicksum(
                        instance.compartment_sizes[k][l]
                        for l in compartments
                    ),
                    name=(
                        f"truck_capacity"
                        f"[{k},{r},{t}]"
                    ),
                )

    return model, {
        "I": I,
        "y": y,
        "q": q,
        "x": x,
        "z": z,
        "u": u,
        "a": a,
    }