#!/usr/bin/env python3

import argparse
from collections import Counter


def load_memo(memofile):
    lexicon = {}
    for line in memofile:
        orig, norm, count = line.strip().split("\t")
        count = int(count)
        if orig in lexicon and lexicon[orig][1] >= count:
            continue
        lexicon[orig] = (norm, count)
    return lexicon


def apply_(args):
    lexicon = load_memo(args.memofile)

    for line in args.infile:
        orig = line.strip().split("\t")[0]
        norm, count = lexicon.get(orig, (orig, 0))
        if args.frequency:
            print("{}\t{}".format(norm, count))
        else:
            print(norm)


def train(args):
    lexicon = Counter(line.strip() for line in args.infile if line.count("\t") == 1)
    for line, count in lexicon.items():
        print("{}\t{}".format(line, count), file=args.memofile)


def combine(args):
    lexicon = load_memo(args.memofile)

    for line, model_pred in zip(args.infile, args.predfile):
        orig = line.strip().split("\t")[0]
        if orig in lexicon:
            print(lexicon[orig][0])
        else:
            print(model_pred.strip())


if __name__ == "__main__":
    description = "A naive memorization normalizer, functionally equivalent to Norma's Mapper component."
    epilog = ""
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    subparsers = parser.add_subparsers(title="available commands")

    sub = subparsers.add_parser("train", help="Train the memorizer")
    sub.add_argument(
        "memofile",
        metavar="MEMOFILE",
        type=argparse.FileType("w", encoding="UTF-8"),
        help="Output file with learned memorizations",
    )
    sub.add_argument(
        "infile",
        metavar="TRAINFILE",
        type=argparse.FileType("r", encoding="UTF-8"),
        help="Training data in two-column format",
    )
    sub.set_defaults(func=train)

    sub = subparsers.add_parser("apply", help="Apply the memorizer")
    sub.add_argument(
        "memofile",
        metavar="MEMOFILE",
        type=argparse.FileType("r", encoding="UTF-8"),
        help="File with learned memorizations",
    )
    sub.add_argument(
        "infile",
        metavar="ORIGFILE",
        type=argparse.FileType("r", encoding="UTF-8"),
        help="Input data to normalize",
    )
    sub.add_argument(
        "-f",
        "--frequency",
        action="store_true",
        default=False,
        help="Additionally output how often the normalized token was seen during training",
    )
    sub.set_defaults(func=apply_)

    sub = subparsers.add_parser(
        "combine",
        help="Combine memorization with other learned predictions",
        description="This will output the learned memorization whenever possible, and the corresponding prediction from a supplied file whenever the input token is not in the memorization lexicon.",
    )
    sub.add_argument(
        "memofile",
        metavar="MEMOFILE",
        type=argparse.FileType("r", encoding="UTF-8"),
        help="File with learned memorizations",
    )
    sub.add_argument(
        "predfile",
        metavar="PREDFILE",
        type=argparse.FileType("r", encoding="UTF-8"),
        help="File with another model's predictions",
    )
    sub.add_argument(
        "infile",
        metavar="ORIGFILE",
        type=argparse.FileType("r", encoding="UTF-8"),
        help="Input data to normalize",
    )
    sub.set_defaults(func=combine)

    args = parser.parse_args()
    args.func(args)
