"""Cryptage par générateur de nombres pseudo-aléatoires.

Portage fidèle de 6.rtf (MakeClef / Code / DeCode en VB6).

Principe (7.txt) : une clef (chaîne ou nombre) initialise un générateur
pseudo-aléatoire. La séquence produite sert à chiffrer chaque caractère
par addition modulo 256. Pour décrypter, il faut la même clef.

En Python moderne, on utilise le module `random` avec une graine
(`seed`) dérivée de la clef — conceptuellement identique au `Rnd`
de VB6 initialisé par `Rnd(clef)`.
"""

from __future__ import annotations

import hashlib
import random


def make_clef(clef: str) -> int:
    """Transforme une chaîne en graine numérique (équivalent de MakeClef, 6.rtf).

    Le VB6 faisait : Randomize Asc(...) pour chaque caractère, puis
    MakeClef = Int(Rnd * 16777214) + 1.
    Ici on dérive une graine stable via SHA-256.
    """
    h = hashlib.sha256(clef.encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big") % 16777214 + 1


def coder(message: str, clef: str | int) -> str:
    """Chiffre le message avec la clef (fonction Code de 6.rtf).

    Chaque caractère c est remplacé par chr((c + add) mod 256)
    où add est un nombre pseudo-aléatoire dans [0, 254].
    """
    if isinstance(clef, str):
        seed = make_clef(clef)
    else:
        seed = abs(int(clef))
    if seed == 0:
        return message

    rng = random.Random(seed)
    resultat = []
    for ch in message:
        car = ord(ch)
        add = rng.randint(0, 254)  # Int(Rnd * 255) en VB6
        resultat.append(chr((car + add) % 256))
    return "".join(resultat)


def decoder(message: str, clef: str | int) -> str:
    """Déchiffre le message (fonction DeCode de 6.rtf) : soustraction mod 256."""
    if isinstance(clef, str):
        seed = make_clef(clef)
    else:
        seed = abs(int(clef))
    if seed == 0:
        return message

    rng = random.Random(seed)
    resultat = []
    for ch in message:
        car = ord(ch)
        add = rng.randint(0, 254)
        resultat.append(chr((car - add + 256) % 256))
    return "".join(resultat)
