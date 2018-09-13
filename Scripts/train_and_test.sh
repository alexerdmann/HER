### THIS SCRIPT ASSUMES WE ARE WORKING WITH THE FULL CORPUS AS INPUT ###

preprocessedPath=$1
corpus="${preprocessedPath##*/}"
ranking=$2
trainSize=$3 # number of sents to be put in training set
features=$4 # separated by '_'
sentenceModelPath=Models/RankedSents/$corpus.$ranking.pkl # pickle file of ranked sentences to take train and test sets from
sentenceModel="${sentenceModelPath##*/}"

rm */*/*fullCorpus*
cat $preprocessedPath > Data/Prepared/fullCorpus.txt

echo "BUILD RANKED MODELS OF SENTENCES"
python3 Scripts/rankSents.py -corpus $preprocessedPath -sort_method $ranking -output $sentenceModelPath -annotate True
python3 Scripts/rankSents.py -corpus $preprocessedPath -sort_method $ranking -output $sentenceModelPath -replace True
rm ANNOTATE.txt

echo 'DIVIDING RANKED SENTENCES INTO TRAINING AND TEST SET'
python3 Scripts/divideSets.py $sentenceModelPath $trainSize -fullCorpus # CAN COMMENT OUT FULLCORPUS IF YOU WANT IT TO USE A FULL CORPUS BIGGER THAN WHAT IT'S CONSIDERING TAKING ITS TRAINING DATA FROM

echo 'GENERATING SPECIFIED FEATURES FOR TRAINING AND TEST SETS'
featureList="$(echo $features | tr '_' ' ')"
python3 Scripts/addFeatures.py -corpus $sentenceModelPath.train$trainSize -fullCorpus $preprocessedPath -features $featureList -simplify True > Data/Features/$sentenceModel.train$trainSize.$features
python3 Scripts/addFeatures.py -corpus $sentenceModelPath.test$trainSize -fullCorpus $preprocessedPath -features $featureList -simplify True > Data/Features/$sentenceModel.test$trainSize.$features

echo 'TRAIN CRF MODEL ON THE TRAINING SET'
crfsuite learn -a pa -m Models/CRF/$sentenceModel.$trainSize.$features.cls Data/Features/$sentenceModel.train$trainSize.$features > delete.txt

echo 'EVALUATE THE CRF ON THE TEST SET AND PRINT RESULTS'
crfsuite tag -m Models/CRF/$sentenceModel.$trainSize.$features.cls Data/Features/$sentenceModel.test$trainSize.$features > Results/$sentenceModel.$trainSize.$features.pred

### CHECK OUT RESULTS
# paste -d , Results/$sentenceModel.$trainSize.$features.pred Data/Features/$sentenceModel.test$trainSize.$features
clear
echo "SENTENCES ANNOTATED: $trainSize"
python3 Scripts/getCounts.py $preprocessedPath
python3 Scripts/customListEval.py Data/Features/$sentenceModel.train$trainSize.$features Data/Features/$sentenceModel.test$trainSize.$features Results/$sentenceModel.$trainSize.$features.pred
echo
crfsuite tag -t -q -m Models/CRF/$sentenceModel.$trainSize.$features.cls Data/Features/$sentenceModel.test$trainSize.$features

# echo 'FRACTION OF ALL HARD CAPPED UNK WORDS WHICH ARE IN THE TRAINING SET'
# python3 Scripts/getRegressionFeats.py $sentenceModelPath.train$trainSize $sentenceModelPath.test$trainSize -light

# ### clean up temp files -> toggle off if you want to debug using any of these files
rm Results/$sentenceModel.$trainSize.$features.pred
rm Data/Features/$sentenceModel.train$trainSize.$features
rm Data/Features/$sentenceModel.test$trainSize.$features
rm $sentenceModelPath.train$trainSize
rm $sentenceModelPath.test$trainSize
rm Models/CRF/$sentenceModel.$trainSize.$features.cls
rm delete.txt
