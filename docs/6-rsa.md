# 6. RSA — cryptage à clef publique

> Équivalent de `11.txt` et `10.rtf` du projet original.

Je n'expliquais pas ici le fonctionnement de ce programme, ceci étant une partie
du TPE lui-même.

Il s'agit d'un système assez proche du RSA. Pourtant, on peut constater que
lorsque ce système sert à crypter un message octet après octet, il consiste
uniquement en un cryptage par substitution ! Pour remédier à cela, il faudrait
crypter des séquences très longues d'octets nécessitant alors une énorme
capacité de calcul.

## Module Python

`cryptage.rsa` — `generer_cles()` produit un objet `ClesRSA(p, q, phi, e, d, n)` ;
`crypter(texte, e, n)` et `decrypter(texte, d, n)` chiffrent caractère par
caractère (résultats séparés par `+`, comme dans le VB6).

## Utilisation

```bash
cryptage rsa-gen --min 1000 --max 9999
cryptage rsa-crypter "ABC" --e 90388981 --n 9776201
cryptage rsa-decrypter "5175199+7458805+1760677+" --d 6036445 --n 9776201
```
