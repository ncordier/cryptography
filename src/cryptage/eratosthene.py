"""Crible d'Ératosthène — génération de nombres premiers.

Portage fidèle de 8.rtf (GetPrime en VB6 avec BitPack.dll).
L'algorithme est le crible classique : on marque les multiples de
chaque nombre premier à partir de 3.

En Python moderne, on utilise un bytearray (équivalent du tableau de
bits de la DLL C++ BitPack) pour une efficacité mémoire optimale.
"""

from __future__ import annotations

import math


def crible(limite: int) -> list[int]:
    """Renvoie tous les nombres premiers <= limite (crible d'Ératosthène).

    Implémentation fidèle à 8.rtf : on ne stocke que les nombres impairs
    dans un tableau de bits (bytearray), comme le faisait BitPack.dll.
    """
    if limite < 2:
        return []
    # Tableau de bits pour les impairs : index i représente le nombre 2*i + 3
    taille = (limite - 3) // 2 + 1
    est_composite = bytearray(taille)  # 0 = premier potentiel, 1 = composite

    limite_crible = math.isqrt(limite)
    for i in range((limite_crible - 3) // 2 + 1):
        if not est_composite[i]:
            p = 2 * i + 3
            # Marquer les multiples de p à partir de p^2
            start = (p * p - 3) // 2
            for j in range(start, taille, p):
                est_composite[j] = 1

    premiers = [2]
    for i in range(taille):
        if not est_composite[i]:
            premiers.append(2 * i + 3)
    return premiers


def crible_vers_fichier(limite: int, chemin: str) -> int:
    """Génère les nombres premiers et les écrit dans un fichier texte.

    Équivalent de la partie 'écriture du fichier' de GetPrime (8.rtf).
    Retourne le nombre de premiers trouvés.
    """
    premiers = crible(limite)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"Nombres premiers jusqu'à {limite}.\n")
        f.write(f"Soit {len(premiers)} nombres premiers.\n\n")
        ligne = ""
        for p in premiers:
            ligne += str(p) + " "
            if len(ligne) > 80:
                f.write(ligne.strip() + "\n")
                ligne = ""
        if ligne:
            f.write(ligne.strip() + "\n")
    return len(premiers)
