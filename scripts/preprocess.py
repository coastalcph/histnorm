#!/usr/bin/env python3

import argparse
import re
import string
import sys
import unicodedata


def main(args):
    for line in args.infile:
        if not line.rstrip():
            if not args.filter_boundaries:
                print()
            continue
        tokens = line.rstrip().split("\t")
        if len(tokens) < 2 and args.filter_empty:
            continue
        if args.filter_punctuation:
            punct = [
                all(map(lambda x: unicodedata.category(x).startswith("P"), t))
                for t in tokens
                if len(t) > 0
            ]
            if any(punct):
                continue
        if args.unicode_normalize is not None:
            tokens = [unicodedata.normalize(args.unicode_normalize, t) for t in tokens]
        if args.lower:
            tokens = [t.lower() for t in tokens]
        if args.digits and any(digit in tokens[0] for digit in string.digits):
            if all(t == tokens[0] for t in tokens[1:]):
                tokens = [re.sub("\d", "0", t) for t in tokens]
        if args.spaces != " ":
            tokens = [re.sub(" ", args.spaces, t) for t in tokens]
        print("\t".join(tokens))


if __name__ == "__main__":
    description = "Preprocess normalization datasets in two-column format."
    epilog = ""
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument(
        "infile", type=argparse.FileType("r", encoding="UTF-8"), help="Input file"
    )
    parser.add_argument(
        "-A",
        "--all",
        action="store_true",
        default=False,
        help='Equivalent to "-bdepl -s ÷ -u NFC"; overrides all other options',
    )
    parser.add_argument(
        "-b",
        "--filter-boundaries",
        action="store_true",
        default=False,
        help="Remove empty lines (indicating sentence boundaries)",
    )
    parser.add_argument(
        "-d",
        "--digits",
        action="store_true",
        default=False,
        help="Replace digits with zeroes when they are identical across columns",
    )
    parser.add_argument(
        "-e",
        "--filter-empty",
        action="store_true",
        default=False,
        help="Filter lines where either column is empty",
    )
    parser.add_argument(
        "-l", "--lower", action="store_true", default=False, help="Lowercase everything"
    )
    parser.add_argument(
        "-p",
        "--filter-punctuation",
        action="store_true",
        default=False,
        help="Filter lines where either column consists only of punctuation characters",
    )
    parser.add_argument(
        "-s",
        "--spaces",
        type=str,
        default=" ",
        help='Replace spaces within columns with this character (default: "%(default)s")',
    )
    parser.add_argument(
        "-u",
        "--unicode-normalize",
        choices=("NFC", "NFKC", "NFD", "NFKD"),
        default=None,
        help="Perform Unicode normalization to given standard form (default: None)",
    )

    args = parser.parse_args()
    if args.all:
        args.filter_boundaries = True
        args.digits = True
        args.filter_empty = True
        args.filter_punctuation = True
        args.lower = True
        args.spaces = "÷"
        args.unicode_normalize = "NFC"

    main(args)
