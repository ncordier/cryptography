# 4. Cryptage par générateur pseudo-aléatoire

> Équivalent de `7.txt` et `6.rtf` du projet original.

Voici le premier vrai système de cryptage : une clef entrée par l'utilisateur
sert à initialiser un générateur de nombres pseudo-aléatoires. La séquence de
nombres que ce générateur va ensuite produire sert à crypter le message. Pour
le décrypter, il faut connaître la valeur qui initialise le générateur. La
technique qui a été utilisée pour crypter n'est plus une information suffisante.

On remarque que la sécurité d'un tel système est très faible et que pour
l'augmenter, il aurait été possible d'utiliser comme clef la séquence de
nombres permettant un cryptage (il s'agit alors de l'algorithme du « masque
jetable »). Mais ce nombre est bien plus long, donc aussi plus long à
transmettre que le seul nombre servant à initialiser le générateur de nombres
pseudo-aléatoires.

## Module Python

`cryptage.pseudo_aleatoire` — fonctions `make_clef(clef)`, `coder(msg, clef)`
et `decoder(msg, clef)`. La clef (chaîne) est hachée en SHA-256 pour produire
une graine déterministe du générateur `random.Random`.

## Utilisation

```bash
cryptage crypter "Message secret" --clef "mon-mot-de-passe"
cryptage decrypter "…" --clef "mon-mot-de-passe"
```
