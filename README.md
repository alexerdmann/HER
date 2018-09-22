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

**Human Capital**

* If you're not familiar with best practices for annotating named entities or are not sure what that really means, it would be good to outline some consistent guidelines for how you will handle issues like ambiguity or embedded named entities ([This will link to a relevant site one day](https://www.amazon.com/USA-Tees-Merica-Dinosaur-Cowboy/dp/B073XXLVNT/ref=pd_lpo_sbs_193_img_0?_encoding=UTF8&refRID=P4PT1M97YJY9CS5H93J3)).

* HER assumes that the user is not mortified by the thought of using a terminal or working from the command line. If you don't know what that means or you've never used the terminal, have no fear! This README will walk you through most everything you need to know and you can consult the Programming Historian's [Introduction to the Command Line](https://programminghistorian.org/en/lessons/intro-to-bash) to fill in any gaps.

**Operating System**

HER was developed and tested on Mac. It should run on any Linux system, though Windows will be problematic. Verifying and addressing this is on the to-do list.

**CRFsuite**

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

**Python 3**

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

To set your *lg* variable, review the language codes supported by the Moses Tokenizer which HER will use to prepare your data. These codes are represented by the suffixes found on the files located in *Scripts/Moses_Tokenizer/share/nonbreaking_prefixes/nonbreaking_prefix.[suffix]*.

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
*Do not use any spaces, dashes, or non-ascii characters when defining* entities*!*

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
cp ../Data/Original/French.zip Data/.
unzip Data/French.zip
mv French/* Data/Original/.
rm -rf French
rm Data/French.zip
cp ../Data/Gazatteers/GEO.gaz Data/Gazatteers/GEO.gaz
```

## Usage

### Step 1


by better leveraging gazatteers induced from your annotation to identify the non-lexical features of words most predictive of entity status.

## Acknowledgments

HER is under continuous development supported by the [Herodotos Project](https://u.osu.edu/herodotos/) and [NYU-PSL Spatial Humanities Partnership](https://wp.nyu.edu/nyupslgeo/). We gratefully acknowledge [Moses](http://www.statmt.org/moses/), from whom we borrowed some code, and [Abraham](https://en.wikipedia.org/wiki/Abraham), from whom we derived three major religions. 

If you find HER useful, please cite the below work from which she was adapted:

* Erdmann et al., 2016 [Challenges and Solutions for Latin Named Entity Recognition](http://www.aclweb.org/anthology/W16-4012)

*Please contact Alex Erdmann (ae1541@nyu.edu) with any questions, bug fixes, or dating advice.*
