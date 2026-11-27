# Cryptage — portage Python moderne

> Portage en Python du TPE « Cryptage » réalisé en Visual Basic 6 en 2004.

---

## Installation

```bash
cd python
pip install -e .
```

Nécessite Python 3.10 ou supérieur. Aucune dépendance externe
(la stéganographie lit/écrit les BMP directement, sans Pillow).

## Lancement

```bash
cryptage --help                  # liste des commandes
python -m pytest tests/ -v       # 66 tests
```

## Les 8 démonstrations

| # | Commande CLI | Module | Concept | Doc |
|---|-------------|--------|---------|-----|
| 1 | `cryptage factoriser <n>` | `factorisation` | Factorisation + primalité | [docs/1-factorisation.md](docs/1-factorisation.md) |
| 2 | `cryptage code-mot <texte>` | `code_mot` | Code secret par mot (César amélioré) | [docs/2-code-mot.md](docs/2-code-mot.md) |
| 3 | `cryptage inverser <texte>` | `inversion_bits` | Inversion de tous les bits | [docs/3-inversion-bits.md](docs/3-inversion-bits.md) |
| 4 | `cryptage crypter <texte> --clef <clef>` | `pseudo_aleatoire` | Cryptage par générateur pseudo-aléatoire | [docs/4-pseudo-aleatoire.md](docs/4-pseudo-aleatoire.md) |
| 5 | `cryptage eratosthene <limite>` | `eratosthene` | Crible d'Ératosthène | [docs/5-eratosthene.md](docs/5-eratosthene.md) |
| 6 | `cryptage rsa-gen` / `rsa-crypter` / `rsa-decrypter` | `rsa` | RSA (clef publique) | [docs/6-rsa.md](docs/6-rsa.md) |
| 7 | `cryptage grands-nombres` | `grands_nombres` | Arithmétique multiprécision (natif Python) | [docs/7-grands-nombres.md](docs/7-grands-nombres.md) |
| 8 | `cryptage stegano-cacher` / `stegano-extraire` | `steganographie` | Stéganographie LSB dans BMP | [docs/8-steganographie.md](docs/8-steganographie.md) |

## Exemples

```bash
cryptage factoriser 600851475143
# → 71 x 839 x 1471 x 6857

cryptage code-mot "Bonjour le monde"
# → Codé : BDJQPLQWTC XSJCB DQOSRHIC  /  Décodé : BONJOUR LE MONDE

cryptage crypter "Message secret" --clef "motdepasse"
cryptage decrypter "…" --clef "motdepasse"

cryptage eratosthene 1000000
# → 78498 nombres premiers

cryptage rsa-gen --min 1000 --max 9999
cryptage rsa-crypter "ABC" --e <E> --n <N>
cryptage rsa-decrypter "…" --d <D> --n <N>

cryptage stegano-cacher ../ballon.bmp "message caché" -o sortie.bmp
cryptage stegano-extraire sortie.bmp
```

## Commentaires sur l'original et le portage

### Choix de l'original (VB6, 2004)

- **VB6 comme langage** : en 2004, c'était le langage enseigné au lycée en
  France (option informatique). Le TPE visait à illustrer des concepts de
  cryptographie, pas à écrire du code de production — VB6 suffisait amplement.
- **DLL C++ (`BitPack.dll`)** : le crible d'Ératosthène manipule des millions de
  bits. En VB6 pur, un tableau de `Boolean` aurait consommé 1 octet par bit.
  La DLL C++ offrait `BitGet`/`BitSet`/`BitClr` sur des `Byte` natifs — 8 fois
  plus compact et bien plus rapide. En Python, `bytearray` joue exactement ce
  rôle sans dépendance externe.
- **RSA avec petits nombres** : P, Q ∈ [3170, 9999] donnaient N ≈ 10⁸, calculable
  sur un `Double` VB6 (précision ~15 chiffres). C'était suffisant pour la démo
  pédagogique mais **cassable en quelques secondes** aujourd'hui. Le texte
  original (11.txt) le reconnaît : crypter octet par octet avec RSA = simple
  substitution.
- **Pas de stéganographie dans les listings** (14.rtf) : l'auteur retirait
  délibérément ce code des sources publiées, probablement pour garder un aspect
  « à découvrir » pour le TPE. Seule la description (15.txt) était fournie.
- **Distances avec la crypto moderne** : aucun de ces algorithmes n'est sûr.
  Le générateur pseudo-aléatoire (6.rtf) est cassable par analyse de fréquence
  statistique ; le « code mot » (2.rtf) perd la ponctuation ; la stéganographie
  LSB disparaît à la moindre recompression. C'est volontaire : le but était
  pédagogique, pas sécuritaire.

### Choix du portage Python

- **Un module = une démo** : chaque fichier `.rtf` original devient un module
  Python nommé explicitement (`rsa.py`, `steganographie.py`…). La correspondance
  est documentée dans [HELP.md](HELP.md).
- **Graine pseudo-aléatoire par SHA-256** : le `Rnd` de VB6 est un générateur
  linéaire congruentiel dont la graine est un `Long`. Python n'a pas ce
  générateur ; `random.Random(seed)` (Mersenne Twister) avec une graine dérivée
  de `sha256(clef)` reproduit le principe : même clef → même séquence →
  décodage possible. C'est plus robuste que le LCG original.
- **`int` natifs pour les grands nombres** : le VB6 avait besoin d'une
  bibliothèque `Byte`/`DByte` (12.rtf) car un `Double` est limité à ~15
  chiffres. Python gère nativement des entiers de taille arbitraire — aucune
  bibliothèque custom nécessaire. `grands_nombres.py` existe surtout pour
  la pédagogie (noms de fonctions explicites).
- **Stéganographie from scratch** : comme le code original n'était pas
  distribué, j'ai implémenté selon la spec de 15.txt (2 bits/octet, LSB, BMP
  24 bits non compressé). Le format est documenté dans le module. Testé et
  validé sur les vraies images du projet (`ballon.bmp`, `colline_verdoyante.bmp`).
- **CLI au lieu de GUI** : `Cryptage.exe` était une application Windows avec
  formulaires. Le portage utilise `argparse` — plus léger, scriptable, et
  testable en CI. Les 66 tests pytest remplacent les tests manuels.
- **Bornes RSA élargies par défaut** : comme expliqué dans
  [docs/6-rsa.md](docs/6-rsa.md), la contrainte `D > 10⁷` avec P, Q ∈ [3170, 9999]
  rendait la génération quasi infinie. Les constantes originales restent
  disponibles en argument.

### Ce que le portage conserve fidèlement

- Les **noms de fonctions** (`coder`/`decoder`, `crypter`/`decrypter`) et la
  **structure des algorithmes** (Euclide étendu pour RSA, crible sur impairs,
  César par mot avec leurre…).
- Le **format de sortie RSA** : nombres séparés par `+`, comme dans `enc`/`dec`
  du VB6.
- La **pédagogie** : chaque module est autonome, commenté, et référence le
  fichier `.rtf` original.

## Documentation

- [HELP.md](HELP.md) — guide de lecture du code + équivalences VB6 ↔ Python
  (équivalent du `HELP.txt` original)
- [docs/](docs/) — description détaillée de chaque démonstration
  (équivalents des `1.txt` … `15.txt` originaux)

## Structure

```
cryptography/
├── pyproject.toml
├── README.md          ← ce fichier (équivalent README.txt)
├── HELP.md            ← guide de lecture (équivalent HELP.txt)
├── docs/              ← descriptions des 8 programmes (équivalents 1.txt…15.txt)
│   ├── 1-factorisation.md
│   ├── 2-code-mot.md
│   ├── 3-inversion-bits.md
│   ├── 4-pseudo-aleatoire.md
│   ├── 5-eratosthene.md
│   ├── 6-rsa.md
│   ├── 7-grands-nombres.md
│   └── 8-steganographie.md
├── src/cryptage/
│   ├── __init__.py
│   ├── factorisation.py
│   ├── code_mot.py
│   ├── inversion_bits.py
│   ├── pseudo_aleatoire.py
│   ├── eratosthene.py
│   ├── rsa.py
│   ├── grands_nombres.py
│   ├── steganographie.py
│   └── cli.py
└── tests/             ← 66 tests (pytest)
```
