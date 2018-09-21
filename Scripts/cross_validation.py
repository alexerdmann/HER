import pickle
import sys
import os 
import fileinput
import random
import argparse
import itertools
import time
import math
from customEval import custom_eval_exclusive

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

	return rankedSents

def randomSort(corpus):
	rankedSents = unrankedSort(corpus)
	random.shuffle(rankedSents)
	return rankedSents

def write_out_splits(testable, alwaysTrain):
	### READ IN THE TESTABLE DATA AND TRAINING DATA
	splits_to_data = {}
	output_base = testable
	testable = unrankedSort(testable)
	sz = math.ceil(len(testable)/3)
	split_size = max(50,sz)  ## 3-fold cross validation
	if alwaysTrain == None:
		alwaysTrain = []
	else:
		alwaysTrain = unrankedSort(alwaysTrain)
	### WRITE OUT ALL OF THE TRAIN TEST SPLITS
	i = 0
	index = 0
	split = 0
	so_far = []
	for sent in testable:
		index += 1
		i += 1
		if i > split_size:
			train_file = open(output_base+'.train-'+str(split),'w')
			test_file = open(output_base+'.test-'+str(split),'w')
			train = alwaysTrain
			try:
				train.extend(testable[0:index-split_size])
			except IndexError:
				pass
			try:
				train.extend(testable[index:])
			except IndexError:
				pass
			for s in train:
				for l in s:
					train_file.write('{}\n'.format(l))
				train_file.write('\n')
			train_file.close()
			for s in so_far:
				for l in s:
					test_file.write('{}\n'.format(l))
				test_file.write('\n')
			test_file.close()
			### RESET I AND THE TEST SET ITERATE THE SPLIT COUNTER
			split += 1
			i = 1
			so_far = []
		so_far.append(sent)

	if len(so_far) > 0:
		train_file = open(output_base+'.train-'+str(split),'w')
		test_file = open(output_base+'.test-'+str(split),'w')
		train = alwaysTrain
		try:
			train.extend(testable[0:index-len(so_far)])
		except IndexError:
			pass
		for s in train:
			for l in s:
				train_file.write('{}\n'.format(l))
			train_file.write('\n')
		train_file.close()
		for s in so_far:
			for l in s:
				test_file.write('{}\n'.format(l))
			test_file.write('\n')
		test_file.close()

	return split + 1

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
		F, prec, rec, recDenom = custom_eval_exclusive(test, predictions)
		score += F*recDenom
		denom += recDenom

		os.system('rm '+featureOutput+'.train')
		os.system('rm '+featureOutput+'.test')
		os.system('rm '+modelLocation)
		os.system('rm '+predictions)

	score /= denom
	print('{}: {}%    (total entities = {})'.format(featureSet,str(round(100*score,2)),str(denom)))
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

args = parser.parse_args()

POSSIBLE_FEATS = ['wordShape','charNgrams','prevWord','prevBiWord','prevWordShape','contextPosition','gazatteers']  ## DEBUG Short List
# POSSIBLE_FEATS = ['wordShape','charNgrams','prevWordShape','nextWordShape','prevWord','nextWord','prevBiWord','nextBiWord','prevBiWordShape','nextBiWordShape','histStats','contextPosition','gazatteers']
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

		print('\n_________________________________\n')
		print('BEST FEATURE SET:    {}'.format('_'.join(bestSet)))
		print('TRAINED MODEL:    {}'.format(modelLocation))
		print('TRAINING DATA WITH FEATURES:    {}'.format(testable+'.fts'))
		print('UNANNOTATED DATA WITH FEATURES:    {}'.format(unannotated+'.fts'))
		print('PREDICTED ACCURACY ON UNANNOTATED DATA: {}%\n\n'.format(str(round(100*bestScore,2))))












