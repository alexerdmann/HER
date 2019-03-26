import pickle
import sys
import os 
import fileinput
import random
import argparse
import itertools
import time
import math
from customEval import custom_eval_biased_recall_exclusive

def unrankedSort(corpus):
	rankedSents = []
	sent = []
	for line in fileinput.input(corpus):
		line = line.replace('\n','')
		if len(line.split()) == 0:
			if len(sent) > 0:
				rankedSents.append(sent)
				sent = []
		else:
			sent.append(line)
	fileinput.close()

	if len(sent) > 0:
		rankedSents.append(sent)

	return rankedSents

def randomSort(corpus):
	rankedSents = unrankedSort(corpus)
	random.shuffle(rankedSents)
	return rankedSents

def write_out_splits(testable, alwaysTrain):
	### READ IN THE TESTABLE DATA AND TRAINING DATA
	output_base = testable
	testable = unrankedSort(testable)
	sz = math.ceil(len(testable)/3)
	splits = math.ceil(len(testable)/sz)
	split_size = max(50,sz)  ## 3-fold cross validation
	if alwaysTrain == None:
		alwaysTrain = []
	else:
		alwaysTrain = unrankedSort(alwaysTrain)
	### WRITE OUT ALL OF THE TRAIN TEST SPLITS

	for s in range(splits):

		train_file = open(output_base+'.train-'+str(s),'w')
		test_file = open(output_base+'.test-'+str(s),'w')

		test_start = s*sz
		test_end = min(len(testable),(s+1)*sz)
		test_split = testable[test_start:test_end]

		for sent in test_split:
			for l in sent:
				test_file.write('{}\n'.format(l))
			test_file.write('\n')
		test_file.close()

		train_split = []
		for i in range(len(testable)):
			if i < test_start or i >= test_end:
				train_split.append(testable[i])

				for l in testable[i]:
					train_file.write('{}\n'.format(l))
				train_file.write('\n')
		train_file.close()

	return splits

def n_way_cross_validation(feature_set, alwaysTrain, number_of_folds, output_base, fullCorpus):
	score = 0
	denom = 0
	if alwaysTrain == None:
		alwaysTrain = 'None'
	for split in range(number_of_folds):

		train = output_base+'.train-'+str(split)
		test = output_base+'.test-'+str(split)
		featureSet = '_'.join(feature_set)
		featureOutput = 'Data/Features/seed_cross_validation'
		modelLocation = 'Models/CRF/seed_cross_validation.cls'
		predictions = 'Results/seed_cross_validation.pred'

		os.system('sh Scripts/getFeatures_train_test.sh '+train+' '+test+' '+fullCorpus+' '+featureSet+' '+featureOutput+' '+modelLocation+' '+predictions+' '+alwaysTrain)

		### DEBUGGING
		# os.system('echo '+train)
		# os.system('echo '+test)
		# os.system('echo '+alwaysTrain)
		# os.system('echo '+featureOutput)
		# input()

		### evaluate (custom)
		F, total = custom_eval_biased_recall_exclusive(test, predictions)
		score += F*total
		denom += total

		os.system('rm '+featureOutput+'.train')
		os.system('rm '+featureOutput+'.test')
		os.system('rm '+modelLocation)
		os.system('rm '+predictions)

	score /= denom
	print('{}\n\t{}% accuracy on {} seed entities'.format(featureSet,str(round(100*score,2)),str(denom)))
	return score

def get_best_feature_set(number_of_folds, alwaysTrain, testable, POSSIBLE_FEATS, fullCorpus):
	# bestScore = n_way_cross_validation(['None'], alwaysTrain, number_of_folds, testable, fullCorpus)
	# bestSet = ('None')
	bestScore = 0

	for k in range(1, len(POSSIBLE_FEATS)+1):
		for feature_set in itertools.combinations(POSSIBLE_FEATS, k):

			### limiting the space of possible feature-sets to search through
			if 'wordShape' in feature_set and 'prevWord' in feature_set and 'gazatteers' in feature_set:

				score = n_way_cross_validation(feature_set, alwaysTrain, number_of_folds, testable, fullCorpus)
				if score >= bestScore:
					bestScore = score
					bestSet = feature_set

	return bestSet, bestScore

###################################################################

parser = argparse.ArgumentParser()
parser.add_argument('-alwaysTrain', type=str, help='Is there any data we can use to train but cant test on?', required=False, default=None)
parser.add_argument('-testable', type=str, help='What data can we test the system on?', required=True)
parser.add_argument('-fullCorpus', type=str, help='What data can we gather statistics from, annotated or otherwise?', required=True)
parser.add_argument('-identify_best_feats', type=bool, help='Should we identify the best set of features to train on?', required=False, default=False)
parser.add_argument('-train_best', type=bool, help='Should we train the best model on testable + alwaysTrain as soon as we identify the best set of features?', required=False, default=False)
parser.add_argument('-unannotated', type=str, help='Where is the unannotated corpus located?', required=False, default=None)
parser.add_argument('-prepare_multiple_tests', type=str, help='Should we do feature engineering on other test sets as well? Pass all test sets in a single string delimited by two underscores, i.e., file1.txt__file2.txt.', required=False, default=None)

args = parser.parse_args()

POSSIBLE_FEATS = ['wordShape','charNgrams','prevWord','prevBiWord','prevWordShape','contextPosition','gazatteers']  ## Short List
# POSSIBLE_FEATS = ['wordShape','charNgrams','prevWordShape','nextWordShape','prevWord','nextWord','prevBiWord','nextBiWord','prevBiWordShape','nextBiWordShape','histStats','contextPosition','gazatteers','wordLength'] ## Full List
alwaysTrain = args.alwaysTrain
testable = args.testable
fullCorpus = args.fullCorpus

### write out and get the total number of splits
number_of_folds = write_out_splits(testable, alwaysTrain)

### CROSS VALIDATE TO PICK THE BEST POSSIBLE FEATURE SET
if '-identify_best_feats' in sys.argv:
	bestSet, bestScore = get_best_feature_set(number_of_folds, alwaysTrain, testable, POSSIBLE_FEATS, fullCorpus)
	os.system('rm '+testable+'.train-*')
	os.system('rm '+testable+'.test-*')

	if '-train_best' in sys.argv:
		modelLocation = 'Models/CRF/best_seed.cls'
		unannotated = args.unannotated
		if alwaysTrain == None:
			alwaysTrain = 'None'
		os.system('sh Scripts/getFeatures_train.sh '+testable+' '+unannotated+' '+fullCorpus+' '+'_'.join(bestSet)+' '+testable+'.fts'+' '+unannotated+'.fts'+' '+modelLocation+' '+alwaysTrain)
		# write out best feature set
		fs = open('Models/CRF/best_seed.featSet', 'w')
		fs.write('_'.join(bestSet))
		fs.close()

		print('\n_________________________________')
		print('BEST FEATURE SET:\n\t{} ({}%)'.format('_'.join(bestSet),str(round(100*bestScore,2))))
		print('TRAINED MODEL:\n\t{}'.format(modelLocation))
		print('TRAINING DATA WITH FEATURES:\n\t{}'.format(testable+'.fts'))
		print('UNANNOTATED DATA WITH FEATURES:\n\t{}'.format(unannotated+'.fts'))
		# print('PREDICTED ACCURACY ON UNANNOTATED DATA: {}%\n\n'.format(str(round(100*bestScore,2))))
		print('_________________________________\n')

	if args.prepare_multiple_tests != None and args.prepare_multiple_tests != 'None':
		multiple_tests = args.prepare_multiple_tests.split('__')

		for unannotated in multiple_tests:
			featureSet = ' '.join(bestSet)
			os.system('python Scripts/addFeatures.py -corpus '+unannotated+' -fullCorpus '+fullCorpus+' -features '+featureSet+' -hist '+fullCorpus+'.hist -gazatteers Data/Gazatteers/* > '+unannotated+'.fts')






