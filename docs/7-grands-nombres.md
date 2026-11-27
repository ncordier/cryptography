# 7. Arithmétique sur grands nombres

> Équivalent de `13.txt` et `12.rtf` du projet original.

Les programmes de cryptage perfectionnés doivent manipuler des nombres de très
grande longueur. Cette tâche n'est pas aisée sur un ordinateur personnel qui
n'est pas programmé pour manipuler des nombres de plus de 20 chiffres, alors
que les besoins d'une application de cryptage peuvent être de plusieurs
centaines de chiffres (environ 200 chiffres actuellement pour la clef N = P×Q
en vue d'une sécurité intéressante).

Le programme original (VB6) permettait d'effectuer des opérations arithmétiques
élémentaires sur des nombres de plusieurs milliers de chiffres grâce à une
bibliothèque custom manipulant des tableaux d'octets (`Byte` / `DByte`).

**En Python, les `int` natifs sont en précision arbitraire** : aucune
bibliothèque externe n'est nécessaire. Le module `cryptage.grands_nombres`
fournit néanmoins des fonctions explicites (`add`, `sous`, `mult`,
`div_entiere`, `modulo`) pour rester fidèle à l'esprit du projet.

## Utilisation

```bash
cryptage grands-nombres
```
