seed_size=$1
sortMethod=$2
lines_annotated=$3
entities=$4
multiple_tests=$5

# tag and rank sentences
sh Scripts/tag_and_rank.sh Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed $sortMethod Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod None $entities

# update your gazatteers based on the annotation you've just done
python Scripts/update_gazatteers.py Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Gazatteers/*

# choose best feature set and re-rank the unannotated data
sh Scripts/update_crossValidate_rerank_glample.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt $sortMethod Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities $multiple_tests

# tag unannotated data
crfsuite tag -m Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts > Data/Splits/predictions_from_seed.txt
