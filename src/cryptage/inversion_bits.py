"""Inversion de bits — code secret par NOT logique.

Portage fidèle de 4.rtf (CoDage en VB6) : chaque octet du texte voit
tous ses bits inversés (0↔1). Le codage et le décodage sont la même
opération (NOT est involutif).
"""

from __future__ import annotations


def coder(texte: str) -> str:
    """Inverse tous les bits de chaque octet (fonction CoDage de 4.rtf).

    En VB6 : car = Not(car) sur un Byte (mod 256).
    En Python : on applique ~car & 0xFF pour rester dans [0, 255].
    """
    return "".join(chr((~ord(ch)) & 0xFF) for ch in texte)


# Le décodage est identique au codage (NOT est involutif)
decoder = coder
