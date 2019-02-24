# HER: Humanities Entity Recognizer

HER is an easy-to-use, active learning tool designed to help Digital Humanists efficiently and effectively automate the identification of entities like persons or places in large text corpora. It offers a *whitebox* solution for robust handling of different types of entities, different languages, styles, and domains, and varying levels of structure in texts.

## Overview

The following outlines the active learning process using Her:

* You give HER all relevant texts and define the types of entities you want to identify in said texts
* HER prompts you to annotate these types of entities in a small *seed* sample text
* Based on said seed, the system ranks all sentences in the corpus that you have not yet annotated based on how useful they should be for helping HER to learn to identify these entity types automatically
* HER requests you to start annotating the ranked sentences
* You can stop annotating at any time and check if HER has learned to identify entities with acceptable accuracy by requesting HER to attempt to identify entities in the remaining unannotated sentences and manually evaluating a sample for quality
* Based on said quality, you decide if your manual labor seems more valuably spent annotating more sentences or post editing said outputs
* Once you're happy with the quality of HER's predicted entity labels, you can use your fully labeled corpus for whatever application you had in mind.

## Quick Start Demo

This limited demo shows you how to identify geographical place names in a sample corpus of French texts extracted from [FranText](https://www.frantext.fr).

To address the wide range of use cases for which HER is designed---including corpora with previously existing partial annotation, presence or lack of gazetteers, diverse orthographies, non-traditional labels, etc.---and for more information regarding data/annotation formatting, **please consult the relevant sections of the [User Manual](https://github.com/alexerdmann/HER/blob/master/Scripts/Docs/Manual.md), which assumes minimal to no computational background from readers**.

### Step 0: Set Up

Define the language (for tokenization purposes only), labels you plan to use to denote all types of entities you want to recognize (separated by an underscore if more than one), an algorithm for active learning, and a name for your working directory.

```
lg=fr
entities=GEO
sortMethod=preTag_delex
name_of_project=Demo
```

Set up the working directory.

```
sh Scripts/set_up_work_space.sh $name_of_project
cd $name_of_project
```

Load the demo texts and, if available, gazatteers, which by the way, I acknowledge is probably spelled wrong.

```
cp ../Data/Original/French.zip Data/. 
unzip Data/French.zip
mv French/* Data/Original/.
rm -rf French Data/French.zip
cp ../Data/Gazatteers/GEO.gaz Data/Gazatteers/GEO.gaz
```

### Step 1: Preparing Your Texts

Normally, you would use the script *Scripts/preprocess.py* for this step, but since you may not speak French, I'll use an *ad hoc* script that preserves pre-existing geospatial annotations. The final output is stored in *Data/Prepared/fullCorpus.txt*.

```
sh Scripts/prepare_original_texts.sh Scripts/Experiments/preprocess_Davids_data.py $lg 2> log.txt
```

### Step 2: Get A Seed

Decide how many sentences will be in your random seed sample and get the sample.

```
seed_size=300
python Scripts/rankSents.py -corpus Data/Prepared/fullCorpus.txt -sort_method random_seed -topXsents $seed_size -output Data/Splits/fullCorpus.seed-$seed_size -annotate True
```

### Step 3 Manual Annotation Of The Seed

We can skip this because I told you the demo corpus comes with pre-existing geospatial annotation, but, normally, you might consider using gazetteers to make suggestions to expedite the tagging, like so:

```
python Scripts/pre-tag_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed $entities Data/Gazatteers/* > Data/Splits/fullCorpus.seed-$seed_size.seed.preTagged
mv Data/Splits/fullCorpus.seed-$seed_size.seed.preTagged Data/Splits/fullCorpus.seed-$seed_size.seed
```

Then you would manually correct the *gazetteer pre-tagged* sample.
Once you've finished annotating your seed, you should update the gazetteers to include any newly encountered named entities.

```
python Scripts/update_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed Data/Gazatteers/*
```

### Step 4: Feature Engineering And Training A Seed Model

Use the seed to determine which features are relevant to identifying entities in your corpus.

```
python Scripts/cross_validation.py -testable Data/Splits/fullCorpus.seed-$seed_size.seed -fullCorpus Data/Prepared/fullCorpus.txt -identify_best_feats True -train_best True -unannotated Data/Splits/fullCorpus.seed-$seed_size.unannotated
```

Train a named entity recognition model on just the seed and use it to predict entities in the rest of the corpus. Save the results so you can evaluate improvement later on in the active learning process as more annotation is completed.

```
sh Scripts/tag_get_final_results.sh 0 Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt crf
mkdir Results/Gazatteers
cp Data/Gazatteers/* Results/Gazatteers/.
mkdir Results_seed
mv Results/* Results_seed
```

### Step 5: Predict And Rank Unannotated Sentences By Informativity

Use Active Learning to determine which unannotated sentences will most improve the model if annotated.

```
sh Scripts/tag_and_rank.sh Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.seed.fts $sortMethod Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod None $entities
```

### Step 6: Manually Annotate Ranked Sentences And Periodically Update Model

Again, we're not manually annotating in the demo, but you might want to pretag again before annotating, like so:

```
python Scripts/pre-tag_gazatteers.py Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities Data/Gazatteers/* > Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged
mv Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod
```

Then you would annotate as much of the file *Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod* as suits your needs, for now, let's say we annotated 5,000 lines. Periodically, you will want to stop, update the model and gazetteers, re-rank the remaining unannotated sentences based on the new annotations, and evaluate model accuracy, like so:

```
lines_annotated=5000
sh Scripts/update_crossValidate_rerank.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt $sortMethod Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities
python Scripts/update_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Gazatteers/*
sh Scripts/tag_get_final_results.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt crf
mkdir Results/Gazatteers
cp Data/Gazatteers/* Results/Gazatteers/.
mkdir Results_seed_plus_5000
mv Results/* Results_seed_plus_5000
```

You can now check out *Results_seed_plus_5000/fullCorpus.final.txt*, *Results_seed_plus_5000/fullCorpus.final-list.txt*, and the files in *Results_seed_plus_5000/Gazatteers/* and compare to the corresponding files in *Results_seed/* to guage performance and improvement. This will help you decide if you want to repeat Step 6 and how many additional lines you should annotate if you do.

For the sake of brevity, we use a CRF-based model for this demo, though you can check the [User Manual](https://github.com/alexerdmann/HER/blob/master/Scripts/Docs/Manual.md) for other supported models which will train slower but could perform better once you've annotated more data.

### Step 7: Take Off Your Digital Hat And Put On Your Humanist Hat

Your done.. go use your annotated corpus for something cool.

## Acknowledgments

HER is under continuous development supported by the [Herodotos Project](https://u.osu.edu/herodotos/) and [NYU-PSL Spatial Humanities Partnership](https://wp.nyu.edu/nyupslgeo/). We gratefully acknowledge [Moses](http://www.statmt.org/moses/), from whom we borrowed some code, and [Abraham](https://en.wikipedia.org/wiki/Abraham), from whom we derived three major religions. 

If you find HER useful, please cite our forthcoming publication:

* Alexander Erdmann, David Joseph Wrisley, Benjamin Allen, Christopher Brown, Sophie Cohen Bodénès, Micha Elsner, Yukun Feng, Brian Joseph, Béatrice Joyeaux-Prunel and Marie-Catherine de Marneffe. 2019. “[Practical, Efficient, and Customizable Active Learning for Named Entity Recognition in the Digital Humanities](https://github.com/alexerdmann/HER/blob/master/HER_NAACL2019_preprint.pdf).” In *Proceedings of North American Association of Computational Linguistics (NAACL 2019)*. Minneapolis, Minnesota.

You may also be interested in the previous work upon which HER builds:

* Alexander Erdmann, Christopher Brown, Brian Joseph, Mark Janse, Petra Ajaka, Micha Elsner, Marie-Catherine de Marneffe. 2016. “[Challenges and Solutions for Latin Named Entity Recognition](http://www.aclweb.org/anthology/W16-4012).” In *Pro- ceedings of the Language Technologies for the Digital Humanities Workshop* in conjunction with *The 26th International Conference on Computational Linguistics (COLING 2016)*. Osaka, Japan.

Please contact Alex Erdmann (ae1541@nyu.edu) with any questions, bug fixes, or dating advice.
