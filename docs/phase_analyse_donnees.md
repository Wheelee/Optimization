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

### Livraison du jour 1

Le camion charge `8 A` dans le compartiment 1 et `5 B` dans le compartiment
2. Il suit `0 -> 1 -> 2 -> 0` et livre :

- station 1 : `5 A + 3 B` ;
- station 2 : `3 A + 2 B`.

Vérifications :

1. Les compartiments respectent `8 <= 10` et `5 <= 8`.
2. Les livraisons égalent exactement les demandes du jour 1.
3. Après livraison, les stocks sont `7 A / 4 B` à la station 1 et `4 A / 4 B`
   à la station 2, sous les capacités des cuves.
4. Après consommation, il reste `2 A / 1 B` à la station 1 et `1 A / 2 B` à la
   station 2.
5. Chaque compartiment transporte un seul produit : les volumes A et B sont
   suivis séparément.

Pour le jour 2, le camion peut charger `6 A` et `6 B`, puis livrer `4 A + 2 B`
à la station 1 et `2 A + 4 B` à la station 2.

## Utilisation

```python
from instance_loader import load_instance

data = load_instance("/chemin/vers/mcd-10-1-3-5-1-1.dat", option=0)
print(data.coordinates[1])
print(data.demand[1][1][1])
```

Ou depuis le terminal :

```bash
python instance_loader.py "/chemin/vers/instance.dat" --option 0
```
