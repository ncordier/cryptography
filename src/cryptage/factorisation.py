"""Factorisation d'entiers et test de primalité.

Portage fidèle de 0.rtf (FactPre / PreMier en VB6).
L'algorithme original teste les diviseurs premiers jusqu'à sqrt(n),
avec un tableau de facteurs (valeur, exposant).
"""

from __future__ import annotations

import math


def est_premier(n: int) -> bool:
    """Renvoie True si n est premier.

    Algorithme identique à PreMier (0.rtf) : test de divisibilité
    par 2 puis par les impairs jusqu'à sqrt(n).
    """
    n = abs(n)
    if n == 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def factoriser(n: int) -> dict[int, int]:
    """Décompose n en facteurs premiers : {premier: exposant}.

    Algorithme identique à FactPre (0.rtf) : on itère sur les candidats
    premiers jusqu'à sqrt(n), en divisant n à chaque fois que possible.
    """
    n = abs(int(n))
    if n == 1:
        return {1: 1}
    if est_premier(n):
        return {n: 1}

    facteurs: dict[int, int] = {}
    # On parcourt les candidats premiers jusqu'à sqrt(n) restant
    i = 2
    while i <= math.isqrt(n):
        if est_premier(i):
            while n % i == 0:
                facteurs[i] = facteurs.get(i, 0) + 1
                n //= i
                if est_premier(n):
                    if n == i:
                        facteurs[i] = facteurs.get(i, 0) + 1
                    else:
                        facteurs[n] = facteurs.get(n, 0) + 1
                    n = 1
                    break
        i += 1
    if n > 1:
        facteurs[n] = facteurs.get(n, 0) + 1
    return facteurs


def factoriser_str(n: int) -> str:
    """Formate le résultat comme dans FactPre : 'p1^e1 x p2^e2 …'."""
    f = factoriser(n)
    if not f:
        return "ERREUR"
    parties = []
    for p in sorted(f):
        e = f[p]
        if e > 1:
            parties.append(f"{p} ^{e}")
        else:
            parties.append(str(p))
    return " x ".join(parties)
