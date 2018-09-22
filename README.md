# HER: Humanities Entity Recognizer

HER is an easy-to-use tool designed to help Digital Humanists by expediting the process of identifying entities in textual corpora. She is robust and adaptable to different languages, styles, and domains, and seemlessly handles structured and unstructured texts.

## Getting Started

### Background

HER assumes that the user is not mortified by the thought of using a terminal or working from the command line. If you don't know what that means or you've never used the terminal, have no fear! This README will walk you through most everything you need to know and you can consult the Programming Historian's [Introduction to the Command Line](https://programminghistorian.org/en/lessons/intro-to-bash) to fill in any gaps.

HER was developed and tested on Mac. It should run on any Linux system though Windows will be problematic. Verifying and addressing this is on the to-do list.

### Prerequisites

* **[CRFsuite]**

We will use the CRFsuite package behind-the-scenes to handle some of the machine learning. It can be installed on a Mac via *Homebrew*. If you don't already have Homebrew installed, run the following command:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

With Homebrew already installed, CRFsuite can be installed on a Mac as follows:

```
brew tap brewsci/science
brew install crfsuite
```

For other installation options, check the CRFsuite host [site](http://www.chokkan.org/software/crfsuite/).

CRFsuite has been successfully installed if you can run the below command without generating an error message

```
crfsuite -h
```

* **[Python 3]**

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
* Verify that you are using the necessary version of Python now
```
python -V
```
**FYI**
* *Everytime you open a terminal, you will need to re-activate this environment to gauruntee that you're using the desired version of Python.*
* *If you ever get a *ModuleNotFoundError*, you can usually fix it with Miniconda like so:*
```
conda install -n [your-environment-name] [whatever-package-you're-missing]
```

## Usage

Meat and tators

```
with code heik
```

## Acknowledgments

HER is under continuous development supported by the [Herodotos Project](https://u.osu.edu/herodotos/) and [NYU-PSL Spatial Humanities Partnership](https://wp.nyu.edu/nyupslgeo/). We gratefully acknowledge [Moses](http://www.statmt.org/moses/), from whom we borrowed some code, and [Abraham](https://en.wikipedia.org/wiki/Abraham), from whom we derived three major religions. 

If you find HER useful, please cite the below work from which she was adapted:

* Erdmann et al., 2016 [Challenges and Solutions for Latin Named Entity Recognition](http://www.aclweb.org/anthology/W16-4012)

*Please contact Alex Erdmann (ae1541@nyu.edu) with any questions, bug fixes, or dating advice.*
