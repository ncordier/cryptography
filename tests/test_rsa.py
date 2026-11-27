"""Tests pour le module RSA (10.rtf)."""

import random

import pytest
from cryptage import rsa


class TestEuler:
    def test_inverse_modulaire(self):
        # e * d ≡ 1 (mod phi)
        phi = 72  # phi(73*97) par exemple
        e = 5
        d = rsa._euler(e, phi)
        assert (e * d) % phi == 1

    def test_valeur_connue(self):
        # Pour phi=40, e=7 : 7*23 = 161 = 4*40 + 1 → d=23
        assert rsa._euler(7, 40) == 23


class TestEstPremier:
    def test_premiers(self):
        for p in [2, 3, 5, 7, 11, 97, 3167, 9973]:
            assert rsa._est_premier(p) is True

    def test_composites(self):
        for c in [1, 4, 9, 15, 3173, 9999]:  # 3173 = 19 × 167
            assert rsa._est_premier(c) is False


class TestMultMod:
    def test_puissance_modulaire(self):
        assert rsa._mult_mod(2, 10, 1000) == 24  # 2^10 = 1024, 1024 mod 1000 = 24

    def test_identite(self):
        assert rsa._mult_mod(5, 0, 100) == 1


class TestGenererCles:
    def test_cles_valides(self):
        rng = random.Random(42)
        cles = rsa.generer_cles(borne_inf_pq=1000, borne_sup_pq=9999, taille_min_d=0, rng=rng)
        assert rsa._est_premier(cles.p)
        assert rsa._est_premier(cles.q)
        assert cles.n == cles.p * cles.q
        assert cles.phi == (cles.p - 1) * (cles.q - 1)
        assert (cles.e * cles.d) % cles.phi == 1

    def test_deterministe_avec_graine(self):
        rng1 = random.Random(7)
        rng2 = random.Random(7)
        c1 = rsa.generer_cles(borne_inf_pq=1000, borne_sup_pq=9999, taille_min_d=0, rng=rng1)
        c2 = rsa.generer_cles(borne_inf_pq=1000, borne_sup_pq=9999, taille_min_d=0, rng=rng2)
        assert c1 == c2


class TestCrypterDecrypter:
    def test_aller_retour(self):
        rng = random.Random(123)
        cles = rsa.generer_cles(borne_inf_pq=1000, borne_sup_pq=9999, taille_min_d=0, rng=rng)
        msg = "ABC"
        chiffre = rsa.crypter(msg, cles.e, cles.n)
        assert chiffre != msg
        dechiffre = rsa.decrypter(chiffre, cles.d, cles.n)
        assert dechiffre == msg

    def test_texte_vide(self):
        assert rsa.crypter("", 5, 100) == ""

    def test_format_sortie(self):
        chiffre = rsa.crypter("A", 3, 55)
        # 'A' = 65, 65^3 mod 55
        assert chiffre.endswith("+")
        assert "+" in chiffre
