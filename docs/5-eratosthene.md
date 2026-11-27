# 5. Crible d'Ératosthène

> Équivalent de `9.txt` et `8.rtf` du projet original.

Pour les systèmes de cryptage à clefs publiques, nous avons vu qu'il était très
important d'utiliser de grands nombres premiers.

Ce programme permet grâce à un crible d'Ératosthène (méthode très peu
performante pour l'informatique mais qui nous suffit pour cet exposé) de créer
une liste de nombres premiers jusqu'à un ordre de grandeur de cent millions.

Dans le projet VB6 original, la manipulation des bits était déléguée à une DLL
C++ (`BitPack.dll`) pour la vitesse. En Python, un `bytearray` joue exactement
ce rôle.

## Module Python

`cryptage.eratosthene` — fonctions `crible(limite)` et
`crible_vers_fichier(limite, chemin)`.

## Utilisation

```bash
cryptage eratosthene 1000000
cryptage eratosthene 100000000 --fichier primes.txt
```
