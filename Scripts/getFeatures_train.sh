train=$1
test=$2
fullCorpus=$3
featureSet=$4  ## connected by _
featureList="$(echo $featureSet | tr '_' ' ')"
trainFts=$5
testFts=$6
modelLocation=$7
alwaysTrain=$8

### get features
python Scripts/addFeatures.py -corpus $train -fullCorpus $fullCorpus -features $featureList -hist $fullCorpus.hist -gazatteers Data/Gazatteers/* > $trainFts
if [ "$alwaysTrain" != "None" ]; then 
	python Scripts/addFeatures.py -corpus $alwaysTrain -fullCorpus $fullCorpus -features $featureList -hist $fullCorpus.hist -gazatteers Data/Gazatteers/* >> $trainFts
fi

python Scripts/addFeatures.py -corpus $test -fullCorpus $fullCorpus -features $featureList -hist $fullCorpus.hist -gazatteers Data/Gazatteers/* > $testFts

### train crf
crfsuite learn -a pa -m $modelLocation $trainFts > log.txt
rm log.txt
