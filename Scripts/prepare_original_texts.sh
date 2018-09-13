preprocessScript=$1
lg=$2

cd Data/Original
for f in *; do python ../../$preprocessScript $f > ../Preprocessed/$f; done

cd ../Preprocessed
for f in *; do ../../Scripts/Moses_Tokenizer/tokenizer/tokenizer.perl -l $lg < $f > ../Tokenized/$f; done

cd ../Tokenized
for f in *; do python ../../Scripts/prepare4crf.py $f > ../Prepared/$f; done
cd ../../

rm -f Data/Prepared/fullCorpus.txt
cat Data/Prepared/* > Data/Prepared/fullCorpus.txt
