"""Stéganographie — cacher un texte dans une image BMP 24 bits.

Portage fidèle de 15.txt / 14.rtf : on cache 2 bits par octet de pixel
dans les 2 bits de poids faible (LSB). La modification est invisible
à l'œil nu mais disparaît si l'image est recompressée.

Format des données cachées :
  - 4 octets (32 bits) = longueur du message en octets (UTF-8)
  - N octets = message encodé en UTF-8
Chaque octet est découpé en 4 groupes de 2 bits, stockés dans les
2 LSB de 4 octets de pixel consécutifs (B, G, R, B, …).
"""

from __future__ import annotations

import struct

BITS_PAR_OCTET_PIXEL = 2  # 2 LSB utilisés par octet de pixel
GROUPES_PAR_OCTET = 4     # 8 bits / 2 = 4 groupes de 2 bits


def _lire_bmp(chemin: str) -> tuple[bytearray, int, int, int, int]:
    """Lit un BMP 24 bits non compressé.

    Retourne (data, offset_pixels, largeur, hauteur, stride).
    """
    with open(chemin, "rb") as f:
        data = bytearray(f.read())
    if data[:2] != b"BM":
        raise ValueError("Fichier BMP invalide (marqueur 'BM' absent).")
    offset = struct.unpack_from("<I", data, 10)[0]
    largeur = struct.unpack_from("<i", data, 18)[0]
    hauteur = struct.unpack_from("<i", data, 22)[0]
    bpp = struct.unpack_from("<H", data, 28)[0]
    compression = struct.unpack_from("<I", data, 30)[0]
    if bpp != 24:
        raise ValueError(f"Seuls les BMP 24 bits sont supportés (trouvé {bpp} bits).")
    if compression != 0:
        raise ValueError("Seuls les BMP non compressés sont supportés.")
    ligne = largeur * 3
    padding = (4 - (ligne % 4)) % 4
    stride = ligne + padding
    return data, offset, largeur, hauteur, stride


def _iterer_positions_pixels(
    offset: int, largeur: int, hauteur: int, stride: int
) -> "object":
    """Itère sur les positions d'octets de pixels (B, G, R) dans l'ordre BMP."""
    h_abs = abs(hauteur)
    for row in range(h_abs):
        y = row if hauteur > 0 else h_abs - 1 - row
        row_start = offset + y * stride
        for col in range(largeur):
            for c in range(3):
                yield row_start + col * 3 + c


def _octet_vers_groupes2(octet: int) -> list[int]:
    """Découpe un octet en 4 groupes de 2 bits (MSB d'abord)."""
    return [(octet >> 6) & 3, (octet >> 4) & 3, (octet >> 2) & 3, octet & 3]


def _groupes2_vers_octet(groupes: list[int]) -> int:
    """Reconstitue un octet à partir de 4 groupes de 2 bits."""
    return (groupes[0] << 6) | (groupes[1] << 4) | (groupes[2] << 2) | groupes[3]


def cacher(chemin_image: str, message: str, chemin_sortie: str) -> int:
    """Cache `message` dans l'image BMP et écrit le résultat.

    Retourne le nombre d'octets de pixels utilisés.
    """
    data, offset, largeur, hauteur, stride = _lire_bmp(chemin_image)
    msg_bytes = message.encode("utf-8")
    payload = struct.pack("<I", len(msg_bytes)) + msg_bytes

    # Convertir le payload en séquence de groupes de 2 bits
    groupes: list[int] = []
    for byte in payload:
        groupes.extend(_octet_vers_groupes2(byte))

    positions = list(_iterer_positions_pixels(offset, largeur, hauteur, stride))
    if len(groupes) > len(positions):
        raise ValueError(
            f"Message trop long : {len(groupes)} groupes de 2 bits nécessaires, "
            f"mais seulement {len(positions)} octets de pixels disponibles."
        )

    for i, pos in enumerate(positions):
        if i < len(groupes):
            # Écrire le groupe de 2 bits dans les 2 LSB de l'octet
            data[pos] = (data[pos] & 0xFC) | (groupes[i] & 0x03)
        else:
            break

    with open(chemin_sortie, "wb") as f:
        f.write(data)
    return len(groupes)


def extraire(chemin_image: str) -> str:
    """Extrait le message caché dans l'image BMP."""
    data, offset, largeur, hauteur, stride = _lire_bmp(chemin_image)
    positions = _iterer_positions_pixels(offset, largeur, hauteur, stride)

    # Lire les 16 premiers groupes de 2 bits → longueur (4 octets × 4 groupes)
    groupes: list[int] = []
    for pos in positions:
        groupes.append(data[pos] & 0x03)
        if len(groupes) >= 16:
            break
    if len(groupes) < 16:
        return ""

    # 4 octets = 16 groupes de 2 bits, en little-endian (struct.pack "<I")
    longueur = 0
    for i in range(0, 16, 4):
        longueur |= _groupes2_vers_octet(groupes[i:i + 4]) << (8 * (i // 4))

    if longueur == 0 or longueur > 100_000_000:
        return ""

    # Lire le message : longueur octets = longueur * 4 groupes de 2 bits
    total_groupes = 16 + longueur * GROUPES_PAR_OCTET
    for pos in positions:
        if len(groupes) >= total_groupes:
            break
        groupes.append(data[pos] & 0x03)

    if len(groupes) < total_groupes:
        return ""

    msg_groupes = groupes[16:]
    octets = []
    for i in range(0, len(msg_groupes), 4):
        if i + 3 < len(msg_groupes):
            octets.append(_groupes2_vers_octet(msg_groupes[i:i + 4]))

    return bytes(octets).decode("utf-8", errors="replace")
