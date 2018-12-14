#!/bin/bash

EUROPARL_DIR=.

for f in de en es pt hu sl sv ; do
        ${EUROPARL_DIR}/tools/tokenizer.perl -l $f < extracted.multi.$f > extracted.multi.$f.tok
        sed 's/ /\n/g' extracted.multi.$f.tok > extracted.multi.$f.toksplit
        sed -i '/^$/d' extracted.multi.$f.toksplit
        python3 preprocess.py -l -p -u extracted.multi.$f.toksplit > __F
        mv __F extracted.multi.$f.toksplit
        env LC_ALL=C sort extracted.multi.$f.toksplit | env LC_COLLATE=C uniq > extracted.multi.$f.uniq
done
