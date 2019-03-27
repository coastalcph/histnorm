#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import argparse
import random


class MainApplication(object):
    data = []

    def __init__(self, args):
        self.args = args

    def read_data(self):
        def read_line_data():
            for line in self.args.infile:
                self.data.append(line)

        def read_block_data():
            cache = ""
            for line in self.args.infile:
                cache += line
                if len(line.strip()) == 0:
                    self.data.append(cache)
                    cache = ""

        if self.args.unit == "line":
            read_line_data()
        elif self.args.unit == "block":
            read_block_data()

    def get_random_subsamples(self):
        # adapted from: http://codereview.stackexchange.com/questions/4872/pythonic-split-list-into-n-random-chunks-of-roughly-equal-size
        n = self.args.num
        size = self.args.size if self.args.size else len(self.data) / n
        if n * size > len(self.data):
            sys.stderr.write("Warning: samples will overlap\n")
            sys.stderr.flush()
            step = (len(self.data) - size) / (n - 1)
        else:
            step = size
        if not self.args.continuous:
            random.shuffle(self.data)
        for c in range(0, n * step, step):
            yield self.data[c : (c + size)]

    def write_subsamples(self):
        n = 0
        for subsample in self.get_random_subsamples():
            n += 1
            with open("%s_%i" % (self.args.prefix, n), "w") as f:
                f.write("".join(subsample))

    def run(self):
        self.read_data()
        self.write_subsamples()


if __name__ == "__main__":
    description = "Randomly splits up a sample file into subsamples of equal length to be used for k-fold cross-validation."
    epilog = ""
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument(
        "infile",
        metavar="INPUT",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Input file (default: STDIN)",
    )
    parser.add_argument(
        "prefix", metavar="PREFIX", help="Prefix for generated subsample files"
    )
    parser.add_argument(
        "-c",
        "--continuous",
        action="store_true",
        default=False,
        help="Make continuous samples, don't shuffle",
    )
    parser.add_argument(
        "-e",
        "--encoding",
        metavar="ENC",
        default="utf-8",
        help="Encoding of the input file (default: %(default)s)",
    )
    parser.add_argument(
        "-n",
        "--num",
        metavar="N",
        type=int,
        default=10,
        help="Number of subsamples to create (default: %(default)d)",
    )
    parser.add_argument(
        "-s",
        "--size",
        metavar="N",
        type=int,
        help="Force subsamples to be of a specific size",
    )
    parser.add_argument(
        "-u",
        "--unit",
        choices=("line", "block"),
        default="line",
        help="Unit of data points in the sample file. "
        + '"line" uses lines as data points; '
        + '"block" uses blocks of lines separated by a blank line. '
        + "(default: %(default)s)",
    )

    args = parser.parse_args()

    # launching application ...
    try:
        MainApplication(args).run()
    except SystemExit:
        sys.stderr.write("\nThere were errors.\n")
        sys.stderr.flush()
