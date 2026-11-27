"""Tests pour le module eratosthene (8.rtf)."""

import os
import tempfile

from cryptage import eratosthene


class TestCrible:
    def test_petits(self):
        assert eratosthene.crible(10) == [2, 3, 5, 7]

    def test_limite_2(self):
        assert eratosthene.crible(2) == [2]

    def test_limite_inferieure(self):
        assert eratosthene.crible(1) == []
        assert eratosthene.crible(0) == []

    def test_compte_100(self):
        premiers = eratosthene.crible(100)
        assert len(premiers) == 25  # il y a 25 premiers <= 100

    def test_compte_1000(self):
        premiers = eratosthene.crible(1000)
        assert len(premiers) == 168

    def test_tous_sont_premiers(self):
        from cryptage.factorisation import est_premier
        for p in eratosthene.crible(10000):
            assert est_premier(p), f"{p} n'est pas premier!"

    def test_100_millions_partiel(self):
        # Vérifie que le crible fonctionne sur une grande plage (extrait)
        premiers = eratosthene.crible(1_000_000)
        assert len(premiers) == 78498  # nombre connu de premiers <= 10^6
        assert premiers[-1] == 999983


class TestCribleFichier:
    def test_ecriture_fichier(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            chemin = f.name
        try:
            n = eratosthene.crible_vers_fichier(100, chemin)
            assert n == 25
            with open(chemin, encoding="utf-8") as f:
                contenu = f.read()
            assert "25 nombres premiers" in contenu
            assert "2" in contenu
            assert "97" in contenu
        finally:
            os.unlink(chemin)
