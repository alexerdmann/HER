name_of_project=$1
seed_size=$2
sort_method=$3
processing_script=$4
lg=$5


# set up work space
for dir in Data Models Scripts Results; do cp -r ../$dir .; done

# prepare texts
sh Scripts/prepare_original_texts.sh $processing_script $lg 

# get seed
python Scripts/rankSents.py -corpus Data/Prepared/fullCorpus.txt -sort_method random_seed -topXsents $seed_size -output Data/Splits/fullCorpus.seed-$seed_size -annotate True

# choose best feature set
python Scripts/cross_validation.py -testable Data/Splits/fullCorpus.seed-$seed_size.seed -fullCorpus Data/Prepared/fullCorpus.txt -identify_best_feats True -train_best True -unannotated Data/Splits/fullCorpus.seed-$seed_size.unannotated

# tag unannotated data
crfsuite tag -m Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts > Data/Splits/predictions_from_seed.txt
