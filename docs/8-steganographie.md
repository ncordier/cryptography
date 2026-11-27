# 8. Stéganographie (watermarking)

> Équivalent de `15.txt` et `14.rtf` du projet original.

Ce programme est un exemple de stéganographie. C'est-à-dire que l'on cache une
information à un endroit où l'on ne s'attend pas à ce qu'elle soit dissimulée.
Les Romains se servaient par exemple d'écrire des messages sur le crâne de leurs
esclaves qu'ils envoyaient ensuite porter le message une fois leurs cheveux
repoussés.

En informatique, on appelle cela du tatouage ou *watermarking*. Ce programme
utilise **deux bits par octet** pour cacher le texte, ce qui ne provoque qu'une
très faible modification de l'image, totalement invisible à l'œil nu.

Le problème, c'est que si l'image est imprimée puis scannée, rééchantillonnée
ou compressée dans un autre format, les informations sont perdues.

> Note du projet original (14.rtf) : le code de stéganographie n'était pas
> distribué dans les listings publics. Ici, il est intégralement porté en
> Python dans `cryptage.steganographie`.

## Module Python

`cryptage.steganographie` — `cacher(image.bmp, message, sortie.bmp)` et
`extraire(image.bmp)`. Format : 4 octets de longueur (little-endian) puis le
message UTF-8, chaque octet découpé en 4 groupes de 2 bits stockés dans les
2 LSB d'octets de pixels consécutifs.

## Utilisation

```bash
cryptage stegano-cacher ballon.bmp "message caché" -o sortie.bmp
cryptage stegano-extraire sortie.bmp
```
