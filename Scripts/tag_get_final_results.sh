lines_annotated=$1
start_unannotated=$(($lines_annotated + 1))
rankedSents=$2
alwaysTrain=$3
unannotated=$4
seed=$5
fullCorpus=$6
predictions=$7
final_corpus=$8
final_list=$9
tagger="${10}"



### tag
if [ $tagger == 'crf' ];
	then
		crfsuite tag -m Models/CRF/best_seed.cls $unannotated.fts > $predictions
elif [ $tagger == 'bilstm-crf' ]
	### using Lample et al 2016
	then
		echo "TRAINING FULL NER MODEL WITH BiLSTM-CRF ARCHITECTURE OF LAMPLE ET AL. (2016)."
		echo "THIS COULD TAKE OVER A DAY, GO GET A SNACK."
		workingDir=$(pwd)
		cd ../tagger
		### get a training set in conll format (dev will be seed, but irrelevant)
		mkdir dataset
		cat $workingDir/$seed $workingDir/$alwaysTrain > dataset/train.crf
		python $workingDir/Scripts/converter.py dataset/train.crf crf conll dataset/train.conll
		python $workingDir/Scripts/converter.py $workingDir/$seed crf conll dataset/dev.conll
		### conll format unannotated data to be the test
		python $workingDir/Scripts/converter.py $workingDir/$unannotated crf conll dataset/test.conll

		### train
		python train.py --train dataset/train.conll --dev dataset/dev.conll --test dataset/dev.conll --model_loc MyModel --path_to_tagger $PWD # --n_epochs 2 # remove the n_epochs after finish debugging

		### test
		python tagger.py --model models/MyModel/ --input dataset/test.conll --output dataset/test.tagged

		### reformat the test output and move to desired location
		cut -f1 dataset/test.tagged > $workingDir/$predictions

		echo "THE MODEL IS STORED IN THE FOLLOWING DIRECTORY:"
		echo $PWD/models/MyModel
		echo "YOU MAY WANT TO RENAME THIS DIRECTORY SOMETHING MORE MEANINGFUL SO YOU REMEMBER WHAT IT IS.. THIS ALSO WILL PROTECT YOU FROM ACCIDENTALLY OVERWRITING IT SHOULD YOU TRAIN ANOTHER MODEL IN THE FUTURE."
		echo
		cd $workingDir






elif [ $tagger == 'cnn-bilstm' ]
	then
		echo "THE CNN-BiLSTM MODEL OF SHEN ET AL. (2017) IS NOT YET SUPPORTED.. SORRY FOR THE INCONVENIENCE!"
		# echo "TRAINING FULL NER MODEL WITH CNN-BiLSTM ARCHITECTURE OF SHEN ET AL. (2017)."
		# echo "THIS COULD TAKE OVER A DAY, GO GET A SNACK."
		# workingDir=$(pwd)
		# cd ../Active_CNN-BiLSTM
		# ### get a training set in conll format (dev will be seed, but irrelevant)
		# cat $workingDir/$seed $workingDir/$alwaysTrain > dataset/train.crf
		# python $workingDir/Scripts/converter.py dataset/train.crf crf conll dataset/train.conll
		# python $workingDir/Scripts/converter.py $workingDir/$seed crf conll dataset/dev.conll
		# ### conll format unannotated data to be the test
		# python $workingDir/Scripts/converter.py $workingDir/$unannotated crf conll dataset/test.conll

		# ### train
		# python train.py --train dataset/train.conll --dev dataset/dev.conll --test dataset/dev.conll --model_loc MyModel --path_to_tagger $PWD # --n_epochs 2 # remove the n_epochs after finish debugging

		# ### test



else
	echo "UNSUPPORTED TAGGER VARIABLE!"
	echo $tagger 
	echo
fi



### align with unannotated
awk 'FNR==NR{a[NR]=$1;next}{$1=a[FNR]}1' $predictions $unannotated > $predictions.aligned
### build the full annotated corpus
cat $seed $alwaysTrain $predictions.aligned > $final_corpus
echo
echo "Full Annotated Corpus (Manual + Automatic Predictions)"
echo $final_corpus
echo
### get the final list of named entities
python Scripts/get_NE_list.py Results/fullCorpus.final.txt > $final_list
echo "Full List of Entities (Manually or Automatically Identified)"
echo $final_list
echo
