#!/usr/bin/env python3

import argparse


def main(args):
    vocab = set((line.strip().split("\t")[0] for line in args.trainfile))

    for refline, knownline, unkline in zip(args.reffile, args.knownfile, args.unkfile):
        if "\t" not in refline:
            continue
        orig, gold = refline.strip().split("\t")
        if orig in vocab:
            norm = knownline.strip()
        else:
            norm = unkline.strip()
        norm = norm.split("\t")[-1] if "\t" in norm else norm
        print("{}\t{}".format(orig, norm))


if __name__ == "__main__":
    description = ("Combine predictions from two systems based on whether the source token "
                   "was seen during training or not.")
    epilog = ""
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('reffile',
                        metavar='REFFILE',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        help='Reference normalizations in two-column format')
    parser.add_argument('trainfile',
                        metavar='TRAINFILE',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        help='Training file in two-column format')
    parser.add_argument('knownfile',
                        metavar='NORMFILE_KNOWN',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        help=('Predicted normalizations that should be used for known (in-vocabulary) tokens'))
    parser.add_argument('unkfile',
                        metavar='NORMFILE_UNKNOWN',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        help=('Predicted normalizations that should be used for unknown (out-of-vocabulary) tokens'))
    args = parser.parse_args()

    main(args)
