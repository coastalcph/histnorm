#!/usr/bin/env python3

import argparse
import numpy as np
from statsmodels.stats.contingency_tables import mcnemar

def get_norm(line):
    line = line.strip()
    return line.split("\t")[-1] if "\t" in line else line

def main(args):
    table = np.zeros((2, 2))
    for (gold, norm_a, norm_b) in zip(args.reffile, args.norm_a, args.norm_b):
        gold   = get_norm(gold)
        norm_a = get_norm(norm_a)
        norm_b = get_norm(norm_b)
        table[int(norm_a == gold)][int(norm_b == gold)] += 1

    print(table)
    print(mcnemar(table))



if __name__ == "__main__":
    description = ("Compare two normalizations against a gold-standard "
                   "reference and output statistical significance of "
                   "their difference in accuracy.")
    epilog = "All files can be one- or two-column; only the last column is used."
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('reffile',
                        metavar='REFFILE',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        help='Reference normalizations')
    parser.add_argument('norm_a',
                        metavar='NORMFILE_1',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        help='Predicted normalizations')
    parser.add_argument('norm_b',
                        metavar='NORMFILE_2',
                        type=argparse.FileType('r', encoding="UTF-8"),
                        help='Predicted normalizations')
    args = parser.parse_args()
    main(args)

