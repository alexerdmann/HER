# HER: Humanities Entity Recognizer

HER is an easy-to-use tool designed to help Digital Humanists automate much of the process of identifying entities like persons or places in large text corpora. She robustly handles different types of entities, different languages, styles, and domains, and varying levels of structure in texts.

## Getting Started

### Overview

HER will walk you through the process of tailoring a system to automatically identify and distinguish whatever types of entities you desire in whatever texts you provide her with. The process, generally speaking, will be as follows:

* You give HER all relevant data and define the types of entities you want to identify in said data
* She prompts you to annotate these types of entities in a small *seed* sample text
* Based on said seed, she ranks all sentences in the corpus that you have not yet annotated based on how useful they should be for helping HER to learn to identify these entity types automatically
* She requests you to start annotating the ranked sentences
* You can stop annotating at any time and check if HER has learned to identify entities with acceptable accuracy by requesting HER to attempt to automatically find all entities in the remaining unannotated sentences and compile a list of all unique, identified entities (both manually and automatically identified)
* You will evaluate the quality of these outputs and decide if your manual labor seems more valuably spent annotating more sentences or post editing said outputs
* You will rejoice over the great efficiency with which you identified all these entities and sally forth to apply them to whatever nefarious application you're planning

### Prerequisites

#### Human Capital

* If you're not familiar with best practices for annotating named entities or are not sure what that really means, it would be good to outline some consistent guidelines for how you will handle issues like ambiguity or embedded named entities ([This will link to a relevant site one day](https://www.amazon.com/USA-Tees-Merica-Dinosaur-Cowboy/dp/B073XXLVNT/ref=pd_lpo_sbs_193_img_0?_encoding=UTF8&refRID=P4PT1M97YJY9CS5H93J3)).

* HER assumes that the user is not mortified by the thought of using a terminal or working from the command line. If you don't know what that means or you've never used the terminal, have no fear! This README will walk you through most everything you need to know and you can consult the Programming Historian's [Introduction to the Command Line](https://programminghistorian.org/en/lessons/intro-to-bash) to fill in any gaps.

#### Operating System

HER was developed and tested on Mac. It should run on any Linux system, though Windows will be problematic. Verifying and addressing this is on the to-do list.

#### CRFsuite

We will use the CRFsuite package behind-the-scenes to handle some of the machine learning. It can be installed on a Mac via *Homebrew*. If you don't already have Homebrew installed, run the following command:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

With Homebrew already installed, CRFsuite can be installed on a Mac as follows:

```
brew tap brewsci/science
brew install crfsuite
```

To install on other platforms, check the CRFsuite host [site](http://www.chokkan.org/software/crfsuite/).

CRFsuite has been successfully installed if you can run the below command without generating an error message

```
crfsuite -h
```

#### Python 3

If the below command tells you that you are using a version of Python less than 3.0, you need to get [Python 3](https://www.python.org/download/releases/3.0/) and/or make it the defualt version of Python.

```
python -V
```

The easiest way to get Python 3 is to create an *environment* using the *Miniconda* tool:
* Download Miniconda from this [url](https://conda.io/miniconda.html`)
* Verify that you have downloaded a file that starts with *Miniconda* and ends with *.sh*
* In your terminal, type *bash* followed by a space, then drag said file into your terminal window, then press enter
* Follow the prompts you are given
* When installation is finished, close the terminal and re-open it before you can use Miniconda
* Create your environment
```
conda create -n [your-environment-name] python=3.6 anaconda
```
* Activate your new environment
```
source activate [your-environment-name]
```
* Finally, verify that you are using the necessary version of Python
```
python -V
```

*Everytime you open a terminal, you will need to re-activate your environment to gauruntee that you're using the desired version of Python.*

*If you ever get a* ModuleNotFoundError *while using HER, you can usually fix it with Miniconda like so:*
```
conda install -n [your-environment-name] [whatever-module-you're-missing]
```

### Defining Parameters

Before we can start identifying named entities, we need to define some aspects of how this entity extraction is gonna go down.

#### Language

First off, we need to define a *lg* variable to tell HER what language we're dealing with. If you have multiple languages, you would probably be better off dividing your data by language and running HER multiple times, one for each language with its own data.

To set your *lg* variable, choose one of the language codes below that are supported by the Moses Tokenizer which HER will use to prepare your data:

* ca - Catalan
* cs - Czech
* de - German
* el - Modern Greek
* en - English
* es - Spanish
* fi - Finnish
* fr - French
* ga - Irish
* hu - Hungarian
* is - Icelandic
* it - Italian
* lt - Lithuanian
* lv - Latvian
* nl - Dutch
* pl - Polish
* pt - Portuguese
* ro - Romanian
* ru - Russian
* sk - Slovak
* sl - Slovenian
* sv - Swedish
* ta - Tamil
* yue - Cantonese
* zh - Mandarin

If your language is not listed, consider using *en*, as English is a safe default. English tokenization is minimalistic, essentially only separating punctuation from adjoining words, whereas many other languages' tokenization schemes aggressively break words into component meaningful parts.

I will tell HER that my data is French with the following command:

```
lg=fr
```

#### Entity Types

In order to teach a machine to help us extract entities, we need to first define what types of entities we want distinguish at what granularity. Once you do that, assign them to a variable called *entities*, separated by underscores. For example, let's say I'm interested in extracting only geographical places which I want marked in my corpus as GEO. Then I'll define *entities* as followings:
```
entities=GEO
```
If you want to identify birth places, death places, and persons' names as GEOB, GEOD, and PRS respectively, then you would define *entities* as followings:
```
entities=GEOB_GEOD_PRS
```
*Do not use any spaces, dashes, or non-ascii characters when defining* entities!

#### Annotation Optimization Algorithm

Now we also need to determine the algorithm that the computer will use to determine which sentences are more informative so that any time spent manually annotating named entities is optimally beneficial. The best, most robust algorithm is *preTag_delex*, which I will tell HER I want to use by assigning it to the variable *sortMethod*:

```
sortMethod=preTag_delex
```

Other, worse performing algorithms include:
* *hardCappedUNKs* which relies on capitalization being highly predictive of the distribution of the entities you're concerned with in your corpus
* *rapidEntityDiversity* and *rapidUncertainty* which are robust to different languages, styles, etc. like *preTag_delex* and unlike *hardCappedUNKs*, though *preTag_delex* far outperforms them
* *random* served as a useful sorting method to compare to as a baseline when i was developing the other algorithms

### Setting Up Your Work Space

If you have *git* installed, run the commands below (you can install git via these [instructions](https://www.linode.com/docs/development/version-control/how-to-install-git-on-linux-mac-and-windows/))
```
git clone https://github.com/alexerdmann/HER
cd HER
```
Otherwise, download HER from this [url](https://github.com/alexerdmann/AgnosticNER.git) and navigate to the downloaded HER directory in the terminal by typing *cd* followed by a space, then dragging the HER directory into your terminal window, then pressing enter.

Now it's time to come up with a name for your project and let HER create a folder to work in:
```
name_of_project=[name-of-your-project]
sh Scripts/set_up_work_space.sh $name_of_project
cd $name_of_project
```
*By the way, if you have used HER for one project and now want to use her for another, you don't need re-download HER from github. Simply re-define your parameters as described earlier, navigate out of the *name_of_project* subdirectory to the *HER* super-directory, run the commands immediately above, and then continue from here*

Upload all the raw texts that you want to extract named entities from
* Put texts in the *Data/Original/* folder in your new project directory
	* *Make sure you don't accidentally put them in* HER/Data/Original/
* The data you put in *Data/Original/* must be *.txt* or *.xml* files, no folders and no other formats/extensions
	* Handling HTML files is on the to-do list

Upload any relevant gazatteers (lists of entities you want to identify) if you have them (I acknowledge the misspelling but I'm not fixing it on principle).
* Gazatteer files should have one entity per line and be placed in *Data/Gazatteers/* with the filename [type-of-entity].gaz
	* A sample gazatteer is located at *../Data/Gazatteers/GEO.gaz*
	* The type of entities in the gazatteer need not exactly match any of the types of entities you want to identify, though if it does, make sure that [type-of-entity] in the filename matches exactly one of the underscore-separated entity types you defined in the *entities* variable

No filenames in either *Data/Original/* or *Data/Gazatteers/* should contain any of the following abominations:
* spaces
* non-ascii characters, e.g., accents, diacritics, chinese letters, etc.
* punctuation other than dash (-) and underscore (\_), i.e., avoid characters like quotations, comments, any form of bracket, etc.

*For the sake of example, I'll use the sample texts and sample gazatteer included with the download:*
```
cp ../Data/Original/French.zip Data/. # This copies the zipped file into the Data/ subdirectory of your new work space
unzip Data/French.zip
mv French/* Data/Original/. # Moves the unzipped data into the Data/Original/ folder
rm -rf French # Gets rid of the now empty folder the data came in
rm Data/French.zip # Gets rid of the original zipped copy of the folder
cp ../Data/Gazatteers/GEO.gaz Data/Gazatteers/GEO.gaz # Copies the sample gazatteer into your new project's Data/Gazatteers/ folder
```

## Usage

### Step 1: Preparing Your Texts

If you have any previously annotated texts, open up the script located at *Scripts/preprocess_Davids_data.py* to see how I incorporated previously annotated texts into my work so as to preserve the annotations. My comments in the script should help you figure out how to adapt it to preserve any pre-existing annotations in your own data. Once you've adapted the script accordingly, save it as *Scripts/preprocess.py*. If you don't have previously annotated texts or the annotations are not useful, the original *Scripts/preprocess.py* script will suite you fine.

Now, run the following command:
```
sh Scripts/prepare_original_texts.sh Scripts/preprocess.py $lg 2> log.txt
```

This takes all your texts in *Data/Original/*, regardless of extension or amount of structure and performs the following:
* *Preprocessing*, it parses relevant meta data structured in the texts
* *Tokenization*, it allows the model to learn that certain words are present even if they appear with adjoining characters instead of being delimited by spaces
* *Preparation*, it formats the texts to be readable by CRFsuite, the machine learning system that will help automate our named entity extraction.

The final output of this script is a document containing the entire fully prepared corpus in one file: *Data/Prepared/fullCorpus.txt*

### Step 2: Get A Seed

We help the computer get started on its path to learning how to identify these entities by manually annotating, or marking their presence, in a small *seed* sample of sentences from the corpus.

#### Assuming that you have no previously annotated data

We will randomly extract sentences to use in your seed. This is preferred, because a deterministic seed may reflect a systematically distinct distribution of named entities in the corpus.

The ideal seed size depends on a number of factors. We can easily adjust seed size later, but for now, let's set it to 200 sentences as follows:

```
seed_size=200
```

If you have gazatteers with lots helpful entities from your corpus, annotation will go more easily, which might motivate you to do a larger seed, though it also might mean that you don't need such a large seed to get HER going.

If your corpus is very densely packed with entities, you could probably redefine *seed_size* to be less than 200 (and *vice versa*), however, if the types of entities you want to identify are many or finely granular, you might want to increase *seed_size* (and *vice versa*).

The following command will actually extract the seed (whose size we can still edit in Step 3:

```
python Scripts/rankSents.py -corpus Data/Prepared/fullCorpus.txt -sort_method random_seed -topXsents $seed_size -output Data/Splits/fullCorpus.seed-$seed_size -annotate True
```

#### If you *do* have previously annotated data or simply do not want your seed to be random

Open *Data/Prepared/fullCorpus.txt* in a plain text editor (like *Atom* or *Sublime*, not *Word*!) and move all previously annotated sentences and any yet-unannotated sentences you want in your seed to the beginning of the file, as the seed will be extracted from the beginning. Keep in mind that this file is just all the files in *Data/Prepared/* combined, so if all the sentences you wanted to include in the seed were in *Data/Prepared/preAnnotated1.txt* and *Data/Prepared/preAnnotated1.txt* with no other sentences present, it would be easier to do this from the command line as follows:

```
rm Data/Prepared/fullCorpus.txt
mv Data/Prepared/preAnnotated1.txt del.1
mv Data/Prepared/preAnnotated2.txt del.2
cat del.1 del.2 Data/Prepared/* > Data/Prepared/fullCorpus.txt
rm del.1 del.2
```

Set the variable *seed_size* to the line number immediately following the last sentence you want to include in the seed. At minimum, it should probably include all of your previously annotated texts.

If the last word from the last sentence in *Data/Prepared/fullCorpus.txt* that you wanted to include in the seed was on line 999, then I would set *seed_size* as follows:

```
seed_size=1000
```

Then, to extract the seed, run the following command:

```
python Scripts/rankSents.py -corpus Data/Prepared/fullCorpus.txt -sort_method set_seed -topXlines $seed_size -output Data/Splits/fullCorpus.seed-$seed_size -annotate True
```

### Step 3 Manual Annotation Of The Seed

The seed sentences are located at: *Data/Splits/fullCorpus.seed-$seed_size.seed*. The file contains one word (well really token, because punctuation and clitics will likely take their own lines) per line with a single blank line between sentences. The line is tab separated with the *label* (also refered to as a *tag*) in the first column, the word itself in the second, and any other features we might later generate will occupy subsequent columns. By default, the *label* will be *0* for every word, meaning that it is not an entity or at least has not been annotated (manually not automatically) as one yet.

In this step, we will identify all words that are entities and change their labels, systematically. Specifically, the label will be composed by joining the relevant entity type (necessarily one of the types defined in *entities*) and the letter *B* or *I* with a dash. For example, if I come across the word *Paris* in my corpus, I would want to label it as *GEO-B*, where I use *B* to indicate that it is the beginning of an entity. If I come across the words *de*, *New*, *York*, and *.* in a sequence, I would want to label them *0*, *GEO-B*, *GEO-I*, and *0* respectively, where *I* denotes that the present entity has not already terminated. 

To expedite the manual annotation, let's first pretag this file using any pre-existing gazatteers.

```
python Scripts/pre-tag_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed $entities Data/Gazatteers/* > Data/Splits/fullCorpus.seed-$seed_size.seed.preTagged
mv Data/Splits/fullCorpus.seed-$seed_size.seed.preTagged Data/Splits/fullCorpus.seed-$seed_size.seed
```

Now go ahead and start annotating the seed using a *plain text editor*. Keep in mind that this may involve correcting some non-*0* labels whenever the pretagging step made a mistake. If the pretagging step makes a lot of consistent mistakes due to bad entries in the gazatteer, consider removing those bad entries from the relevant gazatteer files and restarting this Step. If the pretagging isn't speeding things up at all because the gazatteers are too bad to be worth addressing like this, remember that the two lines of code above are not necessary - you can always skip them - they are only meant make your annotation easier. *Always back up your hard work somewhere!*

Ideally, you might want at least 60 - 100 named entities in your seed set. You might want more if you have a lot of fine grained entity types or your minority types don't show up at all in the seed, but you also might want less if you have good gazatteers for any infrequent entity types.

If you find less entities than seems necessary in your seed, just cut sentences from Data/Splits/fullCorpus.seed-$seed_size.unannotated and paste them into Data/Splits/fullCorpus.seed-$seed_size.seed until you achieve a suitable number of named entities. If the converse occurs and you find that you have far more than the requisite number of entities before finishing annotating the seed, simply cut the remaining sentences from Data/Splits/fullCorpus.seed-$seed_size.seed into Data/Splits/fullCorpus.seed-$seed_size.unannotated. A larger seed is always better, so certainly don't disclude previously annotated data unless you think some domain or style difference might cause it to be extremely unrepresentative of the distribution of entities elsewhere in the corpus. But you also may not want to annotate the whole seed because your annotation time will be more efficiently spent on an upcoming annotation step, provided the seed was big enough to get HER going. *You do not need to update $seed_size to reflect the number of sentences that you actually ended up annotating.*

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

Let's check how the model is doing with just a small seed set to train on. The command below will take a model trained using the best features identified via cross validation and use it to predict labels for the yet un(manually)annotated corpus. It will combine the manually and automatically annotated halves into a single file for your viewing pleasure *Results/fullCorpus.final.txt* and produce a list of all unique entities found in said file *Results/fullCorpus.final-list.txt* Lastly, all gazatteers, in their present state, will be saved in *Results/Gazatteers/*.

```
sh Scripts/tag_get_final_results.sh 0 Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt
mkdir Results/Gazatteers
cp Data/Gazatteers/* Results/Gazatteers/.
```

Before we move on and improve on these results, let's save them somewhere specific so we can compare to them later.

```
mkdir Results_seed
mv Results/* Results_seed
```

### Step 5: Predict And Rank Unannotated Sentences By Informativity

Depending on the chosen *sortMethod* algorithm, we will use the trained seed model's entity predictions to help us identify the most useful sentences to annotate going forward and/or predict how much annotation is needed to achieve a certain accuracy (there is a known bug in the accuracy predictions at present, though).

```
sh Scripts/tag_and_rank.sh Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.seed.fts $sortMethod Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod None $entities
```

The *preTag_delex* sorting method is so successful here because it leverages gazatteers to identify non-lexical features of words most predictive of entity status in words that have yet to be encounered in annotation. It also biases the model toward making precision errors instead of recall errors, as this helps the model better generalize to unknown words. Furthermore, recall errors in a list are far quicker to manually post edit than precision errors.

### Step 6: Manually Annotate Ranked Sentences And Periodically Update Model

Again, pretag before annotating to expedite the process. If you didn't have a gazatteer to start, you should after annotating the seed.

```
python Scripts/pre-tag_gazatteers.py Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod $entities Data/Gazatteers/* > Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged
mv Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod.preTagged Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod
```

Annotate as much of the file *Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod* as suits your needs.

Upon completing your annotation, sanity check your data again to make sure you made no typos.

```
cut -f1 Data/Splits/fullCorpus.seed-$seed_size.seed | sort -u
```

If it appears that you made any typos, search for them in the seed file and correct them before updating your gazatteers.

```
python Scripts/update_gazatteers.py Data/Splits/fullCorpus.seed-$seed_size.seed Data/Gazatteers/*
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

```
sh Scripts/tag_get_final_results.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt
mkdir Results/Gazatteers
cp Data/Gazatteers/* Results/Gazatteers/.
```

Check out *Results/fullCorpus.final.txt*, *Results/fullCorpus.final-list.txt*, and the files in *Results/Gazatteers/* and save your most recent output so you can reference it again later if you want to make more comparisons.

```
mkdir Results_seed_plus_[sum-of-all-lines-annotated_after_the_seed]
mv Results/* Results_seed_plus_[sum-of-all-lines-annotated_after_the_seed]
```

Consider how much improvement you've gotten since last time relative to the amount of time you've spent annotating. If it seems you've finally reached the point where the marginal benefit of time spent manually annotating more sentences is less than the marginal benefit of time spent manually post editing the outputs that you're interested in (either the lists or the annotated corpus or both), it's probably time to quit.

Otherwise, repeat Step 6 as needed.

### Step 8: Take Off Your Digital Hat And Put On Your Humanist Hat

Regardless of how much post editing lies in your future, I hope HER has served you well and the output of this process has facilitated your project goals. Godspeed!

## Acknowledgments

HER is under continuous development supported by the [Herodotos Project](https://u.osu.edu/herodotos/) and [NYU-PSL Spatial Humanities Partnership](https://wp.nyu.edu/nyupslgeo/). We gratefully acknowledge [Moses](http://www.statmt.org/moses/), from whom we borrowed some code, and [Abraham](https://en.wikipedia.org/wiki/Abraham), from whom we derived three major religions. 

If you find HER useful, please cite the below work from which she was adapted:

* Erdmann et al., 2016 [Challenges and Solutions for Latin Named Entity Recognition](http://www.aclweb.org/anthology/W16-4012)

*Please contact Alex Erdmann (ae1541@nyu.edu) with any questions, bug fixes, or dating advice.*
