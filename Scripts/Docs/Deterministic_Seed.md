## Using a Deterministic Seed

Open *Data/Prepared/fullCorpus.txt* in a plain text editor (like *Atom* or *Sublime*, not *Word*!) and move all previously annotated sentences and any yet unannotated sentences you want in your seed to the beginning of the file, as the seed will be extracted from the beginning. Keep in mind that this file is just all the files in *Data/Prepared/* combined, so if all the sentences you wanted to include in the seed were in *Data/Prepared/preAnnotated1.txt* and *Data/Prepared/preAnnotated1.txt* with no other sentences present, it would be easier to do this from the command line as follows:

```
rm Data/Prepared/fullCorpus.txt
mv Data/Prepared/preAnnotated1.txt del.1
mv Data/Prepared/preAnnotated2.txt del.2
cat del.1 del.2 Data/Prepared/* > Data/Prepared/fullCorpus.txt
rm del.1 del.2
```

Now, set the variable *seed_size* to the line number immediately following the last sentence you want to include in the seed. At minimum, it should probably include all of your previously annotated texts.

If the last word from the last sentence in *Data/Prepared/fullCorpus.txt* that you wanted to include in the seed was on line 999, then I would set *seed_size* as follows:

```
seed_size=1000
```

Then, to extract the seed, run the following command:

```
python Scripts/rankSents.py -corpus Data/Prepared/fullCorpus.txt -sort_method set_seed -topXlines $seed_size -output Data/Splits/fullCorpus.seed-$seed_size -annotate True
```