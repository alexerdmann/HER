## Prerequisites

### Human Capital

* If you're not familiar with best practices for annotating named entities or are not sure what that really means, it would be good to outline some consistent guidelines for how you will handle issues like ambiguity or embedded named entities ([This will link to a relevant site one day](https://www.youtube.com/watch?v=T0RvPYRRRbE)).

* HER assumes that the user is not mortified by the thought of using a terminal or working from the command line. If you don't know what that means or you've never used the terminal, have no fear! This README will walk you through most everything you need to know and you can consult the Programming Historian's [Introduction to the Command Line](https://programminghistorian.org/en/lessons/intro-to-bash) to fill in any gaps.

### Operating System

HER was developed and tested on Mac. It should run on any Linux system, though Windows will be problematic. Verifying and addressing this is on the to-do list.

### CRFsuite

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

If you are having trouble with installation, you can take care of this during the [Set Up](https://github.com/alexerdmann/HER/blob/master/Scripts/Set_Up.md)
step. After you've downloaded HER and cd'ed into the *HER/* directory, go through all the scripts in the *Scripts/* subdirectory, search for the command *crfsuite*, and replace it with the absolute path to the prepackaged version of CRFsuite included in the download. To get that absolute path, from the main *HER/* directory, type the following:

```
echo $PWD
```

This will give you the absolute path to that directory, so it should end in */HER*. Simply add */Scripts/crsuite.prog* to the end of that path and you have the absolute path to the prepackaged crfsuite. This should address most installation issues on MAC and Ubuntu, though it is certainly not the most elegant solution.

CRFsuite has been successfully installed if you can run the below command without generating an error message (of course, if you had to replace crfsuite with an absolute path, do so in the below command as well to ensure it is working)

```
crfsuite -h
```

### Python 3

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
