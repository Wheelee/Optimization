# Instances du problème 1

Les 670 fichiers `.dat` du benchmark Multi-Compartment Delivery sont dans
`instances/mcd/`. L'archive téléchargée a été supprimée après vérification
que les 670 fichiers extraits étaient identiques à ceux de l'archive.
Elle n'est pas nécessaire pour exécuter le code.

- Source indiquée dans le sujet : https://www.leandro-coelho.com/instances/multi-compartment-delivery/
- Archive : https://www.leandro-coelho.com/wp-content/uploads/2013/08/Archive.zip
- Téléchargement : 7 novembre 2026.
- SHA-256 de l'archive : `8115abd34de19837e96e8cc64c789925f9b95d59eebabfaa0d6c888fe5c721d0`.

Les fichiers originaux sont conservés sans modification. Ils couvrent 10, 20,
30, 40 ou 50 stations, 1 à 3 produits, 3 à 5 compartiments par camion et
des horizons de 1, 3 ou 5 périodes. Les 670 fichiers ont été chargés avec
`prepare_model_data` et ont passé les contrôles de base de `validate_instance`
sous Python 3.12. Cela ne constitue pas une vérification de faisabilité du MILP.

Le sujet demande d'abord d'adapter le problème 1 à ce benchmark, notamment
avec une seule tournée par camion et par période. Le stock de sécurité et
le nombre maximal de tournées ne sont pas fournis dans ces fichiers ; le code
utilise respectivement 0 et 1 par défaut. Ces choix et les autres hypothèses
du benchmark devront être explicités lors de la formulation.

Exemples pour commencer :

- `mcd-10-1-3-5-1-1.dat` : 10 stations, 1 produit, 1 période ;
- `mcd-10-1-3-5-3-1.dat` : 10 stations, 1 produit, 3 périodes.

Depuis le dossier `Optimization`, avec Python 3.10 ou plus récent :

```sh
python scripts/view_instance.py
python src/model_setup.py
python src/instance_loader.py data/instances/mcd/mcd-10-1-3-5-3-1.dat
```

La déclaration des variables dans `src/model_variables.py` nécessite aussi
Gurobi et son API Python. Aucune résolution n'est encore implémentée.
