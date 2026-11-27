"""Interface en ligne de commande — équivalent moderne de Cryptage.exe.

Usage :
    cryptage factoriser <nombre>
    cryptage code-mot <texte>
    cryptage decode-mot <texte>
    cryptage inverser <texte>
    cryptage crypter <texte> --clef <clef>
    cryptage decrypter <texte> --clef <clef>
    cryptage eratosthene <limite> [--fichier sortie.txt]
    cryptage rsa-gen [--min 3170] [--max 9999]
    cryptage rsa-crypter <texte> --e <e> --n <n>
    cryptage rsa-decrypter <texte> --d <d> --n <n>
    cryptage stegano-cacher <image.bmp> <message> -o <sortie.bmp>
    cryptage stegano-extraire <image.bmp>
    cryptage grands-nombres
"""

from __future__ import annotations

import argparse
import sys

from . import (
    code_mot,
    eratosthene,
    factorisation,
    grands_nombres,
    inversion_bits,
    pseudo_aleatoire,
    rsa,
    steganographie,
)


def cmd_factoriser(args: argparse.Namespace) -> int:
    n = int(args.nombre)
    print(f"Factorisation de {n} :")
    print(f"  {factorisation.factoriser_str(n)}")
    print(f"  Détail : {factorisation.factoriser(n)}")
    return 0


def cmd_code_mot(args: argparse.Namespace) -> int:
    resultat = code_mot.coder(args.texte)
    print(f"Original : {args.texte}")
    print(f"Codé     : {resultat}")
    print(f"Décodé   : {code_mot.decoder(resultat)}")
    return 0


def cmd_decode_mot(args: argparse.Namespace) -> int:
    print(code_mot.decoder(args.texte))
    return 0


def cmd_inverser(args: argparse.Namespace) -> int:
    code = inversion_bits.coder(args.texte)
    print(f"Original : {args.texte!r}")
    print(f"Codé     : {code!r}")
    print(f"Décodé   : {inversion_bits.decoder(code)!r}")
    return 0


def cmd_crypter(args: argparse.Namespace) -> int:
    resultat = pseudo_aleatoire.coder(args.texte, args.clef)
    print(f"Original : {args.texte!r}")
    print(f"Crypté   : {resultat!r}")
    return 0


def cmd_decrypter(args: argparse.Namespace) -> int:
    resultat = pseudo_aleatoire.decoder(args.texte, args.clef)
    print(f"Décrypté : {resultat!r}")
    return 0


def cmd_eratosthene(args: argparse.Namespace) -> int:
    limite = int(args.limite)
    premiers = eratosthene.crible(limite)
    print(f"{len(premiers)} nombres premiers trouvés jusqu'à {limite}.")
    print(f"Premiers : {premiers[:20]}{'…' if len(premiers) > 20 else ''}")
    if args.fichier:
        n = eratosthene.crible_vers_fichier(limite, args.fichier)
        print(f"Écrits dans {args.fichier} ({n} nombres).")
    return 0


def cmd_rsa_gen(args: argparse.Namespace) -> int:
    cles = rsa.generer_cles(borne_inf_pq=args.min, borne_sup_pq=args.max, taille_min_d=0)
    print("Cles RSA générées :")
    print(f"  P = {cles.p}")
    print(f"  Q = {cles.q}")
    print(f"  N = P*Q = {cles.n}")
    print(f"  Phi = (P-1)*(Q-1) = {cles.phi}")
    print(f"  E (clef publique de cryptage)  = {cles.e}")
    print(f"  D (clef privée de décryptage)  = {cles.d}")
    print(f"  Clef publique : (E={cles.e}, N={cles.n})")
    print(f"  Clef privée   : (D={cles.d}, N={cles.n})")
    return 0


def cmd_rsa_crypter(args: argparse.Namespace) -> int:
    resultat = rsa.crypter(args.texte, int(args.e), int(args.n))
    print(f"Original : {args.texte!r}")
    print(f"Crypté   : {resultat}")
    return 0


def cmd_rsa_decrypter(args: argparse.Namespace) -> int:
    resultat = rsa.decrypter(args.texte, int(args.d), int(args.n))
    print(f"Décrypté : {resultat!r}")
    return 0


def cmd_stegano_cacher(args: argparse.Namespace) -> int:
    nb = steganographie.cacher(args.image, args.message, args.sortie)
    print(f"Message caché dans {args.sortie} ({nb} octets de pixels utilisés).")
    return 0


def cmd_stegano_extraire(args: argparse.Namespace) -> int:
    msg = steganographie.extraire(args.image)
    print(f"Message extrait : {msg!r}")
    return 0


def cmd_grands_nombres(args: argparse.Namespace) -> int:
    resultats = grands_nombres.demo()
    print("Arithmétique sur nombres de 1000 chiffres :")
    for k, v in resultats.items():
        print(f"  {k} = {v}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cryptage",
        description="Portage Python du TPE Cryptage (VB6, 2004)",
    )
    sub = parser.add_subparsers(dest="commande", required=True)

    p = sub.add_parser("factoriser", help="Factoriser un entier en facteurs premiers")
    p.add_argument("nombre")
    p.set_defaults(func=cmd_factoriser)

    p = sub.add_parser("code-mot", help="Coder un texte mot par mot (César amélioré)")
    p.add_argument("texte")
    p.set_defaults(func=cmd_code_mot)

    p = sub.add_parser("decode-mot", help="Décoder un texte codé mot par mot")
    p.add_argument("texte")
    p.set_defaults(func=cmd_decode_mot)

    p = sub.add_parser("inverser", help="Inverser tous les bits (code ET décodage)")
    p.add_argument("texte")
    p.set_defaults(func=cmd_inverser)

    p = sub.add_parser("crypter", help="Crypter avec une clef (générateur pseudo-aléatoire)")
    p.add_argument("texte")
    p.add_argument("--clef", required=True)
    p.set_defaults(func=cmd_crypter)

    p = sub.add_parser("decrypter", help="Décrypter avec une clef")
    p.add_argument("texte")
    p.add_argument("--clef", required=True)
    p.set_defaults(func=cmd_decrypter)

    p = sub.add_parser("eratosthene", help="Crible d'Ératosthène jusqu'à une limite")
    p.add_argument("limite")
    p.add_argument("--fichier", help="Écrire les résultats dans un fichier")
    p.set_defaults(func=cmd_eratosthene)

    p = sub.add_parser("rsa-gen", help="Générer un jeu de clefs RSA")
    p.add_argument("--min", type=int, default=10000, help="Borne inf pour P et Q")
    p.add_argument("--max", type=int, default=99999, help="Borne sup pour P et Q")
    p.set_defaults(func=cmd_rsa_gen)

    p = sub.add_parser("rsa-crypter", help="Crypter un texte avec RSA")
    p.add_argument("texte")
    p.add_argument("--e", required=True, help="Exposant public E")
    p.add_argument("--n", required=True, help="Module N")
    p.set_defaults(func=cmd_rsa_crypter)

    p = sub.add_parser("rsa-decrypter", help="Décrypter un texte avec RSA")
    p.add_argument("texte")
    p.add_argument("--d", required=True, help="Exposant privé D")
    p.add_argument("--n", required=True, help="Module N")
    p.set_defaults(func=cmd_rsa_decrypter)

    p = sub.add_parser("stegano-cacher", help="Cacher un message dans une image BMP")
    p.add_argument("image", help="Image BMP source (24 bits)")
    p.add_argument("message")
    p.add_argument("-o", "--sortie", required=True, help="Image BMP de sortie")
    p.set_defaults(func=cmd_stegano_cacher)

    p = sub.add_parser("stegano-extraire", help="Extraire le message d'une image BMP")
    p.add_argument("image", help="Image BMP contenant le message caché")
    p.set_defaults(func=cmd_stegano_extraire)

    p = sub.add_parser("grands-nombres", help="Démo arithmétique grands nombres (1000 chiffres)")
    p.set_defaults(func=cmd_grands_nombres)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
