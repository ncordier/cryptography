# 3. Inversion de bits

> Équivalent de `5.txt` et `4.rtf` du projet original.

Ce programme est un exemple de code secret utilisant la puissance de
l'informatique.

Dans le message, chaque bit d'information est inversé : un 0 devient un 1
et un 1 devient un 0.

Même si la connaissance du code suffit à le casser, le système peut conserver
la mise en forme du message.

## Module Python

`cryptage.inversion_bits` — fonction `coder(texte)` (le décodage est identique,
`NOT` étant involutif).

## Utilisation

```bash
cryptage inverser "ABC"
```
