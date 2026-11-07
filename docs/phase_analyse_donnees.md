# Phase 2 - Analyse des données d'instances

## Structure des fichiers `.dat`

La première ligne contient `n m comps K H` : nombre de stations clientes,
produits, compartiments par camion, camions et périodes.

Après l'en-tête, on lit les coordonnées du dépôt, puis `K` lignes de `comps`
capacités de compartiments. Chaque station est ensuite décrite par :

```text
x_i y_i
I0_i,1 ... I0_i,m
r_i,1,1 ... r_i,1,H
...
r_i,m,1 ... r_i,m,H
U_i,1 h_i,1
...
U_i,m h_i,m
```

Les demandes sont donc regroupées par produit, puis par jour. `U` est la
capacité de la cuve et `h` le coût lu comme un nombre réel. Le dépôt est
l'indice `0`; les stations sont les indices `1..n`.

Le chargeur Python `instance_loader.py` expose ces données sous la forme :

| Donnée | Structure |
|---|---|
| Coordonnées | `coordinates[i] = (x, y)` |
| Stock initial | `initial_inventory[i][product]` |
| Demande | `demand[i][product][period]` |
| Capacité cuve | `tank_capacity[i][product]` |
| Coût de stockage | `holding_cost[i][product]` |
| Compartiments | `compartment_sizes[vehicle][compartment]` |
| Distances | `distances[i][j]`, euclidienne arrondie |

## Options reprises du C++

`load_instance(path, option)` accepte les mêmes options :

- `0` : ordre original du fichier ;
- `1` : demande totale décroissante, tous produits et jours ;
- `2` : demande du produit 1 décroissante ;
- `3` : distance au dépôt croissante ;
- `4` : distance au dépôt décroissante.

Le tri réindexe les stations et la matrice des distances sans modifier les
valeurs physiques. La version Python initialise aussi correctement les
distances impliquant le dépôt, ce qui évite le problème du tableau C++ non
recopié pour `option == 0`.

## Toy example manuel

On prend un dépôt `0` en `(0,0)`, deux stations `1=(3,4)` et `2=(6,8)`, deux
jours, deux carburants `A/B`, et un camion aux compartiments `10` et `8`.

| Station | Stock initial A/B | Demande J1 A/B | Demande J2 A/B | Capacité cuve A/B |
|---|---:|---:|---:|---:|
| 1 | 2 / 1 | 5 / 3 | 4 / 2 | 12 / 10 |
| 2 | 1 / 2 | 3 / 2 | 2 / 4 | 10 / 10 |

Distances : `d(0,1)=5`, `d(0,2)=10`, `d(1,2)=5`.

### Livraisons : deux tournées par jour

Pour cet exemple, fixer `MAX_ROUTES_PER_VEHICLE = 2` et `SECURITY_STOCK = 0`.
Chaque compartiment est réservé à un seul couple station-produit par tournée.

| Jour | Tournée | Parcours | Compartiment 1 (capacité 10) | Compartiment 2 (capacité 8) |
|---|---|---|---|---|
| 1 | 1 | 0 -> 1 -> 0 | 5 A pour la station 1 | 3 B pour la station 1 |
| 1 | 2 | 0 -> 2 -> 0 | 3 A pour la station 2 | 2 B pour la station 2 |
| 2 | 1 | 0 -> 1 -> 0 | 4 A pour la station 1 | 2 B pour la station 1 |
| 2 | 2 | 0 -> 2 -> 0 | 2 A pour la station 2 | 4 B pour la station 2 |

Les compartiments sont rechargés au dépôt entre les tournées. Aucun compartiment
n'est partagé entre stations pendant une tournée. Tous les chargements respectent
les capacités 10 et 8 ; le remplissage partiel est autorisé.

Avant consommation, les stocks A/B valent au jour 1 : 7/4 pour la station 1 et
4/4 pour la station 2 ; au jour 2 : 6/3 et 3/6. Ils respectent les capacités des
cuves. Après consommation, les stocks restent chaque jour 2/1 et 1/2.
Les demandes sont couvertes par le stock disponible et les livraisons : il n'est
pas nécessaire, en général, de livrer autant que la demande de chaque période.

Cet exemple illustre un plan réalisable, sans prétendre minimiser la distance.
Il est vérifié par `test_documented_example`. Il utilise deux tournées et ne
représente donc pas la restriction du benchmark à une tournée par camion.

## Utilisation

```python
from src.instance_loader import load_instance

data = load_instance("/chemin/vers/mcd-10-1-3-5-1-1.dat", option=0)
print(data.coordinates[1])
print(data.demand[1][1][1])
```

Ou depuis le terminal :

```bash
python src/instance_loader.py "/chemin/vers/instance.dat" --option 0
```
