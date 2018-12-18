#!/bin/bash

# this file is used to train RNN seq2seq models, 
# you need to adjust the paths and related parameters 
# especially when you train subword-level models, 
# you need change vocabulary setting "--max-size"

RNN=tanh # or lstm, gru

DATASET=char
DATADIR=~/data/tmp_for_marian/
MARIAN=~/code/marian

TRAIN_SRC=$DATADIR/train.src
TRAIN_TRG=$DATADIR/train.trg
DEV_SRC=$DATADIR/dev.src
DEV_TRG=$DATADIR/dev.trg

MODEL_DIR=~/models/marian/_tmp
rm -rf $MODEL_DIR
mkdir -p $MODEL_DIR

WORKSPACE=10000 #change this value to fit your GPU memory
N=1
EPOCHS=0
B=5 #beam size

if [ ! -e $MARIAN/build/marian ]
then
    echo "marian is not installed in ../../build, you need to compile the toolkit first"
    exit 1
fi

# create common vocabulary
if [ ! -e "${MODEL_DIR}/vocab.ende.yml" ]
then
    cat $TRAIN_SRC $TRAIN_TRG | $MARIAN/build/marian-vocab --max-size 200 > ${MODEL_DIR}/vocab.ende.yml
fi

# train model, you need to change the value of "devices" 
$MARIAN/build/marian \
    --model ${MODEL_DIR}/model.npz --type s2s \
    --enc-cell $RNN --dec-cell $RNN \
    --train-sets $TRAIN_SRC $TRAIN_TRG \
    --max-length 100 \
    --vocabs ${MODEL_DIR}/vocab.ende.yml ${MODEL_DIR}/vocab.ende.yml \
    --mini-batch-fit -w $WORKSPACE --mini-batch 1000 --maxi-batch 1000 \
    --valid-freq 500 --save-freq 500 --disp-freq 500 \
    --valid-metrics ce-mean-words perplexity  \
    --valid-sets $DEV_SRC $DEV_TRG \
    --valid-translation-output ${MODEL_DIR}/valid.bpe.en.output --quiet-translation \
    --beam-size $B --normalize=1 \
    --valid-mini-batch 64 \
    --overwrite --keep-best \
    --early-stopping 8 --after-epochs $EPOCHS --cost-type=ce-mean-words \
    --log ${MODEL_DIR}/train.log --valid-log ${MODEL_DIR}/valid.log \
    --enc-type bidirectional --enc-depth 1 --enc-cell-depth 6 \
    --dec-depth 1 --dec-cell-base-depth 5 --dec-cell-high-depth 1 \
    --tied-embeddings \
    --layer-normalization \
    --dropout-rnn 0.1 --label-smoothing 0.1 \
    --learn-rate 0.0003 --lr-warmup 16000 --lr-decay-inv-sqrt 16000 --lr-report \
    --optimizer-params 0.9 0.98 1e-09 --clip-norm 5 \
    --devices 0 --sync-sgd --seed 1111  \
    --exponential-smoothing
