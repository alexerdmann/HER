seed=$1
alwaysTrain=$2
unannotated=$3
entities=$4

echo
echo "Preparing delexicalized, pretagged splits..."

### Create (preTagged) copies of seed, alwaysTrain, unannotated w/ non-zero tags, and unannotated w/o 
# seed
cp $seed Data/Splits/seed.preTagged
# alwaysTrain
if [ "$alwaysTrain" = "None" ]; then
	touch Data/Splits/alwaysTrain.preTagged
else
	cp $alwaysTrain Data/Splits/alwaysTrain.preTagged
fi


# wc $unannotated 
# wc Data/Splits/unannotated_NE-1.preTagged 
# wc Data/Splits/unannotated_noNE-1.preTagged 
# wc Data/Splits/unannotated_NE-2.preTagged
# wc Data/Splits/unannotated_noNE-2.preTagged 
# echo $entities 
# wc Data/Gazatteers/*
# python Scripts/pre-tag_gazatteers_separate.py $unannotated Data/Splits/unannotated_NE-1.preTagged Data/Splits/unannotated_noNE-1.preTagged Data/Splits/unannotated_NE-2.preTagged Data/Splits/unannotated_noNE-2.preTagged $entities Data/Gazatteers/*





# unannotated w/ and w/o for two folds
python Scripts/pre-tag_gazatteers_separate.py $unannotated Data/Splits/unannotated_NE-1.preTagged Data/Splits/unannotated_noNE-1.preTagged Data/Splits/unannotated_NE-2.preTagged Data/Splits/unannotated_noNE-2.preTagged $entities Data/Gazatteers/*

### Set up 3 splits
# split 0 (trains on seed + always train -i.e. legit tags)
cat Data/Splits/seed.preTagged Data/Splits/alwaysTrain.preTagged > Data/Splits/train_0.preTagged
cat Data/Splits/unannotated*NE*.preTagged > Data/Splits/test_0.preTagged
# split 1 (trains on preTags)
cp Data/Splits/unannotated_NE-1.preTagged Data/Splits/train_1.preTagged
cat Data/Splits/unannotated_NE-2.preTagged Data/Splits/unannotated_noNE-2.preTagged > Data/Splits/test_1.preTagged
# split 2 (trains on preTags)
cp Data/Splits/unannotated_NE-2.preTagged Data/Splits/train_2.preTagged
cat Data/Splits/unannotated_NE-1.preTagged Data/Splits/unannotated_noNE-1.preTagged > Data/Splits/test_2.preTagged

### Delexicalize the features to encourage generalization
for f in Data/Splits/t*_*.preTagged; do python Scripts/addFeatures.py -corpus $f -fullCorpus Data/Prepared/fullCorpus.txt -hist Data/Prepared/fullCorpus.txt.hist -features wordShape prevWord prevBiWord prevWordShape prevBiWordShape nextWordShape nextBiWordShape histStats nextWord nextBiWord contextPosition deLex > $f.deLex; done

echo
echo "Training models to locate sentences with unknown words, likely to be named entities"
echo 
# train, train, align, clean up
# for f in 0 1 2; do crfsuite learn -a pa -m Models/CRF/deLex$f.cls Data/Splits/train_$f.preTagged.deLex > log.txt; rm log.txt; crfsuite tag -m Models/CRF/deLex$f.cls Data/Splits/test_$f.preTagged.deLex > Data/Splits/test_$f.preTagged.deLex.predictions; awk 'FNR==NR{a[NR]=$1;next}{$1=a[FNR]}1' Data/Splits/test_$f.preTagged.deLex.predictions Data/Splits/test_$f.preTagged > Data/Splits/test_$f.aligned.del; cut -f1,2 -d' ' Data/Splits/test_$f.aligned.del > Data/Splits/test_$f.aligned; rm Data/Splits/test_$f.aligned.del; rm Models/CRF/deLex$f.cls; rm Data/Splits/test_$f.preTagged.deLex.predictions; done

for f in 0 1 2; do crfsuite learn -a pa -m Models/CRF/deLex$f.cls Data/Splits/train_$f.preTagged.deLex > log.txt; rm log.txt; crfsuite tag -m Models/CRF/deLex$f.cls Data/Splits/test_$f.preTagged.deLex > Data/Splits/test_$f.preTagged.deLex.predictions; python Scripts/prediction_aligner.py Data/Splits/test_$f.preTagged.deLex.predictions Data/Splits/test_$f.preTagged > Data/Splits/test_$f.aligned.del; cut -f1,2 -d' ' Data/Splits/test_$f.aligned.del > Data/Splits/test_$f.aligned; rm Data/Splits/test_$f.aligned.del; rm Models/CRF/deLex$f.cls; rm Data/Splits/test_$f.preTagged.deLex.predictions; done


### clean up
rm Data/Splits/*.preTagged* # we only need the aligned files





