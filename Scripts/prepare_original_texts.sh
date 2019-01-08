#!/bin/bash

preprocessScript=$1
lg=$2

cd Data/Original
for f in *;
do
	if [ ${f: -4} == ".crf" ]
	then
		cp $f ../Prepared/$f
	else
		python ../../$preprocessScript $f > ../Preprocessed/$f
	fi
done

if [ -z "$(ls -A ../Preprocessed)" ]
then
   echo "..."
else
	cd ../Preprocessed
	for f in *; do perl ../../Scripts/Moses_Tokenizer/tokenizer/tokenizer.perl -l $lg < $f > ../Tokenized/$f; done

	cd ../Tokenized
	for f in *; do python ../../Scripts/prepare4crf.py $f > ../Prepared/$f; done
fi

cd ../../
rm -f Data/Prepared/fullCorpus.txt
cat Data/Prepared/* > Data/Prepared/fullCorpus.txt
