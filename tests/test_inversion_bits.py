"""Tests pour le module inversion_bits (4.rtf)."""

from cryptage import inversion_bits


class TestInversionBits:
    def test_aller_retour(self):
        texte = "Hello World!"
        code = inversion_bits.coder(texte)
        assert inversion_bits.decoder(code) == texte

    def test_not_involutif(self):
        # coder deux fois = identité
        texte = "ABC"
        assert inversion_bits.coder(inversion_bits.coder(texte)) == texte

    def test_bit_inversion(self):
        # 'A' = 0x41 = 01000001 → ~ = 10111110 = 0xBE
        assert ord(inversion_bits.coder("A")) == 0xBE

    def test_texte_vide(self):
        assert inversion_bits.coder("") == ""
