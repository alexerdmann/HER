"""
This code was written for a workshop and demonstration on Named Entity Recognition in the Digital Humanities at the 2018 NYU-PSL Spatial Humanities Workshop in Paris, France.
It is adapted from Erdmann et al. (2016) (http://www.aclweb.org/anthology/W16-4012), and is freely available.
Please cite the above paper if you wish to use or adapt any part of this code.
Feel free to contact the first author (ae1541@nyu.edu) with any questions, comments, or bug fixes.
"""

###----------  PREREQUISITES  ----------###

# crfsuite
	# on a mac, simply run the following command: homebrew install crfsuite

# Python 3
	# If you do not want Python 3 to be the default version of python, use Anaconda to set up an environment where Python 3 is the default and simply activate that source to use this software and deactivate it afterward (https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/).


###----------  USAGE  ----------###

""" SETTING UP YOUR WORK SPACE """
# Download the Agnostic_NER directory as is. It does not require any installing or building.
# For each new named entity recognition project, set up your work space as follows:
name_of_project=myExperiment
sh Scripts/set_up_work_space.sh $name_of_project
cd $name_of_project
# NOW UPLOAD ALL OF YOUR RAW TEXTS THAT YOU WANT TO EXTRACT NAMED ENTITIES FROM to the Data/Original/ folder within your new project directory
# make sure all such raw texts have either a .txt or .xml extension (preprocessing script may not handle all xml files - check to make sure these run okay)
# for the sake of example, I will use the texts included with the download.
cp ../Data/Original/* Data/Original/.


""" DEFINING PARAMETERS """
# We are now ready to start identifying named entities. In order to see efficiently accurately, we need to start by annotating named entities manually in a small sample of sentences from your corpus.
# We can define the number of sentences in this seed set here. The default suggestion should be a reasonable number, and if it turns out to not be reasonable, we can adjust this later on.
seed_size=200  # Minimum number of sentences to be included in the initial random seed set..
# or, if you would like to set a deterministic seed set, set this to the number of lines (NOT SENTENCES) to be included in this seed..
	# If you want to use a deterministically set seed, you will have to wait until after Step 1 to determine number of lines because the corpus will be reformatted in Step 1..
	# Once Step 1 is completed, you would do the following:
		# rm Data/Prepared/fullCorpus.txt
		# cat Data/Prepared/[all-texts-you-want-to-use-as-seed] Data/Prepared/[rest-of-texts-you-want-to-tag] > Data/Prepared/fullCorpus.txt
			# this is because your desired seed must come first in Data/Prepared/fullCorpus.txt
		# set seed_size equal to the line number of the blank line following the last sentence you intend to use as seed data.

# We also need to determine the algorith that will be used later on to identify other sentences to annotate given trends observed in the random seed.
sortMethod=hardCappedUNKs  # can also try "rapidEntityDiversity" (if capitalization is not likely to mark named entities in your corpus) or "rapidUncertainty" (which is comparable to "rapidEntityDiversity"), though both perform worse than hardCappedUNKs in languages that use capitalization to mark named entities. You can also use "random" here as a baseline.
lg=en  # Review the language codes supported by the Moses Tokenizer. They are the suffixes found on the files in Scripts/Moses_Tokenizer/share/nonbreaking_prefixes. The language is only used for tokenization, so if your language is not listed, English is a safe default as the English tokenization scheme does little besides simply separating punctuation.


""" STEP 1: PREPARING YOUR TEXTS """ 
### IF YOU HAVE PREVIOUSLY ANNOTATED TEXTS, YOU CAN EDIT THE FOLLOWING SCRIPT TO PRESERVE WHATEVER ANNOTATIONS ARE USEFUL TO YOUR ANALYSIS:
	# sh Scripts/prepare_original_texts.sh Scripts/preprocess_Davids_data.py $lg 
# OTHERWISE, RUN THIS COMMAND
sh Scripts/prepare_original_texts.sh Scripts/preprocess.py $lg 
# This takes all your original files in Data/Original/, regardless of extension .xml or .txt, and turns them into raw, unstructured text.
# Next, it performs tokenization, which allows the model to learn that certain words are present even if they appear with adjoining characters instead of being delimited by spaces.
# Then it will handle some small preprocessing issues and format the text so that it is readable by our named entity extracting machine learning software.
# Lastly, this script writes out a document containing the entire fully prepared corpus at Data/Prepared/fullCorpus.txt


""" STEP 2: GET SEED """
# This identifies a random portion of sentences to annotate so we can use them to strategically select other yet unannotated sentences to annotate later on which will hopefully fill in the gaps of the system's knowledge. 
# If you already have some annotated data and you want to adapt a system to yet unannotated data, or for whatever reason you just want to specify a specific chunk of text to use as your seed, try the second (commented out) variant of this command.
python Scripts/rankSents.py -corpus Data/Prepared/fullCorpus.txt -sort_method random_seed -topXsents $seed_size -output Data/Splits/fullCorpus.seed-$seed_size -annotate True
# If you use this second command (below), be sure that the texts you want to use in your seed are at the beginning of Data/Prepared/fullCorpus.txt and that $seed_size is set to the number of lines, not sentences, which you wish to use as a seed (as discussed in the "Defining Parameters" section).
	# python Scripts/rankSents.py -corpus Data/Prepared/fullCorpus.txt -sort_method set_seed -topXlines $seed_size -output Data/Splits/fullCorpus.seed-$seed_size -annotate True


""" STEP 3: MANUAL ANNOTATION OF THE SMALL SEED """
# Go ahead and annotate the seed: Data/Splits/fullCorpus.seed-$seed_size.seed (back up your annotation somewhere!)
# Ideally, you want to make sure you have at least 60 - 100 named entities in your seed set to be able to make reasonable predictions about expected accuracy on remaining unannotated data.
# If you find less than this in your seed, just cut sentences from Data/Splits/fullCorpus.seed-$seed_size.unannotated into Data/Splits/fullCorpus.seed-$seed_size.seed until you achieve a suitable number of named entities.
# Similarly, if the converse occurs and you find that you already have well over about 60 named entities before finishing annotating the seed, simply cut the remaining sentences from Data/Splits/fullCorpus.seed-$seed_size.seed into Data/Splits/fullCorpus.seed-$seed_size.unannotated.
# You do not need to update $seed_size to reflect the number of sentences that you actually used in your seed; the $seed_size variable is just used for naming files from this point onward.


""" STEP 4: FEATURE ENGINEERING AND TRAINING SEED MODEL """
# Make sure that -testable is set to your annotation file, which should be Data/Splits/fullCorpus.seed-$seed_size.seed.
# Then run the command below which will perform cross-validation over different folds of the seed data to pick the best feature set (this may take several hours; consider removing some features from POSSIBLE_FEATS (line 164) in Scripts/cross_validation.py if time is a concern).
# It will use this feature set to train a model on all the seed data.
python Scripts/cross_validation.py -testable Data/Splits/fullCorpus.seed-$seed_size.seed -fullCorpus Data/Prepared/fullCorpus.txt -identify_best_feats True -train_best True -unannotated Data/Splits/fullCorpus.seed-$seed_size.unannotated
# Depending on the chosen $sortMethod, this script may predict accuracy on yet unannotated texts. This functionality is still being developed however, and the numbers reported cannot yet be trusted.


""" STEP 5: PREDICT AND RANK UNANNOTATED SENTENCES BY INFORMATIVITY """
# Use the trained seed model to predict the named entity labels in the remaining unannotated data. 
# Depending on the chosen $sortMethod algorithm, these predictions may serve one or both of the following purposes:
	# to determine which sentences to annotate going forward based on the certainty with which the seed model predicts named entities in each sentence, thus making future time spent annotating more productive.
	# to predict how many of the yet unannotated sentences must be annotated in order to achieve a certain accuracy or error reduction (though this functionality is still in development, and the numbers reported cannot yet be trusted).
sh Scripts/tag_and_rank.sh Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Data/Splits/fullCorpus.seed-$seed_size.unannotated.fts Data/Splits/fullCorpus.seed-$seed_size.seed.fts $sortMethod Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod 


""" STEP 6: MANUAL ANNOTATION OF THE RANKED SENTENCES """
# Go ahead and annotate as much of the file Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod as suits your needs.


""" STEP 7: PERIODICALLY UPDATE MODEL (NOT NECESSARY BUT CAN HELP) """
# Anytime you want to take a break from annotating in Step 6, you might find it helpful to re-check your expected accuracy for tagging the rest of the corpus, re-check if the feature set you've been using is still optimal, and re-rank the remaining unannotated sentences.
	# of course if you're using an algorithm like hardCappedUNKs whose ranking does not depend on prediction certainties or feature--label correlations, you may never have the need to perform Step 7, especially as long as the accuracy prediction functionality is not finished.
# Even for metrics other than hardCappedUNKs,the ranking is still designed such that it is not necessary to run this step and recalculate a new ranking provided the seed was large enough, but recalculating after some additional annotation might marginally improve the ranking and reassure the user.

# RECORD THE LINE NUMBER THAT IS THE BLANK LINE AFTER THE LAST SENTENCE YOU ANNOTATED
	# (if you open the file in Sublime or Atom this should be listed on the left-hand panel)
lines_annotated=[some_number]

sh Scripts/update_crossValidate_rerank.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt $sortMethod Data/Splits/fullCorpus.seed-$seed_size.unannotated.probs Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod


""" STEP 8: WHEN YOU ARE DONE, TRAIN THE FINAL MODEL, PREDICT IN THE UNANNOTATED CORPUS, CALCULATE EXPECTED ACCURACY, AND GENERATE A FULL ANNOTATED CORPUS AND A COMPREHENSIVE LIST OF ALL NAMED ENTITIES """
### Same as Step 7 except, at the end, we will produce the entire corpus--a combination of the random seed and the predicted annotations--as well as a list of all identified named entities.

# RECORD THE LINE NUMBER THAT IS THE BLANK LINE AFTER THE LAST SENTENCE YOU ANNOTATED
	# (if you open the file in Sublime or Atom this should be listed on the left-hand panel)
lines_annotated=[some_number]

sh Scripts/update_crossValidate_tag_get_final_results.sh $lines_annotated Models/RankedSents/fullCorpus.seed-$seed_size.$sortMethod Data/Splits/fullCorpus.seed-$seed_size.alwaysTrain Data/Splits/fullCorpus.seed-$seed_size.unannotated Data/Splits/fullCorpus.seed-$seed_size.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-$seed_size.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt