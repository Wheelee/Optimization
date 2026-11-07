"""Contraintes (2) à (14) de « optimisation (2).pdf », problème 1.

Correspondance entre la formulation et les noms affichés dans main.py :
    (2)  stock_balance            : bilan de stock en fin de période.
    (3)  safety_stock             : stock minimal de sécurité.
         La limite supérieure de (3) est la borne ub de la variable stock
         dans model_variables.py (capacité de la cuve).
    (4)  tank_before_consumption  : capacité de cuve avant consommation.
    (5)  compartment_assignment   : affectation unique d'un compartiment.
    (6)  delivery_capacity        : livraison limitée par l'affectation et
         la capacité du compartiment ; q >= 0 est une borne de variable.
    (7)  assignment_visit         : affectation seulement si la station est visitée.
    (8)  depot_departure          : départ du dépôt d'une tournée active.
    (9)  depot_return             : retour au dépôt d'une tournée active.
    (10) station_incoming         : un arc entrant par station visitée.
    (11) station_outgoing         : un arc sortant par station visitée.
    (12) visit_active             : visite seulement dans une tournée active.
    (13) order_lower/order_upper  : bornes des variables d'ordre MTZ.
    (14) mtz                      : élimination des sous-tours entre stations.

Les numéros suivent le PDF, même si les boucles regroupent autrement les
contraintes dans le code. L'équation (1) est l'objectif, encore à ajouter.

Les livraisons précèdent la consommation. Un compartiment peut être rempli
partiellement, mais dessert au plus un couple station-produit par tournée.
Les bornes supérieures des stocks et les domaines sont déjà fixés à la
création des variables. Aucun objectif n'est défini ici.
"""

from typing import Any, Dict

from src.model_setup import ModelData
from src.model_variables import GurobiVariables, _require_gurobi


def add_model_constraints(
    model: Any, data: ModelData, variables: GurobiVariables,
) -> Dict[str, int]:
    """Ajoute au modèle les contraintes (2)-(14) à partir des données et variables.

    Modifie le modèle reçu, le synchronise avec model.update(), puis retourne
    un dictionnaire {nom de famille: nombre de contraintes ajoutées}.
    À appeler une seule fois par modèle : un second appel ajouterait des doublons.
    Cette fonction ne définit pas l'objectif et ne lance pas la résolution.
    """
    gp = _require_gurobi()
    instance = data.instance
    v = variables
    counts: Dict[str, int] = {}

    def add(family, indices, expression):
        """Ajoute une expression nommée famille_indices et met à jour son compteur."""
        # Chaque appel ajoute une contrainte Gurobi nommée pour les indices
        # donnés, puis incrémente le compteur de sa famille pour main.py.
        suffix = "_".join(str(index) for index in indices)
        model.addConstr(expression, name=f"{family}_{suffix}")
        counts[family] = counts.get(family, 0) + 1

    # (2)-(4) Stocks : I[i,p,0] est une donnée, pas une variable.
    for i in data.stations:
        for p in data.products:
            for t in data.periods:
                previous = (instance.initial_inventory[i][p] if t == 1
                            else v.stock[i, p, t - 1])
                delivered = gp.quicksum(
                    v.delivery[i, p, k, l, r, t]
                    for k in data.vehicles for r in data.routes[k]
                    for l in data.compartments[k]
                )
                # (2) Bilan : stock final = stock précédent + livraisons - demande.
                add("stock_balance", (i, p, t),
                    v.stock[i, p, t] == previous + delivered - instance.demand[i][p][t])
                # (3) Limites de stock : S_ip <= I_ipt <= C_ip.
                # Ici, on ajoute la limite basse ; la limite haute est déjà
                # imposée par ub=instance.tank_capacity[i][p] dans les variables.
                add("safety_stock", (i, p, t),
                    v.stock[i, p, t] >= data.security_stock[i, p])
                # (4) Avant consommation : stock précédent + livraisons <= C_ip.
                # Empêche un débordement, même si le stock final respecte (3).
                add("tank_before_consumption", (i, p, t),
                    previous + delivered <= instance.tank_capacity[i][p])

    for k in data.vehicles:
        for r in data.routes[k]:
            for t in data.periods:
                active = v.active_route[k, r, t]
                # (5) Un seul couple station-produit par compartiment.
                # Somme des z <= a : aucune affectation si la tournée est inactive.
                for l in data.compartments[k]:
                    add("compartment_assignment", (k, l, r, t),
                        gp.quicksum(v.assignment[i, p, k, l, r, t]
                                    for i in data.stations for p in data.products) <= active)

                # (8) Départ : somme des arcs dépôt -> station = a_krt.
                add("depot_departure", (k, r, t),
                    gp.quicksum(v.movement[0, i, k, r, t]
                                for i in data.stations) == active)
                # (9) Retour : somme des arcs station -> dépôt = a_krt.
                add("depot_return", (k, r, t),
                    gp.quicksum(v.movement[i, 0, k, r, t]
                                for i in data.stations) == active)

                for i in data.stations:
                    visit = v.visited[i, k, r, t]
                    # (6)-(7) Quantités, capacités et lien avec les visites.
                    for p in data.products:
                        for l in data.compartments[k]:
                            key = (i, p, k, l, r, t)
                            # (6) q <= Q_kl * z : sans affectation, livraison nulle ;
                            # sinon, remplissage partiel possible jusqu'à Q_kl.
                            # La borne q >= 0 est fixée dans model_variables.py.
                            add("delivery_capacity", key,
                                v.delivery[key] <= instance.compartment_sizes[k][l]
                                * v.assignment[key])
                            # (7) z <= y : affecter un compartiment exige une visite.
                            add("assignment_visit", key, v.assignment[key] <= visit)

                    # (10) Entrée : somme des arcs j -> i = y_ikrt.
                    add("station_incoming", (i, k, r, t),
                        gp.quicksum(v.movement[j, i, k, r, t]
                                    for j in data.locations if j != i) == visit)
                    # (11) Sortie : somme des arcs i -> j = y_ikrt.
                    add("station_outgoing", (i, k, r, t),
                        gp.quicksum(v.movement[i, j, k, r, t]
                                    for j in data.locations if j != i) == visit)
                    # (12) y <= a : aucune visite dans une tournée inactive.
                    add("visit_active", (i, k, r, t), visit <= active)

                    # (13) y <= u <= n*y : ordre nul si la station n'est pas
                    # visitée, compris entre 1 et n sinon. Deux contraintes
                    # Gurobi représentent cette double inégalité du PDF.
                    add("order_lower", (i, k, r, t), v.order[i, k, r, t] >= visit)
                    add("order_upper", (i, k, r, t),
                        v.order[i, k, r, t] <= instance.n * visit)
                    # (14) u_i - u_j + n*x_ij <= n - y_j, pour i != j,
                    # sans le dépôt. Un arc utilisé impose u_j >= u_i + 1,
                    # ce qui interdit les cycles déconnectés du dépôt.
                    for j in data.stations:
                        if i != j:
                            add("mtz", (i, j, k, r, t),
                                v.order[i, k, r, t] - v.order[j, k, r, t]
                                + instance.n * v.movement[i, j, k, r, t]
                                <= instance.n - v.visited[j, k, r, t])

    model.update()
    return counts
