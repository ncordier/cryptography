"""Tests pour le module steganographie (14.rtf / 15.txt)."""

import os
import struct
import tempfile

import pytest
from cryptage import steganographie


def _creer_bmp_test(chemin: str, largeur: int = 64, hauteur: int = 64) -> None:
    """Crée un BMP 24 bits uni (gris) de test."""
    ligne = largeur * 3
    padding = (4 - (ligne % 4)) % 4
    stride = ligne + padding
    taille_pixel = stride * hauteur
    taille_fichier = 54 + taille_pixel
    data = bytearray(taille_fichier)
    # En-tête BMP
    data[0:2] = b"BM"
    struct.pack_into("<I", data, 2, taille_fichier)
    struct.pack_into("<I", data, 10, 54)  # offset
    struct.pack_into("<I", data, 14, 40)  # taille header info
    struct.pack_into("<i", data, 18, largeur)
    struct.pack_into("<i", data, 22, hauteur)
    struct.pack_into("<H", data, 26, 1)   # plans
    struct.pack_into("<H", data, 28, 24)  # bpp
    struct.pack_into("<I", data, 30, 0)   # compression
    struct.pack_into("<I", data, 34, taille_pixel)
    # Remplir de gris moyen
    for i in range(54, taille_fichier):
        data[i] = 128
    with open(chemin, "wb") as f:
        f.write(data)


class TestSteganographie:
    def test_aller_retour(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src.bmp")
            dst = os.path.join(tmp, "dst.bmp")
            _creer_bmp_test(src)
            message = "Message caché dans l'image!"
            steganographie.cacher(src, message, dst)
            extrait = steganographie.extraire(dst)
            assert extrait == message

    def test_message_court(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src.bmp")
            dst = os.path.join(tmp, "dst.bmp")
            _creer_bmp_test(src, 32, 32)
            steganographie.cacher(src, "Hi", dst)
            assert steganographie.extraire(dst) == "Hi"

    def test_message_long(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src.bmp")
            dst = os.path.join(tmp, "dst.bmp")
            _creer_bmp_test(src, 200, 200)
            message = "Un message un peu plus long pour tester la stéganographie. " * 5
            steganographie.cacher(src, message, dst)
            assert steganographie.extraire(dst) == message

    def test_trop_long(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src.bmp")
            dst = os.path.join(tmp, "dst.bmp")
            _creer_bmp_test(src, 4, 4)  # très petite image
            with pytest.raises(ValueError, match="trop long"):
                steganographie.cacher(src, "X" * 1000, dst)

    def test_image_non_modifiee_hors_zone(self):
        """Les pixels non utilisés pour le message doivent rester identiques."""
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src.bmp")
            dst = os.path.join(tmp, "dst.bmp")
            _creer_bmp_test(src, 64, 64)
            steganographie.cacher(src, "A", dst)
            with open(src, "rb") as f:
                orig = f.read()
            with open(dst, "rb") as f:
                mod = f.read()
            # L'en-tête doit être identique
            assert orig[:54] == mod[:54]
            # La majorité des octets doivent être identiques (seulement 20 octets modifiés pour "A" + longueur)
            diffs = sum(1 for a, b in zip(orig, mod) if a != b)
            assert diffs <= 24  # 4 octets longueur + 1 octet message = 5 octets = 20 groupes de 2 bits
