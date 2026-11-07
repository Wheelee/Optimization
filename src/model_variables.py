"""Déclaration des variables de décision avec Gurobi.

Cette étape crée le modèle Gurobi et ses variables, mais n'ajoute encore
aucune contrainte ni fonction objectif.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.model_setup import ModelData, prepare_model_data


Key = Tuple[int, ...]
VariableMap = Dict[Key, Any]


@dataclass
class GurobiVariables:
    """Références vers les variables Gurobi de la formulation."""

    stock: VariableMap          # I[i,p,t]
    active_route: VariableMap   # a[k,r,t]
    visited: VariableMap        # y[i,k,r,t]
    movement: VariableMap       # x[i,j,k,r,t]
    assignment: VariableMap     # z[i,p,k,l,r,t]
    delivery: VariableMap       # q[i,p,k,l,r,t]
    order: VariableMap          # u[i,k,r,t]


def _require_gurobi():
    """Importe Gurobi seulement lors de la construction du modèle."""
    try:
        import gurobipy as gp
        return gp
    except ImportError as exc:
        raise RuntimeError(
            "gurobipy n'est pas installé. Installe Gurobi Optimizer et son "
            "API Python, puis vérifie qu'une licence Gurobi est disponible."
        ) from exc


def build_gurobi_model(
    data: ModelData,
    model_name: str = "fuel_replenishment",
):
    """Crée un modèle Gurobi et toutes les variables de l'étape 2.

    Retourne ``(model, variables)``. Les contraintes et l'objectif seront
    ajoutés dans les étapes suivantes.
    """
    gp = _require_gurobi()
    model = gp.Model(model_name)
    instance = data.instance

    stock = {}
    for i in data.stations:
        for p in data.products:
            for t in data.periods:
                stock[i, p, t] = model.addVar(
                    vtype=gp.GRB.CONTINUOUS,
                    lb=0.0,
                    ub=instance.tank_capacity[i][p],
                    name=f"I_{i}_{p}_{t}",
                )

    active_route = {}
    for k in data.vehicles:
        for r in data.routes[k]:
            for t in data.periods:
                active_route[k, r, t] = model.addVar(
                    vtype=gp.GRB.BINARY,
                    name=f"a_{k}_{r}_{t}",
                )

    visited = {}
    for i in data.stations:
        for k in data.vehicles:
            for r in data.routes[k]:
                for t in data.periods:
                    visited[i, k, r, t] = model.addVar(
                        vtype=gp.GRB.BINARY,
                        name=f"y_{i}_{k}_{r}_{t}",
                    )

    movement = {}
    for i, j in data.arcs:
        for k in data.vehicles:
            for r in data.routes[k]:
                for t in data.periods:
                    movement[i, j, k, r, t] = model.addVar(
                        vtype=gp.GRB.BINARY,
                        name=f"x_{i}_{j}_{k}_{r}_{t}",
                    )

    assignment = {}
    delivery = {}
    for i in data.stations:
        for p in data.products:
            for k in data.vehicles:
                for l in data.compartments[k]:
                    for r in data.routes[k]:
                        for t in data.periods:
                            key = (i, p, k, l, r, t)
                            assignment[key] = model.addVar(
                                vtype=gp.GRB.BINARY,
                                name=f"z_{i}_{p}_{k}_{l}_{r}_{t}",
                            )
                            delivery[key] = model.addVar(
                                vtype=gp.GRB.CONTINUOUS,
                                lb=0.0,
                                ub=instance.compartment_sizes[k][l],
                                name=f"q_{i}_{p}_{k}_{l}_{r}_{t}",
                            )

    order = {}
    for i in data.stations:
        for k in data.vehicles:
            for r in data.routes[k]:
                for t in data.periods:
                    order[i, k, r, t] = model.addVar(
                        vtype=gp.GRB.CONTINUOUS,
                        lb=0.0,
                        ub=float(instance.n),
                        name=f"u_{i}_{k}_{r}_{t}",
                    )

    model.update()
    variables = GurobiVariables(
        stock=stock,
        active_route=active_route,
        visited=visited,
        movement=movement,
        assignment=assignment,
        delivery=delivery,
        order=order,
    )
    return model, variables


def variable_counts(variables: GurobiVariables) -> Dict[str, int]:
    return {
        "I_stock": len(variables.stock),
        "a_tournee": len(variables.active_route),
        "y_visite": len(variables.visited),
        "x_deplacement": len(variables.movement),
        "z_affectation": len(variables.assignment),
        "q_livraison": len(variables.delivery),
        "u_ordre_MTZ": len(variables.order),
    }


if __name__ == "__main__":
    instance_path = PROJECT_ROOT / "data/instances/mcd/mcd-10-1-3-5-1-1.dat"
    data = prepare_model_data(instance_path)
    try:
        model, variables = build_gurobi_model(data)
    except RuntimeError as exc:
        print(f"Configuration Gurobi incomplète : {exc}")
        raise SystemExit(1)

    print("Étape 2 - variables Gurobi déclarées")
    for name, count in variable_counts(variables).items():
        print(f"{name:20s}: {count}")
    print(f"Variables Gurobi dans le modèle : {model.NumVars}")
