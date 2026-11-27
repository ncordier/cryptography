"""Code secret par mot — chiffre de César amélioré.

Portage fidèle de 2.rtf (Code / DeCoDe / VeRif1 / VeRif2 / VeRif3 en VB6).

Principe (3.txt) : chaque mot est codé par un chiffre de César dont le
decalage est tire au hasard. Le premier caractere du mot code indique le
decalage (A=1 … Z=26). Une lettre leurre est inseree a une position
aleatoire, indiquee par le dernier caractere du mot code.
"""

from __future__ import annotations

import random
import re
import unicodedata


def _normaliser(texte: str) -> str:
    """Équivalent de VeRif1 : majuscules, suppression des accents et ponctuation."""
    # Décomposer les caractères accentués et ne garder que la base
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    texte = texte.upper()
    # Remplacer la ponctuation par des espaces
    texte = re.sub(r"[^A-Z ]", " ", texte)
    return texte


def _nettoyer_espaces(texte: str) -> str:
    """Équivalent de VeRif2 : supprime les espaces doubles, début et fin."""
    return re.sub(r" +", " ", texte).strip()


def _preparer(texte: str) -> list[str]:
    """Équivalent de VeRif1 + VeRif2 + VeRif3 : retourne la liste des mots."""
    texte = _normaliser(texte)
    texte = _nettoyer_espaces(texte)
    if not texte:
        return []
    return texte.split(" ")


def coder(texte: str, rng: random.Random | None = None) -> str:
    """Code le texte mot par mot (fonction Code de 2.rtf).

    Pour chaque mot :
      - dec = décalage aléatoire dans [1, 25]
      - chaque lettre est décalée de `dec` (mod 26, A=65…Z=90)
      - nl2[0] = chr(dec + 64)   → indique le décalage
      - une lettre leurre est insérée à une position po aléatoire
      - nl2[-1] = chr(po + 64)   → indique la position du leurre
    """
    r = rng or random.Random()
    mots = _preparer(texte)
    if not mots:
        return "ERREUR"

    resultat: list[str] = []
    for mot in mots:
        nc = len(mot)
        dec = r.randint(1, 25)

        # Chiffre de César sur le mot
        nl = []
        for ch in mot:
            c = ord(ch) + dec
            if c > 90:
                c -= 26
            nl.append(chr(c))

        # Construction du mot codé avec en-tête (dec) + leurre + position
        # VB6 : po = Int(Rnd * (nc + 1)) + 2  →  po ∈ [2, nc+2]
        po = r.randint(2, nc + 2)  # position du leurre dans nl2 (1-based)
        leurre = chr(r.randint(0, 25) + 65)

        nl2 = [chr(dec + 64)]  # premier caractère = décalage
        g = 0
        for i in range(2, nc + 3):  # positions 2 à nc+2
            if i == po:
                nl2.append(leurre)
            else:
                nl2.append(nl[g])
                g += 1
        nl2.append(chr(po + 64))  # dernier caractère = position du leurre

        resultat.append("".join(nl2))

    return " ".join(resultat).strip()


def decoder(texte: str) -> str:
    """Décode le texte mot par mot (fonction DeCoDe de 2.rtf)."""
    mots = _preparer(texte)
    if not mots:
        return "ERREUR"

    resultat: list[str] = []
    for mot in mots:
        nc = len(mot)
        if nc < 3:
            resultat.append("ERREUR")
            continue

        po = ord(mot[-1]) - 64  # position du leurre
        if po < 2 or po > (nc - 1):
            resultat.append("ERREUR")
            continue

        # Retirer le leurre
        sans_leurre = ""
        for i in range(nc - 1):  # enlever le dernier caractère (position)
            if i + 1 != po:
                sans_leurre += mot[i]

        dec = ord(sans_leurre[0]) - 64  # décalage
        # Décoder le reste (à partir du 2e caractère de sans_leurre)
        clair = ""
        for i in range(1, len(sans_leurre)):
            c = ord(sans_leurre[i]) - dec
            if c < 65:
                c += 26
            clair += chr(c)

        resultat.append(clair)

    return " ".join(resultat).strip()
