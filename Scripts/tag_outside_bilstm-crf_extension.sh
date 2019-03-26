test=$1
model=$2 # models/MyModel/

workingDir=$(pwd)
mkdir ../tagger/dataset

python Scripts/converter.py $test crf conll ../tagger/dataset/test.conll

cd ../tagger

python tagger.py --model $workingDir/$model --input dataset/test.conll --output dataset/test.tagged

cd $workingDir

cut -f1 ../tagger/dataset/test.tagged > $test.pred
