# Aide — lire le code Python du projet

> Équivalent de `HELP.txt` du projet original, adapté à Python.

Ce petit texte aide à la compréhension du code. Il ne s'agit pas d'un cours de
programmation, plutôt d'informations servant à la compréhension pour des
personnes qui sauraient programmer dans un autre langage.

## Conventions du projet

- Chaque démonstration est un **module** dans `src/cryptage/` :
  `factorisation.py`, `code_mot.py`, `inversion_bits.py`, `pseudo_aleatoire.py`,
  `eratosthene.py`, `rsa.py`, `grands_nombres.py`, `steganographie.py`.
- Chaque module expose des fonctions publiques nommées comme dans le VB6
  original : `coder`/`decoder` (ou `crypter`/`decrypter`), etc.
- Les fonctions privées ou internes sont préfixées par `_` (ex: `_est_premier`,
  `_euler`, `_mult_mod` dans `rsa.py`).
- Les commentaires dans le code font référence au fichier `.rtf` original
  correspondant (ex: « Portage fidèle de 10.rtf »).

## Python vs VB6 — équivalences rapides

| VB6 (original) | Python (portage) |
|----------------|------------------|
| `Dim x As Integer` | `x = 0` (typage dynamique) |
| `Dim t() As String` + `ReDim` | `liste = []` / `liste.append(...)` |
| `x = y` (affectation) | `x = y` (identique) |
| `x \ y` (division entière) | `x // y` |
| `x Mod y` | `x % y` |
| `x ^ y` (puissance) | `x ** y` ou `pow(x, y, m)` |
| `Sqr(x)` | `math.isqrt(x)` ou `math.sqrt(x)` |
| `Asc(c)` / `Chr$(n)` | `ord(c)` / `chr(n)` |
| `Mid$(s, i, n)` | `s[i-1:i-1+n]` |
| `Len(s)` | `len(s)` |
| `UCase$(s)` / `LCase$(s)` | `s.upper()` / `s.lower()` |
| `Split(s, " ")` | `s.split(" ")` |
| `Join(t, " ")` | `" ".join(liste)` |
| `GoTo label` | boucles `while` / `for` structurées |
| `Rnd` / `Randomize` | `random.Random(seed)` |
| `DoEvents` | pas nécessaire (pas d'UI bloquante en CLI) |

## Correspondance fichiers

| Fichier original | Module Python | Documentation |
|-----------------|---------------|---------------|
| `0.rtf` | `factorisation.py` | `docs/1-factorisation.md` |
| `2.rtf` | `code_mot.py` | `docs/2-code-mot.md` |
| `4.rtf` | `inversion_bits.py` | `docs/3-inversion-bits.md` |
| `6.rtf` | `pseudo_aleatoire.py` | `docs/4-pseudo-aleatoire.md` |
| `8.rtf` | `eratosthene.py` | `docs/5-eratosthene.md` |
| `10.rtf` | `rsa.py` | `docs/6-rsa.md` |
| `12.rtf` | `grands_nombres.py` | `docs/7-grands-nombres.md` |
| `14.rtf` / `15.txt` | `steganographie.py` | `docs/8-steganographie.md` |
| `README.txt` | `README.md` | — |
| `HELP.txt` | ce fichier | — |

## Auteur original

Tous les programmes du projet original ont été écrits en Visual Basic 6 par
**Mathias Ke.** (2004), avec des corrections de Nicolas Co. Ce portage
Python conserve la même structure pédagogique et les mêmes algorithmes.
