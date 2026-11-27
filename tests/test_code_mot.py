"""Tests pour le module code_mot (2.rtf) — César amélioré par mot."""

import random

import pytest
from cryptage import code_mot


class TestNormalisation:
    def test_majuscules(self):
        assert code_mot._normaliser("Bonjour") == "BONJOUR"

    def test_accents_supprimes(self):
        assert code_mot._normaliser("éléphant") == "ELEPHANT"

    def test_ponctuation_remplacee(self):
        assert code_mot._normaliser("Bonjour, monde!") == "BONJOUR  MONDE "

    def test_espaces_multiples(self):
        assert code_mot._nettoyer_espaces("A   B  C") == "A B C"


class TestCoderDecoder:
    def test_aller_retour(self):
        rng = random.Random(42)
        texte = "Bonjour le monde"
        code = code_mot.coder(texte, rng=rng)
        decode = code_mot.decoder(code)
        assert decode == "BONJOUR LE MONDE"

    def test_texte_vide(self):
        assert code_mot.coder("") == "ERREUR"
        assert code_mot.decoder("") == "ERREUR"

    def test_un_mot(self):
        rng = random.Random(123)
        code = code_mot.coder("HELLO", rng=rng)
        assert code_mot.decoder(code) == "HELLO"

    def test_plusieurs_mots(self):
        rng = random.Random(7)
        texte = "Le chat dort sur le tapis"
        code = code_mot.coder(texte, rng=rng)
        # Le codage ajoute 3 caractères par mot (en-tête + leurre + position)
        mots = texte.upper().split()
        mots_codes = code.split()
        assert len(mots_codes) == len(mots)
        for orig, mc in zip(mots, mots_codes):
            assert len(mc) == len(orig) + 3
        assert code_mot.decoder(code) == "LE CHAT DORT SUR LE TAPIS"

    def test_deterministe_avec_graine(self):
        rng1 = random.Random(99)
        rng2 = random.Random(99)
        t = "Test de determinisme"
        assert code_mot.coder(t, rng=rng1) == code_mot.coder(t, rng=rng2)

    def test_avec_accents(self):
        rng = random.Random(5)
        code = code_mot.coder("Voilà un été très chaud", rng=rng)
        assert code_mot.decoder(code) == "VOILA UN ETE TRES CHAUD"
