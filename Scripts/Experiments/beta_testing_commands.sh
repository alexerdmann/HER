git clone https://github.com/alexerdmann/HER
cd HER

name_of_project=myExperiment
sh Scripts/set_up_work_space.sh $name_of_project
cd $name_of_project

cp ../Data/Original/French.zip Data/.
unzip Data/French.zip
mv French/* Data/Original/.
rm -rf French
rm Data/French.zip
cp ../Data/Gazatteers/GEO.gaz Data/Gazatteers/GEO.gaz

sh Scripts/prepare_original_texts.sh Scripts/Useful/preprocess_Davids_data.py $lg 

seed_size=200

python Scripts/pre-tag_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed $entities Data/Gazatteers/* > Data/Splits/fullCorpus.seed-$seed_size.seed.preTagged
mv Data/Splits/fullCorpus.seed-$seed_size.seed.preTagged Data/Splits/fullCorpus.seed-$seed_size.seed

cut -f1 Data/Splits/fullCorpus.seed-$seed_size.seed | sort -u

python Scripts/update_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed Data/Gazatteers/*

python Scripts/cross_validation.py -testable Data/Splits/fullCorpus.seed-$seed_size.seed -fullCorpus Data/Prepared/fullCorpus.txt -identify_best_feats True -train_best True -unannotated Data/Splits/fullCorpus.seed-$seed_size.unannotated

sh Scripts/tag_get_final_results.sh 0 Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt crf
mkdir Results/Gazatteers
cp Data/Gazatteers/* Results/Gazatteers/.

mkdir Results_seed
mv Results/* Results_seed

sh Scripts/tag_and_rank.sh Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.seed.fts $sortMethod Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod None $entities

python Scripts/pre-tag_gazatteers.py Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities Data/Gazatteers/* > Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged
mv Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod

cut -f1 Data/Splits/fullCorpus.seed-$seed_size.seed | sort -u

python Scripts/update_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed Data/Gazatteers/*

lines_annotated=2000

sh Scripts/update_crossValidate_rerank.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt $sortMethod Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities

sh Scripts/tag_get_final_results.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt crf
mkdir Results/Gazatteers
cp Data/Gazatteers/* Results/Gazatteers/.

mkdir Results_seed_plus_2000
mv Results/* Results_seed_plus_2000

python Scripts/pre-tag_gazatteers.py Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities Data/Gazatteers/* > Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged
mv Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod

cut -f1 Data/Splits/fullCorpus.seed-$seed_size.seed | sort -u

python Scripts/update_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed Data/Gazatteers/*

lines_annotated=10000

sh Scripts/update_crossValidate_rerank.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt $sortMethod Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities

sh Scripts/tag_get_final_results.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt crf
mkdir Results/Gazatteers
cp Data/Gazatteers/* Results/Gazatteers/.

mkdir Results_seed_plus_12000
mv Results/* Results_seed_plus_12000
