"""Petites instances résolues pour vérifier les contraintes du problème 1.

Lancer depuis Optimization : python -B -m unittest discover -s tests -v
Ou ouvrir ce fichier dans l'IDE et cliquer sur ▶ avec l'interpréteur Python
3.12 contenant gurobipy. Le lancement direct fonctionne depuis tout dossier.
Une installation et une licence Gurobi sont nécessaires.

Chaque test construit une petite instance indépendante et vérifie sa faisabilité
avec les contraintes (2) à (14) de « optimisation (2).pdf ». L'objectif est nul :
OPTIMAL signifie ici qu'une solution réalisable a été trouvée, pas que la distance
a été minimisée. INFEASIBLE est le résultat attendu des scénarios interdits.
Un test affiche « ok » lorsque le résultat obtenu correspond au résultat attendu,
y compris quand le modèle testé est volontairement irréalisable.
"""

import sys
import tempfile
import unittest
from pathlib import Path

import gurobipy as gp

# Permet aussi l'exécution directe du fichier avec le bouton ▶ de l'IDE.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.model_constraints import add_model_constraints
from src.model_setup import prepare_model_data
from src.model_variables import build_gurobi_model


class ConstraintTests(unittest.TestCase):
    def make_model(self, rows, periods=1, compartments=1, routes=1, safety=0,
                   products=1, capacities=None):
        """Crée une instance temporaire, ses variables et toutes les contraintes.

        Chaque ligne suit le format MCD : x, y, stocks par produit, demandes
        par produit puis période, couples capacité/coût par produit.
        capacities contient une liste de capacités par camion (même nombre
        de compartiments, comme dans le format MCD). On vérifie également que
        les compteurs de contraintes correspondent au total du modèle.
        Le fichier temporaire est supprimé après lecture ; Gurobi est libéré
        automatiquement à la fin du test grâce à addCleanup.
        """
        capacities = capacities if capacities is not None else [[10] * compartments]
        compartments = len(capacities[0])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "toy.dat"
            path.write_text(
                f"{len(rows)} {products} {compartments} {len(capacities)} {periods}\n0 0\n"
                + " ".join(str(q) for truck in capacities for q in truck) + "\n"
                + "\n".join(rows), encoding="utf-8",
            )
            data = prepare_model_data(path, safety, routes)
        model, variables = build_gurobi_model(data)
        self.addCleanup(model.dispose)
        model.Params.OutputFlag = 0
        counts = add_model_constraints(model, data, variables)
        self.assertEqual(sum(counts.values()), model.NumConstrs)
        return model, variables

    def assert_status(self, model, expected):
        """Résout le problème de faisabilité et compare son statut à celui attendu."""
        # Objectif nul : on vérifie uniquement la faisabilité.
        model.optimize()
        self.assertEqual(model.Status, expected)

    def test_two_products_need_separate_compartments(self):
        """(5)-(6) Deux produits demandés : un compartiment échoue, deux suffisent."""
        row = ["1 0 0 0 3 4 10 0.01 10 0.01"]
        for capacities, expected in [([[10]], gp.GRB.INFEASIBLE),
                                     ([[3, 4]], gp.GRB.OPTIMAL)]:
            with self.subTest(capacities=capacities):
                model, _ = self.make_model(row, products=2, capacities=capacities)
                self.assert_status(model, expected)

    def test_two_heterogeneous_trucks_supply_one_station(self):
        """(2), (5)-(9) Une demande de 11 impose deux camions de capacités 4 et 7."""
        model, v = self.make_model(["1 0 0 11 20 0.01"], capacities=[[4], [7]])
        self.assert_status(model, gp.GRB.OPTIMAL)
        for k, quantity in [(1, 4), (2, 7)]:
            self.assertAlmostEqual(v.delivery[1, 1, k, 1, 1, 1].X, quantity)
            self.assertAlmostEqual(v.visited[1, k, 1, 1].X, 1)

    def test_individual_safety_stocks_and_route_limits(self):
        """Les stocks 1/2 et les limites 1/2 s'appliquent aux bons indices."""
        model, v = self.make_model(
            ["1 0 1 2 1 1 10 0.01 10 0.01"], products=2,
            capacities=[[3], [4]], safety={(1, 1): 1, (1, 2): 2},
            routes={1: 1, 2: 2},
        )
        self.assertNotIn((1, 2, 1), v.active_route)
        self.assertIn((2, 2, 1), v.active_route)
        for key in v.delivery:
            model.addConstr(v.delivery[key] == 0)
        self.assert_status(model, gp.GRB.INFEASIBLE)

    def test_invalid_configuration_is_rejected(self):
        """Rejette valeurs non finies, limites non entières et dictionnaires incomplets."""
        for options in [dict(safety=float('nan')), dict(safety=float('inf')),
                        dict(safety={}), dict(routes={}), dict(routes=1.5),
                        dict(routes=0), dict(safety=3)]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.make_model(["1 0 2 1 10 0.01"], **options)

    def test_documented_example(self):
        """Vérifie les deux jours documentés avec deux tournées et deux produits.

        Chaque tournée dessert une seule station avec deux compartiments.
        Les livraisons égalent les demandes ; les stocks finaux restent 2/1 et 1/2.
        """
        model, v = self.make_model([
            "3 4 2 1 5 4 3 2 12 0.01 10 0.01",
            "6 8 1 2 3 2 2 4 10 0.01 10 0.01",
        ], periods=2, products=2, capacities=[[10, 8]], routes=2)
        quantities = {(1, 1): (5, 3), (1, 2): (4, 2),
                      (2, 1): (3, 2), (2, 2): (2, 4)}
        for key, variable in v.delivery.items():
            i, p, k, l, r, t = key
            model.addConstr(variable == (quantities[i, t][p - 1]
                                         if r == i and l == p else 0))
        self.assert_status(model, gp.GRB.OPTIMAL)
        for (i, p, t), variable in v.stock.items():
            self.assertAlmostEqual(variable.X, {(1, 1): 2, (1, 2): 1,
                                               (2, 1): 1, (2, 2): 2}[i, p])

    def test_partial_load_and_inventory_across_periods(self):
        """Accepte une charge partielle et reporte correctement le stock sur deux jours.

        Contraintes concernées : (2)-(4), (6), (8)-(9).
        Stock initial 2, livraison imposée de 6 sur une capacité de 10 au jour 1,
        demandes de 3 puis 4, aucune tournée au jour 2 : stocks attendus 5 puis 1.
        Le modèle doit être réalisable et utiliser les arcs dépôt -> station
        et station -> dépôt au jour 1.
        """
        model, v = self.make_model(["1 0 2 3 4 10 0.01"], periods=2, safety=1)
        model.addConstr(v.delivery[1, 1, 1, 1, 1, 1] == 6)
        model.addConstr(v.active_route[1, 1, 2] == 0)
        self.assert_status(model, gp.GRB.OPTIMAL)
        self.assertAlmostEqual(v.stock[1, 1, 1].X, 5)
        self.assertAlmostEqual(v.stock[1, 1, 2].X, 1)
        self.assertAlmostEqual(v.movement[0, 1, 1, 1, 1].X, 1)
        self.assertAlmostEqual(v.movement[1, 0, 1, 1, 1].X, 1)

    def test_overflow_before_consumption_is_rejected(self):
        """Rejette une livraison qui fait déborder la cuve avant consommation (4).

        Stock initial 8 + livraison imposée 5 = 13, pour une cuve de capacité 10.
        Le stock final serait pourtant admissible : 13 - demande 5 = 8.
        Résultat attendu : INFEASIBLE, grâce à la limite avant consommation.
        """
        model, v = self.make_model(["1 0 8 5 10 0.01"])
        model.addConstr(v.delivery[1, 1, 1, 1, 1, 1] == 5)
        self.assert_status(model, gp.GRB.INFEASIBLE)

    def test_compartment_cannot_supply_two_stations(self):
        """Interdit de partager un compartiment entre deux stations (5)-(6).

        Deux stations sans stock demandent chacune 2. Un seul compartiment de
        capacité 10 et une seule tournée sont disponibles. Le volume suffirait,
        mais l'affectation à deux stations est interdite : INFEASIBLE attendu.
        """
        model, _ = self.make_model(["1 0 0 2 10 0.01", "2 0 0 2 10 0.01"])
        self.assert_status(model, gp.GRB.INFEASIBLE)

    def test_two_routes_can_supply_same_station(self):
        """Autorise une station à recevoir plusieurs tournées dans une période.

        Contraintes concernées : (2), (5)-(9). Une station sans stock demande 15,
        avec un seul compartiment de capacité 10 et deux tournées possibles.
        Résultat attendu : modèle réalisable, avec les deux tournées actives.
        """
        model, v = self.make_model(["1 0 0 15 20 0.01"], routes=2)
        self.assert_status(model, gp.GRB.OPTIMAL)
        self.assertAlmostEqual(sum(v.active_route[1, r, 1].X for r in (1, 2)), 2)

    def test_disconnected_cycle_is_rejected(self):
        """Élimine un cycle de stations déconnecté du dépôt avec MTZ (13)-(14).

        On impose le parcours 0 -> 1 -> 0 et, séparément, le cycle 2 -> 3 -> 2.
        Les degrés entrants/sortants sont compatibles avec ces arcs, mais MTZ
        interdit le cycle isolé : résultat attendu INFEASIBLE.
        """
        model, v = self.make_model([
            "1 0 0 0 10 0.01", "2 0 0 0 10 0.01", "3 0 0 0 10 0.01",
        ])
        for i, j in [(0, 1), (1, 0), (2, 3), (3, 2)]:
            model.addConstr(v.movement[i, j, 1, 1, 1] == 1)
        self.assert_status(model, gp.GRB.INFEASIBLE)

    def test_delivery_requires_visit(self):
        """Interdit de satisfaire une demande sans visiter la station (2), (6)-(7).

        La station n'a aucun stock et demande 2, mais sa visite est fixée à zéro.
        La livraison nécessaire devient impossible : INFEASIBLE attendu.
        """
        model, v = self.make_model(["1 0 0 2 10 0.01"])
        model.addConstr(v.visited[1, 1, 1, 1] == 0)
        self.assert_status(model, gp.GRB.INFEASIBLE)

    def test_safety_stock_is_enforced(self):
        """Impose de conserver le stock de sécurité après consommation (2)-(3).

        Stock initial 2, demande 2 et stock de sécurité 1. Sans tournée autorisée,
        le stock final serait nul, donc inférieur à 1 : INFEASIBLE attendu.
        """
        model, v = self.make_model(["1 0 2 2 10 0.01"], safety=1)
        model.addConstr(v.active_route[1, 1, 1] == 0)
        self.assert_status(model, gp.GRB.INFEASIBLE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
