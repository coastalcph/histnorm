#!/usr/bin/env python3

import argparse
import stringdist
import sys

def accuracy(words):
    """Word accuracy"""
    val = [gold == norm for (gold, norm) in words]
    return val

def cer(words):
    """Character error rate (CER), defined as Levenshtein distance normalized by
       reference word length."""
    val = [(0 if gold == norm else stringdist.levenshtein(gold, norm) / len(gold)) \
           for (gold, norm) in words]
    return val

def main(args, stemmer=None):
    vocab = None
    if args.trainfile:
        vocab = set((line.strip().split("\t")[0] for line in args.trainfile))

    data = []
    for refline, normline in zip(args.reffile, args.normfile):
        if "\t" not in refline:
            continue
        orig, gold = refline.strip().split("\t")
        norm = normline.strip()
        norm = norm.split("\t")[-1] if "\t" in norm else norm
        if args.only_incorrect and gold == norm:
            continue
        if args.only_knowns and orig not in vocab:
            continue
        if args.only_unknowns and orig in vocab:
            continue
        if args.stem:
            gold, norm = stemmer.stemWords([gold, norm])
        data.append((gold, norm))

    print("       Tokens: {:d}".format(len(data)))
    if not data:
        return

    acc = accuracy(data)
    print("Word accuracy: {:.4f}".format(sum(acc) / len(acc)))
    err = cer(data)
    print("  Average CER: {:.4f}".format(sum(err) / len(err)))

if __name__ == "__main__":
    description = ("Evaluate normalization quality.")
    epilog = ""
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('reffile',
                        metavar='REFFILE',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        help='Reference normalizations in two-column format')
    parser.add_argument('normfile',
                        metavar='NORMFILE',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        help=('Predicted normalizations; can be one- or two-column'
                              ' (with normalizations expected in second column)'))
    parser.add_argument('trainfile',
                        metavar='TRAINFILE',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        nargs='?',
                        help='Training file in two-column format; required for some options')
    parser.add_argument('-s', '--stem',
                        metavar='LANGUAGE',
                        type=str,
                        help=('Stem word forms before evaluation; '
                              'LANGUAGE is a language name (e.g., "english")'))
    parser.add_argument('-i', '--only-incorrect',
                        action='store_true',
                        default=False,
                        help='Only evaluate on the subset of incorrect normalizations')
    parser.add_argument('-k', '--only-knowns',
                        action='store_true',
                        default=False,
                        help=('Only evaluate on the subset of known/in-vocabulary tokens;'
                              ' requires TRAINFILE'))
    parser.add_argument('-u', '--only-unknowns',
                        action='store_true',
                        default=False,
                        help=('Only evaluate on the subset of unknown/out-of-vocabulary '
                              'tokens; requires TRAINFILE'))
    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)
    args = parser.parse_args()

    if args.only_knowns and args.only_unknowns:
        parser.error("can't select both --only-knowns and --only-unknowns")
    if (args.only_knowns or args.only_unknowns) and not args.trainfile:
        parser.error("--only-knowns/--only-unknowns requires TRAINFILE")
    stemmer = None
    if args.stem:
        import Stemmer
        try:
            stemmer = Stemmer.Stemmer(args.stem.lower())
        except KeyError:
            parser.error("No stemming algorithm for '{}'; valid choices are: {}".format(
                args.stem, ", ".join(Stemmer.algorithms())))

    main(args, stemmer=stemmer)
