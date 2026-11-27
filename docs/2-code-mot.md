# 2. Code secret par mot (chiffre de César amélioré)

> Équivalent de `3.txt` et `2.rtf` du projet original.

Ce programme montre l'application d'un code secret.

La différence entre une technique de code secret et un cryptage repose sur le
fait que lorsque l'on sait comment on code, on peut décoder le message alors
qu'avec du cryptage, il faut en plus posséder une clef.

Ce code, imaginé par un ami et porté sur ordinateur, est en fait une amélioration
du chiffre de César : chaque mot est codé par un chiffre de César dont le
décalage correspond à la valeur de la première lettre. En outre, on rajoute une
dernière lettre dont la valeur indique dans le mot codé une lettre qui ne sert
à rien.

On remarque qu'un tel codage perd toute la mise en forme du message.

## Module Python

`cryptage.code_mot` — fonctions `coder(texte)` et `decoder(texte)`.

## Utilisation

```bash
cryptage code-mot "Bonjour le monde"
cryptage decode-mot "BDJQPLQWTC XSJCB DQOSRHIC"
```
