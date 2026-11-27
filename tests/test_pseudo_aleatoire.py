"""Tests pour le module pseudo_aleatoire (6.rtf)."""

from cryptage import pseudo_aleatoire


class TestMakeClef:
    def test_deterministe(self):
        assert pseudo_aleatoire.make_clef("motdepasse") == pseudo_aleatoire.make_clef("motdepasse")

    def test_differentes_cles(self):
        assert pseudo_aleatoire.make_clef("abc") != pseudo_aleatoire.make_clef("abd")

    def test_plage(self):
        c = pseudo_aleatoire.make_clef("test")
        assert 1 <= c <= 16777214


class TestCoderDecoder:
    def test_aller_retour_str(self):
        msg = "Message secret à crypter!"
        clef = "ma-clef-secrete"
        chiffre = pseudo_aleatoire.coder(msg, clef)
        assert chiffre != msg
        assert pseudo_aleatoire.decoder(chiffre, clef) == msg

    def test_aller_retour_int(self):
        msg = "Hello"
        clef = 42
        chiffre = pseudo_aleatoire.coder(msg, clef)
        assert pseudo_aleatoire.decoder(chiffre, clef) == msg

    def test_clef_zero(self):
        msg = "Inchangé"
        assert pseudo_aleatoire.coder(msg, 0) == msg
        assert pseudo_aleatoire.decoder(msg, 0) == msg

    def test_mauvaise_clef(self):
        msg = "Secret"
        chiffre = pseudo_aleatoire.coder(msg, "bonne")
        assert pseudo_aleatoire.decoder(chiffre, "mauvaise") != msg

    def test_deterministe(self):
        msg = "Test"
        c1 = pseudo_aleatoire.coder(msg, "clef")
        c2 = pseudo_aleatoire.coder(msg, "clef")
        assert c1 == c2
