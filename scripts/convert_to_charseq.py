#!/usr/bin/env python3

"""Usage: convert_to_charseq.py TRAIN [TEST [DEV]] --to DIRECTORY

Prepares parallel two-column text files for use with XNMT or Marian.

Options:
  -h, --help         Show this helpful text.
  --to DIRECTORY     Output directory for writing the processed files.
"""

from docopt import docopt
import better_exceptions
import os

def preprocess(token):
    token = token.lower()
    token = token.replace(" ", "÷")
    return [char for char in token]

def main(args):
    data = {}
    with open(args["TRAIN"], 'r', encoding="utf-8") as infile:
        data['train'] = [line.strip().split("\t") for line in infile]
    if args["TEST"] is not None:
        with open(args["TEST"], 'r', encoding="utf-8") as infile:
            data['test'] = [line.strip().split("\t") for line in infile]
    if args["DEV"] is not None:
        with open(args["DEV"], 'r', encoding="utf-8") as infile:
            data['dev'] = [line.strip().split("\t") for line in infile]

    outdir = args["--to"]
    os.makedirs(outdir, exist_ok=True)

    for dset in data.keys():
        with open(f"{outdir}/{dset}.src", 'w', encoding="utf-8") as origfile:
            with open(f"{outdir}/{dset}.trg", 'w', encoding="utf-8") as normfile:
                for (orig, norm) in data[dset]:
                    print(*preprocess(orig), file=origfile)
                    print(*preprocess(norm), file=normfile)

    origset, normset = set([]), set([])
    for (orig, norm) in data['train']:
        origset.update(preprocess(orig))
        normset.update(preprocess(norm))
    with open(f"{outdir}/train.src.vocab", 'w', encoding="utf-8") as origfile:
        for item in origset:
            print(item, file=origfile)
    with open(f"{outdir}/train.trg.vocab", 'w', encoding="utf-8") as normfile:
        for item in normset:
            print(item, file=normfile)


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
