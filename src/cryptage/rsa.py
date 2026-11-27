"""RSA — cryptographie à clef publique.

Portage fidèle de 10.rtf (keyGen / Euler / PGCD / IsPrime / Mult / enc / dec).

Le chiffrement se fait caractère par caractère : chaque octet est élevé
à la puissance E modulo N. Le résultat est une suite de nombres séparés
par '+' (comme dans le VB6 original).

Constantes originales du VB6 (10.rtf) :
    PQ_UP = 9999, PQ_LW = 3170          (plage de P et Q)
    N_UP  = 99999999, N_LW = 10000000   (plage de E)
    KEY_LOWER_LIMIT = 10000000          (D doit dépasser cette valeur)
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

# Constantes originales VB6 (10.rtf)
PQ_UP_ORIG = 9999
PQ_LW_ORIG = 3170
N_UP_ORIG = 99_999_999
N_LW_ORIG = 10_000_000
KEY_LOWER_LIMIT_ORIG = 10_000_000


@dataclass
class ClesRSA:
    """Ensemble de clefs RSA (équivalent des variables k1…k6 de 10.rtf)."""
    p: int          # k1 — premier facteur
    q: int          # k2 — second facteur
    phi: int        # k3 — (P-1)*(Q-1)
    e: int          # k4 — clef publique de cryptage
    d: int          # k5 — clef privée de décryptage
    n: int          # k6 — module N = P*Q

    @property
    def clef_publique(self) -> tuple[int, int]:
        return (self.e, self.n)

    @property
    def clef_privee(self) -> tuple[int, int]:
        return (self.d, self.n)


def _est_premier(n: int) -> bool:
    """Test de primalité (IsPrime de 10.rtf) : divisibilité jusqu'à sqrt(n)."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def _euler(e: int, phi: int) -> int:
    """Renvoie x tel que x*e ≡ 1 (mod phi) — algorithme d'Euclide étendu.

    Algorithme identique à Euler (10.rtf) : itérations de l'algorithme
    d'Euclide jusqu'à v3 = 0, puis ajustement positif.
    """
    u1, u2, u3 = 1, 0, phi
    v1, v2, v3 = 0, 1, e
    while v3 != 0:
        q = u3 // v3
        u1, u2, u3, v1, v2, v3 = v1, v2, v3, u1 - q * v1, u2 - q * v2, u3 - q * v3
    inverse = u2
    if inverse < 0:
        inverse += phi
    return inverse


def _choisir_e(phi: int, rng: random.Random,
               borne_inf: int = N_LW_ORIG, borne_sup: int = N_UP_ORIG) -> int:
    """Choisit E premier dans [borne_inf, borne_sup], copremier avec phi.

    Fidèle à PGCD (10.rtf) : le VB6 tirait nE aléatoirement dans
    [10^7, 10^8] et acceptait si nE était premier et ne divisait pas phi
    (vérifié via nPHI Mod nE <> 0, sachant que x Mod nE = x quand x < nE).
    """
    while True:
        e = rng.randint(borne_inf, borne_sup)
        if _est_premier(e) and math.gcd(e, phi) == 1:
            return e


def _mult_mod(x: int, p: int, m: int) -> int:
    """Élève x à la puissance p modulo m (fonction Mult de 10.rtf).

    Le VB6 utilisait une boucle square-and-multiply manuelle ; ici on
    délègue à pow() natif, sémantiquement identique.
    """
    return pow(x, p, m)


def generer_cles(
    borne_inf_pq: int = 10_000,
    borne_sup_pq: int = 99_999,
    taille_min_d: int = KEY_LOWER_LIMIT_ORIG,
    rng: random.Random | None = None,
) -> ClesRSA:
    """Génère un jeu de clefs RSA (keyGen de 10.rtf).

    Tire P et Q aléatoirement dans [borne_inf_pq, borne_sup_pq] jusqu'à
    obtenir deux nombres premiers, calcule N, phi, choisit E premier
    copremier avec phi, puis D = euler(E, phi). Répète tant que
    D < taille_min_d.

    Note : les constantes originales VB6 (P,Q ∈ [3170, 9999]) donnaient
    phi ≈ 10^7, rendant la condition D > 10^7 quasi impossible. Les
    bornes par défaut sont élargies pour un usage moderne ; passez
    borne_inf_pq=3170, borne_sup_pq=9999, taille_min_d=0 pour le
    comportement historique exact.
    """
    r = rng or random.Random()
    while True:
        while True:
            p = r.randint(borne_inf_pq, borne_sup_pq)
            q = r.randint(borne_inf_pq, borne_sup_pq)
            if _est_premier(p) and _est_premier(q) and p != q:
                break
        n = p * q
        phi = (p - 1) * (q - 1)
        e = _choisir_e(phi, r)
        d = _euler(e, phi)
        if d > taille_min_d:
            return ClesRSA(p=p, q=q, phi=phi, e=e, d=d, n=n)


def crypter(texte: str, e: int, n: int) -> str:
    """Chiffre le texte caractère par caractère (fonction enc de 10.rtf).

    Chaque octet est élevé à la puissance E modulo N. Les résultats
    sont séparés par '+' et la chaîne se termine par '+'.
    """
    if not texte:
        return ""
    return "+".join(str(_mult_mod(ord(ch), e, n)) for ch in texte) + "+"


def decrypter(texte_chiffre: str, d: int, n: int) -> str:
    """Déchiffre le texte (fonction dec de 10.rtf).

    Le texte chiffré est une suite de nombres séparés par '+'.
    """
    tokens = [t for t in texte_chiffre.split("+") if t.strip()]
    return "".join(chr(_mult_mod(int(t), d, n)) for t in tokens)
