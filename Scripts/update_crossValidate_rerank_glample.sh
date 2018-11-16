lines_annotated=$1
start_unannotated=$(($lines_annotated + 1))
rankedSents=$2
alwaysTrain=$3
unannotated=$4
seed=$5
fullCorpus=$6
sortMethod=$7
predictions=$8
output=$9
entities="${10}"
multiple_tests="${11}"


# divide annotated ranked sentences
head -$lines_annotated $rankedSents >> $alwaysTrain
# from yet unannotated sentences
tail -n +$start_unannotated $rankedSents > $unannotated
sh Scripts/crossValidate_tag_glample.sh $seed $alwaysTrain $unannotated $fullCorpus $multiple_tests
# This will overwrite your ranked sentences file, so you can start annotating the new fullCorpus.seed-$seed_size.$sortMethod from line 1
python Scripts/rankSents.py -corpus $unannotated -seed $seed -alwaysTrain $alwaysTrain -sort_method $sortMethod -predictions $predictions -output $output -entities $entities
