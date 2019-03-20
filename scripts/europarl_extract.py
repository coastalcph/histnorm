#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from collections import defaultdict, Counter

defaultdict_set = lambda: defaultdict(set)


def main(args):
    europarl = defaultdict(defaultdict_set)

    langqueue = []
    for lang in args.languages:
        prefix = "{}/europarl-v7.{}-en".format(args.dir, lang)
        filename_lang = ".".join((prefix, lang))
        filename_en = ".".join((prefix, "en"))
        for filename in (filename_lang, filename_en):
            if not os.path.exists(filename):
                raise Exception("File not found: {}".format(filename))
        langqueue.append((lang, filename_en, filename_lang))

    for (lang, filename_en, filename_lang) in langqueue:
        print("Processing {}-en...".format(lang))
        with open(filename_en, "r") as f_en:
            with open(filename_lang, "r") as f_lang:
                for (line_en, line_lang) in zip(f_en, f_lang):
                    line_en, line_lang = line_en.strip(), line_lang.strip()
                    if not line_en or not line_lang:
                        continue
                    europarl[line_en][lang].add(line_lang)

    print("Found {:8d} unique English lines.".format(len(europarl)))
    multicount = sum(
        1
        for translations in europarl.values()
        if len(translations) == len(args.languages)
    )
    print("Found {:8d} lines that appear in all languages.".format(multicount))

    outfile = {
        lang: open("extracted.multi.{}".format(lang), "w")
        for lang in list(args.languages) + ["en"]
    }

    for (line, translations) in europarl.items():
        if len(translations) < len(args.languages):
            continue
        print(line, file=outfile["en"])
        for (lang, lines_trans) in translations.items():
            for line_trans in lines_trans:
                print(line_trans, file=outfile[lang])

    for f in outfile.values():
        f.close()


if __name__ == "__main__":
    description = ""
    epilog = "Languages of Europarl files are detected from their filenames."
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument(
        "languages",
        nargs="+",
        metavar="LANG",
        type=str,
        help="Language codes to include",
    )
    parser.add_argument(
        "--dir", default=".", type=str, help="Directory for Europarl files"
    )

    args = parser.parse_args()
    main(args)
