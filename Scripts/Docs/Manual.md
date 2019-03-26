# HER: Humanities Entity Recognizer

HER is an easy-to-use, active learning tool designed to help Digital Humanists efficiently and effectively automate the identification of entities like persons or places in large text corpora. It robustly handles different types of entities, different languages, styles, and domains, and varying levels of structure in texts.

## Overview

The following outlines the active learning process using Her:

* You give HER all relevant texts and define the types of entities you want to identify in said texts
* HER prompts you to annotate these types of entities in a small *seed* sample text
* Based on said seed, the system ranks all sentences in the corpus that you have not yet annotated based on how useful they should be for helping HER to learn to identify these entity types automatically
* HER requests you to start annotating the ranked sentences
* You can stop annotating at any time and check if HER has learned to identify entities with acceptable accuracy by requesting HER to attempt to identify entities in the remaining unannotated sentences and manually evaluating a sample for quality
* Based on said quality, you decide if your manual labor seems more valuably spent annotating more sentences or post editing said outputs
* Once you're happy with the quality of HER's predicted entity labels, you can use your fully labeled corpus for whatever application you had in mind.

## Getting Started

First things first, you need to download the HER repository. If you have *git* installed, run the commands below (you can install git via these [instructions](https://www.linode.com/docs/development/version-control/how-to-install-git-on-linux-mac-and-windows/))

```
git clone https://github.com/alexerdmann/HER
cd HER
```

Otherwise, download HER from this [url](https://github.com/alexerdmann/HER) and navigate to the downloaded HER directory in the terminal by typing *cd* followed by a space, then dragging the HER directory into your terminal window, then pressing enter.

Make sure that you are always in the *HER/* directory or the appropriate subdirectory of *HER/* anytime you run a command going forward, as you may not return to the same directory when you open a new terminal.

### Prerequisites

Check out the [Prerequisites](https://github.com/alexerdmann/HER/blob/master/Scripts/Docs/Prerequisites.md) page for information on how to make sure HER will run on your machine.

### Defining Parameters

Tell HER what language you're working on, what entity labels you want to use, and what algorithm you want HER to use to find more of those entities. Check out the [Parameters](https://github.com/alexerdmann/HER/blob/master/Scripts/Docs/Defining_Parameters.md) page for details on how to do this.

### Setting Up Your Work Space

Set up is simple. Just come up with a name for your project and run the commands below.

```
name_of_project=[name-of-your-project]
sh Scripts/set_up_work_space.sh $name_of_project
cd $name_of_project
```

Now, from this newly created directory with the name you just came up with, cp all the files from your corpus into *Data/Original/* and if you have any gazetteers, put them in *Data/Gazatteers/*. For crucial details regarding file naming and formatting conventions, check out the [Set Up](https://github.com/alexerdmann/HER/blob/master/Scripts/Docs/Set_Up.md) page.

And for the record, I acknowledge that I have no idea how to spell gazatteer; I'm just leaning into it at this point.

## Usage

Once you've loaded your data and defined your *name_of_project*, *lg*, *entities*, and *sortMethod* variables, we're ready to get started!

### Step 1: Preparing Your Texts

If any of your texts include previous entity annotations that you want to leverage, open up the script located at *Scripts/Experiments/preprocess_Davids_data.py* to see how I incorporated previously annotated texts in my experiments. My comments in the script should help you figure out how to adapt this script to preserve any pre-existing annotations in your own data. Once you've adapted the script accordingly, save it as *Scripts/preprocess.py*.

If you don't have previously annotated texts or the annotations are not useful, the original *Scripts/preprocess.py* script will suite you fine.

Now, run the following command:

```
sh Scripts/prepare_original_texts.sh Scripts/preprocess.py $lg 2> log.txt
```

This takes all your texts in *Data/Original/*, regardless of extension or amount of structure and performs the following:
* *Preprocessing*, it parses relevant meta data structured in the texts
* *Tokenization*, it allows the model to learn that certain words are present even if they appear with adjoining characters instead of being delimited by spaces
* *Preparation*, it formats the texts to be readable by CRFsuite, the machine learning system that guides Active Learning, i.e., it helps determine which sentences are most useful for annotation.

The final output of this script is a document containing the entire fully prepared corpus in one file: *Data/Prepared/fullCorpus.txt*

### Step 2: Get A Seed

We help HER get started on the path to learning how to identify these entities by manually annotating, or marking their presence, in a small *seed* sample of sentences from the corpus.

#### Assuming that you have no previously annotated data

We will randomly extract sentences to use in your seed. This is preferred, because a deterministic seed may reflect a systematically biased distribution of named entities in the corpus.

The ideal seed size depends on a number of factors. We can easily adjust seed size later, but for now, let's set it to 200 sentences as follows:

```
seed_size=200
```

If you have gazatteers with lots of helpful entities from your corpus, annotation will go more easily, which might motivate you to do a larger seed, though it also might mean that you don't need such a large seed to get HER going.

If your corpus is very densely packed with entities, you could probably redefine *seed_size* to be less than 200 (and *vice versa*), however, if the types of entities you want to identify are many or finely granular, you might want to increase *seed_size* (and *vice versa*).

The following command will actually extract the seed (whose size we can still edit in Step 3:

```
python Scripts/rankSents.py -corpus Data/Prepared/fullCorpus.txt -sort_method random_seed -topXsents $seed_size -output Data/Splits/fullCorpus.seed-$seed_size -annotate True
```

#### If you *do* have previously annotated data or simply do not want your seed to be random

Follow the [Deterministic Seed Instructions](https://github.com/alexerdmann/HER/blob/master/Scripts/Docs/Deterministic_Seed.md) before proceeding to Step 3.

### Step 3 Manual Annotation Of The Seed

The seed sentences are located at: *Data/Splits/fullCorpus.seed-$seed_size.seed*. The file contains one word (well really token, because punctuation and clitics will likely take their own lines) per line with a single blank line between sentences. The line is tab separated with the *label* (also refered to as a *tag*) in the first column, the word itself in the second, and any other features we might later generate will occupy subsequent columns. By default, the *label* will be *0* for every word, meaning that it is not an entity or at least has not been annotated (manually not automatically) as one yet (if you are familiar with the *BIO* annotation scheme, please note that we are using a zero (0), not a capital letter (O), though this should probably be changed soon in order to fully conform to the popular *BIO* scheme).

In this step, we will identify all words that are entities and change their labels, systematically. Specifically, the label will be composed by joining the relevant entity type (necessarily one of the types defined in *entities*) and the letter *B* or *I* with a dash. For example, if I come across the word *Paris* in my corpus, I would want to label it as *GEO-B*, where I use *B* to indicate that it is the beginning of an entity. If I come across the words *de*, *New*, *York*, and *.* in a sequence, I would want to label them *0*, *GEO-B*, *GEO-I*, and *0* respectively, where *I* denotes a non-initial member of an ongoing entity. 

To expedite the manual annotation, let's first pretag this file using any pre-existing gazatteers.

```
python Scripts/pre-tag_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed $entities Data/Gazatteers/* > Data/Splits/fullCorpus.seed-$seed_size.seed.preTagged
mv Data/Splits/fullCorpus.seed-$seed_size.seed.preTagged Data/Splits/fullCorpus.seed-$seed_size.seed
```

Now go ahead and start annotating the seed using a *plain text editor* like [Atom](https://atom.io) or [Sublime](https://www.sublimetext.com) - not Word! Keep in mind that this may involve correcting some non-*0* labels whenever the pretagging step made a mistake. If the pretagging step makes a lot of consistent mistakes due to bad entries in the gazatteer, consider removing those bad entries from the relevant gazatteer files and restarting this Step. If the pretagging isn't speeding things up at all because the gazatteers are too bad to be worth addressing like this, remember that the two lines of code above are not necessary - you can always skip them - they are only meant make your annotation easier.

*Always back up your annotation somewhere!*

Ideally, you might want at least 60-100 named entities in your seed set. You might want more if you have a lot of fine grained entity types or your minority types don't show up at all in the seed, but you also might want less if you have good gazatteers for any infrequent entity types.

If you find less entities than seems necessary in your seed, just cut sentences from Data/Splits/fullCorpus.seed-$seed_size.unannotated and paste them into Data/Splits/fullCorpus.seed-$seed_size.seed until you achieve a suitable number of named entities. If the converse occurs and you find that you have far more than the requisite number of entities before finishing annotating the seed, simply cut the remaining sentences from Data/Splits/fullCorpus.seed-$seed_size.seed into Data/Splits/fullCorpus.seed-$seed_size.unannotated. A larger seed is always better, so certainly don't disclude previously annotated data unless you think some domain or style difference might cause it to be extremely unrepresentative of the distribution of entities elsewhere in the corpus. But you also may not want to annotate the whole seed because your annotation time will be more efficiently spent on an upcoming annotation step once we start Active Learning, provided the seed was big enough to get HER going.

*Don't update $seed_size to reflect the number of sentences that you actually ended up annotating.. It is used for file naming purposes. The fact that it may not reflect the actual seed size is not important.*

Upon completing your annotation, sanity check your data to make sure you made no typos. Run the following command to identify all unique labels in your seed and double check that they are all well formed as either *0* or *[allowable-entity-name]-[B-or-I]*. If you made any typos, search for them in the seed file and correct them.

```
cut -f1 Data/Splits/fullCorpus.seed-$seed_size.seed | sort -u
```

Once you've ensured your seed is well formed, use it to update and/or create your gazatteers based on this new information.

```
python Scripts/update_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed Data/Gazatteers/*
```

### Step 4: Feature Engineering And Training A Seed Model

Run the command below which will perform a technique called cross-validation to determine the most useful features for locating named entities in your data. In order to make this run fairly quickly, I've limited the candidate features to those that are cross linguistically most likely to be useful in identifying named entities. For maximal robustness, consider commenting in line 168 of *Scripts/cross_validation.py* (by deleting the *#* at the beginning of the line) and using a larger subset of the possible features than what is presented in line 167.

```
python Scripts/cross_validation.py -testable Data/Splits/fullCorpus.seed-$seed_size.seed -fullCorpus Data/Prepared/fullCorpus.txt -identify_best_feats True -train_best True -unannotated Data/Splits/fullCorpus.seed-$seed_size.unannotated
```

*Depending on the chosen* sortMethod *, this script may claim to predict accuracy on yet unannotated texts. This functionality has yet to be completed though so take these numbers with a grain of salt.*

Let's check how the model is doing with just a small seed set to train on. The command below will take a Conditional Random Field (CRF) model trained using the best features identified via cross validation and use it to predict labels for the yet un(manually)annotated corpus. It will combine the manually and automatically annotated halves into a single file for your viewing pleasure *Results/fullCorpus.final.txt* and produce a list of all unique entities found in said file *Results/fullCorpus.final-list.txt*. Lastly, all gazatteers, in their present state, will be saved in *Results/Gazatteers/*.

```
sh Scripts/tag_get_final_results.sh 0 Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt crf
mkdir Results/Gazatteers
cp Data/Gazatteers/* Results/Gazatteers/.
```

*See Step 6 for a discussion of other supported models besides CRF's and why you might want to use them later on*

Before we move on and improve on these results, let's save them somewhere specific so we can compare to them later.

```
mkdir Results_seed
mv Results/* Results_seed
```

### Step 5: Predict And Rank Unannotated Sentences By Informativity

We will now use information from the annotated seed to identify the most useful sentences to annotate going forward, based on our chosen *sortMethod*.

```
sh Scripts/tag_and_rank.sh Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.seed.fts $sortMethod Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod None $entities
```

The *preTag_delex* sorting method is so successful here because it leverages gazatteers to identify non-lexical features of words most predictive of entity status in words that have yet to be encounered in annotation. It also biases the model toward making precision errors instead of recall errors, as this helps the model better generalize to unknown words. Furthermore, recall errors in a list are far quicker to manually post edit than precision errors.

### Step 6: Manually Annotate Ranked Sentences And Periodically Update Model

Again, let's pretag before annotating to expedite the process. If you didn't have a gazatteer to start, you should after annotating the seed.

```
python Scripts/pre-tag_gazatteers.py Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities Data/Gazatteers/* > Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged
mv Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod
```

Annotate as much of the file *Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod* as suits your needs. If you find that the file is too large to open in your text editor, try annotating a in a file that only contains the first few thousand lines. You can create such a file with the following command:

```
head -10000 Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod > annotate_this.txt
```

Of course, when you're done, make sure you write over the first however many lines with your new annotation, which you can do as follows:

```
tail -n +10001 Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod > rest.txt
cat annotate_this.txt rest.txt > Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod
```

The sentences in *Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod* have been specifically ordered such the most useful and hopefully named entity rich sentences are located in the beginning of the file. If at some point you realize that the model is performing poorly on infrequent, *minority* labels, and they are not being incorporated in the sentences favored by the Active Learning algorithm for annotation, you can help the model to learn these entities by artificially re-ranking sentences. To do this, search the *Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod* file for some words that you expect to take the problematic minority label in your corpus and cut a few sentences including such words from wherever they are located in the file and paste that at the front of the file, to be annotated immediately. You can use similar tactics if you find that a specific genre, author, style, or domain is being systematically dispreferred by the Active Learning sentence sorting algorithm. 

Upon completing your annotation, sanity check your data again to make sure you made no typos.

```
cut -f1 Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod | sort -u
```

If it appears that you made any typos, search for them in the seed file and correct them before updating your gazatteers.

```
python Scripts/update_gazatteers.py Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Gazatteers/*
```

The rest of Step 6 shows you how to re-evaluate the output lists of entities and full annotated corpus after updating your model with the most recent manual annotation. It is not necessary, but is easy to do and might be a good idea to perform anytime you want to take a break from annotating for a while.

First, record the line number that is the blank line after the last sentence you annotated in *Data/Splits/fullCorpus.seed-$seed_size.seed*. By way of example, let's say that line is 2000 for me. I would run the following command:

```	
lines_annotated=2000
```

Then update the model and re-rank the remaining sentences to be manually annotated later.

```
sh Scripts/update_crossValidate_rerank.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt $sortMethod Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities
```

Let's check how the model is doing compared to how it was doing last time. 

Now, the first line of the code below (starting with *sh Scripts/tag_get_final_results.sh*...) specifies that, again, we will be using a CRF architecture for our model. However, you can change the last argument in that line from *crf* to *bilstm-crf* or *cnn-bilstm* to experiment with these two alternative *neural network* architectures (full disclosure, I haven't finished incorporating the CNN-BiLSTM yet, but you BiLSTM-CRF is ready to go). As demonstrated in Erdmann et al. (*under review*), there are two factors affecting whether you should stick with the CRF architecture or adopt the [BiLSTM-CRF](https://arxiv.org/pdf/1603.01360.pdf) or [CNN-BiLSTM](https://arxiv.org/pdf/1707.05928.pdf) architecture:

* The intended application of the model you're training
* The amount of already manually annotated data you are using to train this model

If you're sole purpose in training this model is to get accurate entity labels for the corpus you've provided, it seems that no neural network will outperform the CRF, however, if you plan to use this model to generalize to other data in the future that was not included in the corpus you provided to HER to do Active Learning on, then you need to consider the second factor, i.e., how much annotation is available for training. If the total annotation you've done so far (including the seed) is 30,000 tokens or less (I'm considering each line in the annotation files to be one token here), the CRF is probably still your best bet. Between 30 and 100,000 tokens, the CNN-BiLSTM is the best architecture. And once you have more than 100,000 tokens manually annotated, the BiLSTM-CRF architecture tends to perform the best.

Considering that, change the last argument, *crf*, to one of the other models if necessary and run the following commands (note that if you choose to use the BiLSTM-CRF, you will probably need to first enter the command ```chmod +x ../tagger/evaluation/conlleval``` in order to make sure it runs smoothly): 

```
sh Scripts/tag_get_final_results.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt crf
mkdir Results/Gazatteers
cp Data/Gazatteers/* Results/Gazatteers/.
```

Check out *Results/fullCorpus.final.txt*, *Results/fullCorpus.final-list.txt*, and the files in *Results/Gazatteers/* and save your most recent output so you can reference it again later if you want to make more comparisons.

```
mkdir Results_seed_plus_[sum-of-all-lines-annotated_after_the_seed]
mv Results/* Results_seed_plus_[sum-of-all-lines-annotated_after_the_seed]
```

Consider how much improvement you've gotten since last time relative to the amount of time you've spent annotating. You can guage this by manually evaluating samples from each of the files in the Results directories. If it seems you've finally reached the point where the marginal benefit of time spent manually annotating more sentences is less than the marginal benefit of time spent manually post editing the outputs that you're interested in (either the lists or the annotated corpus or both), it's probably time to quit.

Otherwise, repeat Step 6 as needed.

### Step 7: Apply the Trained Model

The final tagged corpus and final list of named entities are aggregate over the entire corpus you provided at the beginning and sentences/entities are not listed in any particular order. To project the named entity labels directly onto the individual texts making up your corpus, run the command below. The tagged individual texts will be placed into *Data/Prepared/* and they will all have the extension *.tagged*.

```
python Scripts/project_tags.py Results_seed_plus_[sum-of-all-lines-annotated_after_the_seed]/fullCorpus.final.txt Data/Prepared/*
```

If you want to get a list of unique named entities found in every individual text from your corpus, you can follow the above command with the following one, which generates files in the same *Data/Prepared/* directory ending in the extension *.list* containing the relevant lists.

```
for f in Data/Prepared/*.tagged; do python Scripts/get_NE_list.py $f > $f.list; done
```

It may also be desirable to use your trained model to tag new texts later on that were not part of your original corpus. You can re-use your tagger at any time to label named entities in a new text with the commands below. Just specify what new text you want to tag, whether you used the crf or bilstm-crf tagger architecture, and where that trained model is located, as demonstrated. For crf, the model will, by default, be located at *Models/CRF/best_seed.cls*, whereas the trained bilstm-crf model is stored by default at *../tagger/models/MyModel/*.

```
new_text=[path_to_text_you_want_to_tag]
architecture=[either_crf_or_bilstm-crf]
model=[either_Models/CRF/best_seed.cls_or_../tagger/models/MyModel/]

python Scripts/tag_text_outside_fullCorpus.py $model $new_text $lg $architecture Data/Prepared/fullCorpus.txt Models/CRF/best_seed.featSet
```

Running these commands will create a new director *Data/External/* containing a preprocessed version of your new text along with a file with the extension *.aligned* which has been tagged by your trained tagger. Another file with the extension *.list* contains all the unique named entities that the tagger discovered in your new text.

### Step 8: Take Off Your Digital Hat And Put On Your Humanist Hat

Regardless of how much post editing lies in your future, I hope HER has served you well and the output of this process has facilitated your project goals. Godspeed!

## Acknowledgments

HER is under continuous development supported by the [Herodotos Project](https://u.osu.edu/herodotos/) and [NYU-PSL Spatial Humanities Partnership](https://wp.nyu.edu/nyupslgeo/). We gratefully acknowledge [Moses](http://www.statmt.org/moses/), from whom we borrowed some code, and [Abraham](https://en.wikipedia.org/wiki/Abraham), from whom we derived three major religions. 

If you find HER useful, please cite the below work from which the system was adapted:

* Erdmann et al., 2016 [Challenges and Solutions for Latin Named Entity Recognition](http://www.aclweb.org/anthology/W16-4012)

*Please contact Alex Erdmann (ae1541@nyu.edu) with any questions, bug fixes, or dating advice.*
