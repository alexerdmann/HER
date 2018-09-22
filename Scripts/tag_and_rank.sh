modelLocation=$1
test=$2
probs=$3
unannotated=$4
seed=$5
sortMethod=$6
output=$7
alwaysTrain=$8
entities=$9

# tag
crfsuite tag -p -i -m $modelLocation $test > $probs

# rank
python Scripts/rankSents.py -corpus $unannotated -seed $seed -sort_method $sortMethod -predictions $probs -output $output -alwaysTrain $alwaysTrain -entities $entities
