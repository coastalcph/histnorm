#!/usr/bin/fish

set -l datadir "../../texts/normalization/"
set -l csmtiser "$HOME/repositories/csmtiser/"

if test (count $argv) -ne 1
        echo "Usage: ./train_csmtiser.fish <DATASET>"
        echo ""
        echo "Input files:         "$datadir"<DATASET>.{train|dev|test}.txt"
        echo "Output in directory: ./<DATASET>/"
        exit 1
end

set -l currentdir (pwd)
set -l dataset $argv[1]
set -l trainfile "$datadir$dataset.train.txt"
set -l devfile "$datadir$dataset.dev.txt"
set -l testfile "$datadir$dataset.test.txt"

for file in "$trainfile" "$devfile" "$testfile" "config_template.py"
        if not test -e "$file"
                echo "File not found: $trainfile"
                exit 1
        end
end

if test -d "./$dataset"
        echo "Error: directory '$dataset' already exists"
        exit 1
end

if not test -d "$csmtiser"
        echo "Error: csmtiser not found at: $csmtiser"
        exit 1
end

sed "s/<DATASET>/$dataset/g" config_template.py > config.$dataset.py

if test -e "$csmtiser/config.py"
        mv "$csmtiser/config.py" "$csmtiser/config.py.bak"
end

cp config.$dataset.py "$csmtiser/config.py"
mkdir "$dataset"
cut -f1 "$trainfile" > "$dataset/dataset.train.orig"
cut -f2 "$trainfile" > "$dataset/dataset.train.norm"
cut -f1 "$testfile" > "$dataset/dataset.test.orig"
cut -f2 "$testfile" > "$dataset/dataset.test.norm"
cut -f1 "$devfile" > "$dataset/dataset.dev.orig"
cut -f2 "$devfile" > "$dataset/dataset.dev.norm"

cd "$csmtiser"
python2 preprocess.py
python2 train.py
#python2 normalise.py "$currentdir/$dataset/dataset.dev.orig"
python2 normalise.py "$currentdir/$dataset/dataset.test.orig"

if test -e "$csmtiser/config.py.bak"
        mv "$csmtiser/config.py.bak" "$csmtiser/config.py"
end
