seed_size=$1
sortMethod=$2
lines_annotated=$3

# tag and rank sentences
sh Scripts/tag_and_rank.sh Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed $sortMethod Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod 

# choose best feature set and re-rank the unannotated data
sh Scripts/update_crossValidate_rerank.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt $sortMethod Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod

# tag unannotated data
crfsuite tag -m Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts > Data/Splits/predictions_from_seed.txt