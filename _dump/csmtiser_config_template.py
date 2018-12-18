# -*- encoding: utf-8 -*-

# Configuration file of the normaliser. The paths to Moses components and various parameters are set here.

# Absolute path to the directory in which the models should be created
data_dir='/home/bollmann/repositories/phd/models/csmt/<DATASET>/'
working_dir='/home/bollmann/repositories/phd/models/csmt/<DATASET>/'
repo_dir='/home/bollmann/repositories/csmtiser/'

# Encoding of all the datasets
encoding='utf8'

# the character to be used internally for marking word boundaries
# this must be a single character that is different from the space character and does not appear anywhere in the corpus
# usually, the underscore (_) is a good choice, but as it occurs in the example Slovene twitter file we use the pound sign here
tokenseparator='÷'

# Whether the data has to be tokenised, ie. spaces put before punctuation etc.
tokenise=False

# Whether the data should be truecased.
truecase=False
# Location of the dataset on which truecasing should be learnt, if no dataset (or model) is given, truecasing is learnt on both sides of the training data
truecase_dataset=None
# If you already have a truecasing model available, just give its' path and that model will be used
truecase_model=None

# Whether the data should be lowercased, if the data is written in non-standard orthography (like Twitter data), this is probably a good idea, however, all normalisation will therefore be lowercased as well
lowercase=False

# Whether the output should be verticalised and token-aligned
align=False

# Training datasets
train_orig=data_dir+'dataset.train.orig'
train_norm=data_dir+'dataset.train.norm'

# Percentage of training data to be used for development set (for tuning the system)
# If you have a dev set aisde of the training data, define the path in the dev variable
dev_perc=0
dev_orig=data_dir+'dataset.dev.orig'
dev_norm=data_dir+'dataset.dev.norm'

# Location of the datasets for language modeling, the target-side training data is always used (does not have to be defined)
# Experiments show that using multiple relevant target-language datasets as language models is the easiest way to improve your results
lms=[]

# Order of the language model, if you have compiled KenLM allowing orders higher than 6, order 10 has shown to yield best results
lm_order=6

# Location of the Moses scripts
moses_scripts='/home/bollmann/repositories/mosesdecoder/scripts/'

# Location of the KenLM tool for language modeling (by default installed with Moses)
kenlm='/home/bollmann/repositories/mosesdecoder/bin/'

# Location of the Moses decoder, mostly same as location of KenLM
moses='/home/bollmann/repositories/mosesdecoder/bin/'

# Location of mgiza
mgiza='/home/bollmann/repositories/mgiza/mgizapp/inst/bin/'

# Number of CPU cores to use during training and tuning
num_cores=10
