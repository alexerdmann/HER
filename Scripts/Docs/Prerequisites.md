## Prerequisites

### Human Capital

* If you're not familiar with best practices for annotating named entities or are not sure what that really means, it would be good to outline some consistent guidelines for how you will handle issues like ambiguity or embedded named entities ([This will link to a relevant site one day](https://www.youtube.com/watch?v=EpP6Rgbyh1U)).

* HER assumes that the user is not mortified by the thought of using a terminal or working from the command line. If you don't know what that means or you've never used the terminal, have no fear! This manual will walk you through most everything you need to know and you can consult the Programming Historian's [Introduction to the Command Line](https://programminghistorian.org/en/lessons/intro-to-bash) to fill in any gaps.

### Operating System

If you are using a Mac, you don't need to do anything. If you're on a Windows machine, you will need to install [PuTTY](https://www.putty.org) or [Cygwin](https://www.cygwin.com) to simulate Linux.
If you are using Linux, either natively or through Cygwin or Putty, you will need to switch to the Linux-friendly Scripts directory included in the repository. You can do that quite simply with the following commands:


```
rm -rf Scripts
unzip Scripts_Linux.zip
```

You may also, if you are using Linux, need to sym link the *sh* command to *bash*. Basically, this has to deal with the programming language your terminal is expecting. On Ubuntu machines typically, if you start a command in the terminal with *sh*, it interprets what follows in the *dash* language, whereas we want *sh* to be interpreted in the slightly different *bash* language.

You can check how *sh* is interpreted on your machine by running the following command:

```
ls -l /bin/sh
```

If it returns something including */bin/sh -> /bin/dash*, that means that *sh* is symbolically linked to *dash* and you need to change the symbolic link to *bash*. Provided you have *sudo* authority, you can do this on your machine with the following command, just supply the password when prompted (otherwise, you'll need to bug your system administrator for help).

```
sudo ln -s /bin/bash /bin/sh
```

### CRFsuite

We will use the [CRFsuite](http://www.chokkan.org/software/crfsuite/) package behind-the-scenes to handle some of the machine learning. If you are using the Linux Scripts directory, there is a pre-compiled executable version of CRFsuite included in the directory, so you don't need to worry about this. 

Otherwise, CRFsuite can be installed on a Mac via *Homebrew*. If you don't already have Homebrew installed, run the following command:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

With Homebrew installed, CRFsuite can be installed as follows:

```
brew tap brewsci/science
brew install crfsuite
```

CRFsuite has been successfully installed if you can run one of the two below commands without generating an error message.

On Mac:

```
crfsuite -h
```

On Linux:

```
./Scripts/crfsuite.prog -h
```

### Python 3

If the below command tells you that you are using a version of Python less than 3.0, you need to get [Python 3](https://www.python.org/download/releases/3.0/) and/or make it the defualt version of Python.

```
python -V
```

The easiest way to get Python 3 is to create an *environment* using the *Miniconda* tool:
* Download Miniconda from this [url](https://conda.io/miniconda.html)
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

*Everytime you open a terminal, you will need to re-activate your environment to gauruntee that you're using the desired version of Python. Without version 3 or higher, HER will be unable to handle many non-standard characters, making it impossible to work on languages like Chinese or Arabic.*

*If you ever get a* ModuleNotFoundError *while using HER, you can usually fix it with Miniconda like so:*
```
conda install -n [your-environment-name] [whatever-module-you're-missing]
```
