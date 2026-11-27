"""Arithmétique sur grands nombres.

Portage de 12.rtf : en VB6, il fallait une bibliothèque custom (Byte/DByte)
pour manipuler des nombres de milliers de chiffres. En Python, les `int`
natifs ont une précision arbitraire — aucune bibliothèque externe n'est
nécessaire.

Ce module fournit néanmoins des fonctions explicites pour rester fidèle
à l'esprit du projet original.
"""

from __future__ import annotations


def add(a: int, b: int) -> int:
    """Addition de deux grands entiers (DByteAdd de 12.rtf)."""
    return a + b


def sous(a: int, b: int) -> int:
    """Soustraction (DByteSou de 12.rtf)."""
    return a - b


def mult(a: int, b: int) -> int:
    """Multiplication (DByteMul de 12.rtf)."""
    return a * b


def div_entiere(a: int, b: int) -> int:
    """Division entière (DByteIntDiv de 12.rtf)."""
    return a // b


def modulo(a: int, b: int) -> int:
    """Reste de la division (ByteMod de 12.rtf)."""
    return a % b


def demo() -> dict[str, str]:
    """Démonstration avec des nombres de 1000 chiffres."""
    a = int("9" * 1000)
    b = int("7" * 1000)
    return {
        "a + b (10 premiers chiffres)": str(add(a, b))[:10] + "…",
        "a * b (10 premiers chiffres)": str(mult(a, b))[:10] + "…",
        "a // b": str(div_entiere(a, b)),
        "a mod b (10 derniers chiffres)": "…" + str(modulo(a, b))[-10:],
    }
