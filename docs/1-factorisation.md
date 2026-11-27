# 1. Factorisation d'entiers

> Équivalent de `1.txt` et `0.rtf` du projet original.

Pour les applications de cryptage à clefs publiques, la factorisation d'entiers
a toujours été un problème important. Toute la sécurité de ces systèmes repose
sur le fait que la clef de cryptage est un entier suffisamment grand pour ne
pas être factorisé.

Ce programme, dont l'algorithme n'est pas parfait, ne fait qu'illustrer ceci et
l'augmentation très importante du temps de calcul avec l'augmentation de la
taille des nombres à factoriser.

## Module Python

`cryptage.factorisation` — fonctions `est_premier(n)` et `factoriser(n)`.

## Utilisation

```bash
cryptage factoriser 600851475143
# → 71 x 839 x 1471 x 6857
```
