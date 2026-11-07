# Projet d'optimisation - Réapprovisionnement en carburant

Ce projet porte sur l'optimisation des tournées de camions qui livrent du
carburant à plusieurs stations pendant plusieurs périodes.

Les 670 instances officielles du benchmark sont disponibles dans
`data/instances/mcd/`. La provenance et les vérifications sont détaillées
dans [data/README.md](data/README.md).

Le dossier contient actuellement :

- `main.py` : lancement des étapes actuelles du problème 1 depuis l'IDE ;
- `src/instance_loader.py` : chargeur Python des fichiers d'instances `.dat` ;
- `src/model_setup.py` : préparation des ensembles et paramètres du modèle ;
- `scripts/view_instance.py` : programme d'affichage direct d'une instance exemple ;
- `docs/phase_analyse_donnees.md` : analyse détaillée du format et toy example ;
- `docs/analyse_coherence_formulation.txt` : analyse de cohérence de la formulation.

## Lancement depuis l'IDE

Ouvrir `main.py` puis cliquer sur le bouton ▶ pour exécuter le fichier Python.
Il affiche l'instance, prépare les données et déclare les variables Gurobi.
Les chemins sont calculés depuis le fichier : le dossier courant du terminal
n'a pas d'importance.

Sélectionner l'interpréteur Python 3.12 qui contient Gurobi :
`C:\Users\pret\AppData\Local\Python\pythoncore-3.12-64\python.exe`.
Dans VS Code, utiliser « Python: Select Interpreter » dans la palette de
commandes (`Ctrl+Shift+P`) si nécessaire.

Pour changer d'instance, modifier `INSTANCE_NAME` en haut de `main.py`.
Le stock de sécurité et le nombre maximal de tournées sont aussi configurables
dans ce fichier. Aucune optimisation n'est encore lancée : les contraintes
et l'objectif restent à implémenter.

## Architecture du projet

```text
Optimization/
├── README.md
├── main.py
├── src/
│   ├── __init__.py
│   ├── instance_loader.py
│   ├── model_setup.py
│   └── model_variables.py
├── scripts/
│   └── view_instance.py
└── docs/
    ├── phase_analyse_donnees.md
    └── analyse_coherence_formulation.txt
```

Les fichiers de `src/` contiennent le code réutilisable du modèle. Les fichiers
de `scripts/` servent à lancer des démonstrations ou des vérifications. Les
fichiers de `docs/` contiennent la documentation du projet.

Pour vérifier l'étape 2, qui déclare les variables de décision Gurobi :

```bash
python3 src/model_variables.py
```

Cette étape nécessite `gurobipy`, Gurobi Optimizer et une licence Gurobi
valide. Les contraintes et la fonction objectif seront ajoutées ensuite.

## 1. Instance utilisée comme exemple

Le programme `view_instance.py` utilise par défaut le fichier :

```text
data/instances/mcd/mcd-10-1-3-5-1-1.dat
```

Son contenu brut est :

```text
10 1 3 5 1
413 26  20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000
415 293 8042 6383 50000 0.01
149 421 7982 6335 50000 0.01
59 263 5103 4362 50000 0.01
172 236 9003 6926 50000 0.01
429 282 5627 5211 50000 0.01
67 135 1560 1530 50000 0.01
58 69 4534 4929 50000 0.01
11 42 10862 8167 50000 0.01
419 284 3648 3229 50000 0.01
315 370 11781 8537 50000 0.01
```

## 2. Signification de la première ligne

La première ligne contient cinq paramètres :

```text
n m comps K H
```

Dans l'exemple : `10 1 3 5 1` signifie :

| Valeur | Nom | Signification |
|---:|---|---|
| `10` | `n` | nombre de stations clientes |
| `1` | `m` | nombre de produits ou carburants |
| `3` | `comps` | nombre de compartiments par camion |
| `5` | `K` | nombre de camions |
| `1` | `H` | nombre de périodes ou jours |

Le dépôt n'est pas compté dans `n`. Dans le programme Python, il est toujours
représenté par l'indice `0`, tandis que les stations utilisent les indices
`1` à `n`.

## 3. Dépôt et capacités des camions

La deuxième ligne commence par les coordonnées du dépôt :

```text
413 26
```

Le dépôt se trouve donc au point `(413, 26)`.

Les valeurs qui suivent sont les capacités des compartiments. Dans l'exemple,
il y a `5 x 3 = 15` valeurs :

```text
20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000 20000
```

Cela signifie que chaque camion possède trois compartiments de capacité
`20 000`.

Dans le contexte du transport de carburant, ces capacités sont généralement
interprétées en litres. Cependant, le fichier `.dat` ne stocke pas explicitement
l'unité : il manipule seulement des valeurs numériques. L'unité officielle doit
donc être confirmée dans l'énoncé du projet ou la documentation du jeu de
données.

Dans Python, ces valeurs sont accessibles avec :

```python
data.compartment_sizes[camion][compartiment]
```

Les indices des camions et compartiments commencent à `1` pour rester
compatibles avec le code C++ fourni.

## 4. Structure d'une ligne de station

Dans cet exemple, il n'y a qu'un produit et qu'une période. Une ligne de
station contient donc :

```text
X Y Stock_initial Demande Capacité_cuve Coût_stockage
```

Par exemple :

```text
415 293 8042 6383 50000 0.01
```

signifie :

| Valeur | Signification |
|---:|---|
| `415 293` | coordonnées de la station |
| `8042` | stock initial |
| `6383` | demande pendant la période 1 |
| `50000` | capacité maximale de la cuve |
| `0.01` | coût de stockage unitaire |

Pour plusieurs produits ou plusieurs périodes, la structure devient :

```text
X_i Y_i
I0_i,1 ... I0_i,m
r_i,1,1 ... r_i,1,H
r_i,2,1 ... r_i,2,H
...
r_i,m,1 ... r_i,m,H
U_i,1 h_i,1
U_i,2 h_i,2
...
U_i,m h_i,m
```

Les demandes sont donc lues produit par produit, puis période par période.

Dans Python :

```python
data.coordinates[i]
data.initial_inventory[i][product]
data.demand[i][product][period]
data.tank_capacity[i][product]
data.holding_cost[i][product]
```

## 5. Distances

Les coordonnées servent à calculer les distances entre le dépôt et les
stations, ainsi qu'entre les stations.

La distance utilisée est la distance euclidienne arrondie à l'entier le plus
proche :

```text
d(i,j) = arrondi(sqrt((x_i-x_j)^2 + (y_i-y_j)^2))
```

Dans Python, la matrice est accessible avec `data.distances[i][j]`.

## 6. Chargement d'une instance en Python

```python
from src.instance_loader import load_instance

data = load_instance(
    "data/instances/mcd/mcd-10-1-3-5-1-1.dat",
    option=0,
)

print("Stations :", data.n)
print("Produits :", data.m)
print("Camions :", data.k)
print("Périodes :", data.h)
print("Coordonnées de la station 1 :", data.coordinates[1])
print("Stock initial station 1 :", data.initial_inventory[1][1])
print("Demande station 1, produit 1, jour 1 :", data.demand[1][1][1])
```

## 7. Options de réordonnancement

Le code Python reprend les options de la fonction C++ `loadInstance` :

| Option | Ordre des stations |
|---:|---|
| `0` | ordre original du fichier |
| `1` | demande totale décroissante, tous produits et jours |
| `2` | demande totale décroissante du produit 1 |
| `3` | distance au dépôt croissante |
| `4` | distance au dépôt décroissante |

Exemple :

```python
data = load_instance("/chemin/vers/instance.dat", option=3)
```

## 8. Affichage direct d'une instance

Depuis le dossier parent du projet, avec Python 3.10 ou plus récent :

```bash
cd "/Users/mana/Documents/ChatGPT/Optimization"
python3 scripts/view_instance.py
```

Le programme affiche les dimensions de l'instance, les capacités des
compartiments, les coordonnées, les distances, les stocks, les demandes, les
capacités des cuves, les coûts de stockage et la matrice complète des
distances.

Pour afficher une autre instance, modifier `DEFAULT_INSTANCE` dans
`scripts/view_instance.py` :

```python
DEFAULT_INSTANCE = Path(
    "data/instances/mcd/mcd-10-1-3-5-1-1.dat"
)
```

## 9. Toy example

On peut vérifier le fonctionnement du modèle avec un dépôt, deux stations,
deux jours, deux carburants `A` et `B`, et un camion composé de deux
compartiments de capacités `10` et `8`.

Une livraison possible le jour 1 est :

- compartiment 1 : `8 A` ;
- compartiment 2 : `5 B` ;
- station 1 : `5 A + 3 B` ;
- station 2 : `3 A + 2 B`.

Les contrôles à effectuer sont :

1. chaque chargement respecte la capacité de son compartiment ;
2. chaque station reçoit au moins sa demande ;
3. le stock après livraison ne dépasse pas la capacité de la cuve ;
4. le stock après consommation reste cohérent pour la période suivante ;
5. un compartiment ne mélange pas plusieurs produits.

Ce toy example permet de comprendre les contraintes avant d'implémenter le
solveur d'optimisation.
