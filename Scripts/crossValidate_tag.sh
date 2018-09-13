testable=$1
alwaysTrain=$2
unannotated=$3
fullCorpus=$4

### cross validate
python Scripts/cross_validation.py -testable $testable -alwaysTrain $alwaysTrain -fullCorpus $fullCorpus -identify_best_feats True -train_best True -unannotated $unannotated

### tag
crfsuite tag -p -i -m Models/CRF/best_seed.cls $unannotated.fts > $unannotated.probs


