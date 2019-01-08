## Defining Parameters

Before we can start identifying named entities, we need to define some aspects of how this entity extraction is gonna go down.

### Language

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

I can tell HER that my data is French with the following command:

```
lg=fr
```

### Entity Types

In order to teach a machine to help us extract entities, we need to first define what types of entities we want distinguish and at what granularity. Once you do that, assign them to a variable called *entities*, separated by underscores. For example, let's say I'm interested in extracting only geographical places which I want marked in my corpus as *GEO*. Then I'll define *entities* as follows:
```
entities=GEO
```
If you want to identify birth places, death places, and persons' names as GEOB, GEOD, and PRS respectively, then you would define *entities* as followings:
```
entities=GEOB_GEOD_PRS
```
*Do not use any spaces, dashes, or non-ascii characters when defining* entities!

There is nothing special about the labels you choose for your entities. It is however crucial that you use them consistently later on when you are annotating entities in context.

### Annotation Optimization Algorithm

Now we also need to determine the algorithm that HER will use to determine which sentences are more informative so that any time spent manually annotating named entities is optimally beneficial. The best, most robust algorithm is *preTag_delex*, which I will tell HER I want to use by assigning it to the variable *sortMethod*:

```
sortMethod=preTag_delex
```

Other, worse performing algorithms include:
* *hardCappedUNKs*, which relies on capitalization being highly predictive of the distribution of the entities you're concerned with in your corpus
* *rapidEntityDiversity* and *rapidUncertainty*, which are robust to different languages, styles, etc. like *preTag_delex* and unlike *hardCappedUNKs*, though *preTag_delex* far outperforms them
* *random* served as a useful sorting method to compare to as a baseline when i was developing the other algorithms
