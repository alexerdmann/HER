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



# divide annotated ranked sentences
head -$lines_annotated $rankedSents >> $alwaysTrain
# from yet unannotated sentences
tail -n +$start_unannotated $rankedSents > $unannotated
### cross validate (which will predict the accuracy as well)
python Scripts/cross_validation.py -testable $seed -alwaysTrain $alwaysTrain -fullCorpus $fullCorpus -identify_best_feats True -train_best True -unannotated $unannotated
### tag
crfsuite tag -m Models/CRF/best_seed.cls $unannotated.fts > $predictions
### align with unannotated
awk 'FNR==NR{a[NR]=$1;next}{$1=a[FNR]}1' $predictions $unannotated > $predictions.aligned
### build the full annotated corpus
cat $seed $alwaysTrain $predictions.aligned > $final_corpus
echo "FINAL CORPUS (MANUAL ANNOTATIONS + AUTOMATICALLY PREDICTED ANNOTATIONS):"
echo $final_corpus
echo
### get the final list of named entities
python Scripts/get_NE_list.py Results/fullCorpus.final.txt > $final_list
echo "FINAL NAMED ENTITY LIST:"
echo $final_list
echo
