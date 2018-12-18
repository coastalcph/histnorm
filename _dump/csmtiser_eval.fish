#!/usr/bin/fish

set -l datadir "../../texts/normalization/"
set -l csmtiser "$HOME/repositories/csmtiser/"

if test (count $argv) -ne 1
        echo "Usage: ./eval_dev.fish <DATASET>"
        echo ""
        echo "Input files:         "$datadir"<DATASET>.dev.txt"
        echo "Output in directory: ./<DATASET>/"
        exit 1
end

set -l currentdir (pwd)
set -l dataset $argv[1]
set -l devfile "$datadir$dataset.dev.txt"

if not test -e "$devfile"
        echo "File not found: $devfile"
        exit 1
end

if not test -d "./$dataset"
        echo "Error: directory '$dataset' does not exist"
        exit 1
end

if not test -d "$csmtiser"
        echo "Error: csmtiser not found at: $csmtiser"
        exit 1
end

if test -e "$csmtiser/config.py"
        mv "$csmtiser/config.py" "$csmtiser/config.py.bak"
end

cp config.$dataset.py "$csmtiser/config.py"
cd "$csmtiser"
python2 normalise.py "$currentdir/$dataset/dataset.dev.orig"

if test -e "$csmtiser/config.py.bak"
        mv "$csmtiser/config.py.bak" "$csmtiser/config.py"
end
