"""Tests pour le module factorisation (0.rtf)."""

import pytest
from cryptage import factorisation


class TestEstPremier:
    def test_1_non_premier(self):
        assert factorisation.est_premier(1) is False

    def test_2_premier(self):
        assert factorisation.est_premier(2) is True

    def test_nombres_premiers(self):
        for p in [3, 5, 7, 11, 13, 97, 7919, 104729]:
            assert factorisation.est_premier(p) is True, f"{p} devrait être premier"

    def test_nombres_composites(self):
        for c in [4, 6, 9, 15, 21, 100, 7917, 104727]:
            assert factorisation.est_premier(c) is False, f"{c} ne devrait pas être premier"

    def test_grand_premier(self):
        assert factorisation.est_premier(1000003) is True

    def test_negatif(self):
        assert factorisation.est_premier(-7) is True  # abs() dans l'algo


class TestFactoriser:
    def test_1(self):
        assert factorisation.factoriser(1) == {1: 1}

    def test_premier(self):
        assert factorisation.factoriser(13) == {13: 1}

    def test_puissance_de_2(self):
        assert factorisation.factoriser(1024) == {2: 10}

    def test_composite(self):
        assert factorisation.factoriser(60) == {2: 2, 3: 1, 5: 1}

    def test_grand_nombre(self):
        f = factorisation.factoriser(600851475143)
        # 600851475143 = 71 × 839 × 1471 × 6857
        assert f == {71: 1, 839: 1, 1471: 1, 6857: 1}

    def test_verification_produit(self):
        for n in [2, 12, 100, 360, 1001, 123456]:
            f = factorisation.factoriser(n)
            produit = 1
            for p, e in f.items():
                produit *= p ** e
            assert produit == n, f"factoriser({n}) ne redonne pas {n}"


class TestFactoriserStr:
    def test_format_simple(self):
        assert factorisation.factoriser_str(13) == "13"

    def test_format_puissance(self):
        assert factorisation.factoriser_str(8) == "2 ^3"

    def test_format_multiple(self):
        s = factorisation.factoriser_str(60)
        assert "2 ^2" in s
        assert "3" in s
        assert "5" in s
        assert " x " in s
