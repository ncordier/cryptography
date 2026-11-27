"""Tests pour le module grands_nombres (12.rtf)."""

from cryptage import grands_nombres


class TestGrandsNombres:
    def test_addition(self):
        a = int("9" * 100)
        b = int("1" * 100)
        assert grands_nombres.add(a, b) == a + b

    def test_multiplication(self):
        a = int("9" * 500)
        b = int("7" * 500)
        assert grands_nombres.mult(a, b) == a * b
        # Vérifie que le résultat a bien ~1000 chiffres
        assert len(str(grands_nombres.mult(a, b))) >= 999

    def test_division(self):
        a = int("9" * 100)
        assert grands_nombres.div_entiere(a, 3) == a // 3

    def test_modulo(self):
        assert grands_nombres.modulo(17, 5) == 2

    def test_demo(self):
        resultats = grands_nombres.demo()
        assert len(resultats) == 4
