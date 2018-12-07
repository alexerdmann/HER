import pickle
import sys
import os 
import fileinput
import random
import argparse
import time
import itertools
import math
import string

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

def hard_capped_UNK_sort_and_write_out(corpus, filename, seedHist):
	avg_sent_length = [0,0]
	sents = unrankedSort(corpus)
	hardCappedUNKs = {}
	word2sentNum = {}
	sentNum2word = {}
	sentNum2length = {}
	for sNum in range(len(sents)):
		s = sents[sNum]
		sent_length = len(s)
		sentNum2length[sNum] = sent_length
		avg_sent_length[0] += sent_length
		avg_sent_length[1] += 1
		for lNum in range(sent_length):
			l = s[lNum]
			word = l.split()[1]
			if word[0].isupper() and word not in seedHist:
				if lNum != 0:
					if word not in word2sentNum:
						word2sentNum[word] = {}
					if sNum not in sentNum2word:
						sentNum2word[sNum] = {}
					if word not in hardCappedUNKs:
						hardCappedUNKs[word] = 0
					word2sentNum[word][sNum] = True
					sentNum2word[sNum][word] = True
					hardCappedUNKs[word] += 1

	avg_sent_length = avg_sent_length[0]/avg_sent_length[1]

	rankedHardCaps = sorted([(hardCappedUNKs[k], k) for k in hardCappedUNKs.keys()], reverse=True)

	### GET AS MANY HIGH FREQUENCY HARD CAP WORDS AS FAST AS POSSIBLE
	alreadyIncludedWords = dict(seedHist)
	alreadyIncludedSents = {}
	rankedSents = []
	for t in range(len(rankedHardCaps)):
		word = rankedHardCaps[t][1]
		if word not in alreadyIncludedWords:
			bestAddedFreqs = -1
			for sNum in word2sentNum[word]:
				if sNum not in alreadyIncludedSents:


					denominator = max(sentNum2length[sNum],avg_sent_length)


					addedFreqs = 0
					for w in sentNum2word[sNum]:


						# addedFreqs += hardCappedUNKs[w]
						addedFreqs += hardCappedUNKs[w] / denominator


					if addedFreqs > bestAddedFreqs:
						bestAddedFreqs = addedFreqs
						bestSent = sNum 
			for w in sentNum2word[bestSent]:
				alreadyIncludedWords[w] = True
			alreadyIncludedSents[bestSent] = True
			rankedSents.append(sents[bestSent])

	limit = len(rankedSents)
	# append the rest of the sents
	for sNum in range(len(sents)):
		if sNum not in alreadyIncludedSents:
			rankedSents.append(sents[sNum])

	# write out
	output = open(filename,'w')
	for s in rankedSents:
		for l in s:
			output.write('{}\n'.format(l))
		output.write('\n')
	output.close()

	os.system("sed '/./,$!d' "+filename+" > "+filename+".2")
	os.system("mv "+filename+".2 "+filename)

	return rankedSents, limit

def random_sort_and_write_out(corpus, output):
	sents = randomSort(corpus)

	# write out
	output = open(output,'w')
	for s in sents:
		for l in s:
			output.write('{}\n'.format(l))
		output.write('\n')
	output.close()

	return sents

def print_annotation(sents, output):
	output = open(output,'w')
	for s in sents:
		for l in s:
			output.write(l+'\n')
		output.write('\n')
	output.close()

def getHist(fts):
	hist = {}
	for s in fts:
		for l in s:
			w = l.split()[1]
			if w not in hist:
				hist[w] = 0
			hist[w] += 1
	return hist

def get_UNKs_stats(unannotated, predictions, seedHist):
	UNKs_to_Egains = {}
	sents_to_UNKs = {}
	UNKs_to_sents = {}
	sentNum2length = {}
	avg_sent_length = [0,0]
	totalUNKs = 0.0
	leftover = {}
	for s in range(len(unannotated)):
		w = -2
		sents_to_UNKs[s] = {}
		sent_length = len(unannotated[s])
		sentNum2length[s] = sent_length
		avg_sent_length[0] += sent_length
		avg_sent_length[1] += 1
		for l in range(len(predictions[s])):
			w += 1
			if w == -1:
				sentProb = float(predictions[s][l].split('\t')[1])
			else:
				word = unannotated[s][w].split()[1]
				if word not in seedHist:
					sents_to_UNKs[s][word] = True
					if word not in UNKs_to_sents:
						UNKs_to_sents[word] = {}
					UNKs_to_sents[word][s] = True
					Egain = 1.0 - float(predictions[s][l].split(':')[1])
					if word not in UNKs_to_Egains:
						UNKs_to_Egains[word] = 0
					UNKs_to_Egains[word] += Egain
					totalUNKs += Egain
	avg_sent_length = avg_sent_length[0]/avg_sent_length[1]

	for s in sents_to_UNKs:
		if len(sents_to_UNKs[s]) == 0:
			leftover[s] = True
	for s in leftover:
		del sents_to_UNKs[s]
	return UNKs_to_Egains, sents_to_UNKs, UNKs_to_sents, leftover, totalUNKs, sentNum2length, avg_sent_length

def get_feature_significances(seed):
	feature_significances = {}
	avg_feature_NE_likelihood = [0,0]

	for s in seed:
		for l in s:
			line = l.split()
			label = line[0]
			features = line[1:]
			NE = False
			if label != '0':
				NE = True
				
			for f in features:
				avg_feature_NE_likelihood[1] += 1
				if f not in feature_significances:
					feature_significances[f] = [0,0]  # [occured w/ NE, occured]
				feature_significances[f][1] += 1
				if NE:
					avg_feature_NE_likelihood[0] += 1
					feature_significances[f][0] += 1

	avg_feature_NE_likelihood = avg_feature_NE_likelihood[0]/avg_feature_NE_likelihood[1]
	minFeat = None
	for f in feature_significances:

		### OCCURRENCES * PERCENT OCCURENCES WITH NEs
		# feature_significances[f] = (feature_significances[f][0] ** 2 ) / feature_significances[f][1]

		### OCCURRENCES TO THE POWER OF THE DIFFERENCE BETWEEN PERCENT OCCURENCES WITH NEs and AVG PERCENT OCCURENCES WITH NEs OVER ALL FEATURES
		feature_freq = feature_significances[f][1]
		feature_NE_likelihood = feature_significances[f][0]/feature_significances[f][1]

		feature_significances[f] = max(0, feature_freq**(feature_NE_likelihood - avg_feature_NE_likelihood) -1 )

		if minFeat == None and feature_significances[f] > 0:
			minFeat = feature_significances[f]
		elif feature_significances[f] > 0 and feature_significances[f] < minFeat:
			minFeat = feature_significances[f]

	### lambda smoothing with lambda = smallest positive significance value for any feat
	for f in feature_significances:
		feature_significances[f] += minFeat

	return feature_significances, minFeat

def get_UNKhist(seedHist, unannotated):
	UNKhist = {}
	for s in unannotated:
		for l in s:
			word = l.split()[1]
			if word not in seedHist:
				if word not in UNKhist:
					UNKhist[word] = 0
				UNKhist[word] += 1
	return UNKhist

def get_sent_significances(unannotated, feature_significances, UNKhist, minFeat):
	UNKs_to_cells = {}
	sents_to_significance_matrix = []
	UNKless = []
	matrix_to_map = {}
	max_significance = 0
	avg_sent_length = [0,0]

	rowID = -1
	for s in unannotated:

		hasUNK = False

		rowID += 1
		row = []
		for l in s:
			significance = 0
			line = l.split()
			word = line[1]
			features = line[1:]
			if word in UNKhist:

				hasUNK = True

				if word not in UNKs_to_cells:
					UNKs_to_cells[word] = []
				UNKs_to_cells[word].append([len(sents_to_significance_matrix),len(row)])

				for feature in features:
					if feature in feature_significances:
						significance += feature_significances[feature]
					else:
						significance += minFeat

			if significance > max_significance:
				max_significance = significance

			row.append(significance)

		if hasUNK:
			matrix_to_map[len(sents_to_significance_matrix)] = rowID
			sents_to_significance_matrix.append(row)
			avg_sent_length[0] += len(row)
			avg_sent_length[1] += 1

		else:
			UNKless.append(s)

	### SCALE SCORES
	max_v = 0
	for rowID in range(len(sents_to_significance_matrix)):
		for columnID in range(len(sents_to_significance_matrix[rowID])):
			if sents_to_significance_matrix[rowID][columnID] > 0:
				sents_to_significance_matrix[rowID][columnID] = sents_to_significance_matrix[rowID][columnID] ** (math.log(2)/math.log(max_significance))
				### ACCOUNT FOR FREQUENCY
				sents_to_significance_matrix[rowID][columnID] *= UNKhist[unannotated[matrix_to_map[rowID]][columnID].split()[1]]

				max_v = max(sents_to_significance_matrix[rowID][columnID], max_v)

				# sents_to_significance_matrix[rowID][columnID] = ( (1 + sents_to_significance_matrix[rowID][columnID]) ** UNKhist[unannotated[matrix_to_map[rowID]][columnID].split()[1]] ) - 1

				# sents_to_significance_matrix[rowID][columnID] = ((1 + UNKhist[unannotated[matrix_to_map[rowID]][columnID].split()[1]]) ** sents_to_significance_matrix[rowID][columnID] ) - 1

	### RE-SCALE AFTER ACCOUNTING FOR FREQUENCY
	avg_sent_length = avg_sent_length[0]/avg_sent_length[1]
	for rowID in range(len(sents_to_significance_matrix)):
		sent_length = len(sents_to_significance_matrix[rowID])
		for columnID in range(sent_length):
			if sents_to_significance_matrix[rowID][columnID] > 0:
				sents_to_significance_matrix[rowID][columnID] = sents_to_significance_matrix[rowID][columnID] ** (math.log(2)/math.log(max_v))

		### APPEND SUM OF SCORES TO END OF EACH ROW
		# denominator = 1
		# denominator = sent_length+1
		# denominator = max((sent_length + (avg_sent_length - sent_length), sent_length))
		# denominator = max(sent_length,5)
		denominator = max(sent_length,avg_sent_length)
		for columnID in range(len(sents_to_significance_matrix[rowID])):
			sents_to_significance_matrix[rowID][columnID] /= denominator
		sents_to_significance_matrix[rowID].append(sum(sents_to_significance_matrix[rowID]))


	return UNKs_to_cells, sents_to_significance_matrix, UNKless, matrix_to_map

def REDrank_and_write_out(UNKs_to_cells, unannotated, sents_to_significance_matrix, matrix_to_map, UNKless, filename):
	rankedSents = []
	usedIDs = {}
	output = open(filename,'w')

	assert len(unannotated) == len(sents_to_significance_matrix) + len(UNKless)

	# for UNK in UNKs_to_cells:
	# 	for cell in UNKs_to_cells[UNK]:
	# 		assert cell[0] < len(sents_to_significance_matrix)
	# 		assert cell[1] < len(sents_to_significance_matrix[cell[0]]) - 1
	# print('GOOD TO GO!!')
	# sys.exit()

	# rank all the sentences containing UNKs by their summed significances
	while len(rankedSents) < len(sents_to_significance_matrix):
		bestSum = -1
		bestID = None
		for rowID in range(len(sents_to_significance_matrix)):
			if rowID not in usedIDs:
				s = sents_to_significance_matrix[rowID]

				if s[-1] > bestSum:
					bestSum = s[-1]
					bestID = rowID

		bestRow = unannotated[matrix_to_map[bestID]]
		assert bestID != None
		usedIDs[bestID] = True
		rankedSents.append(bestRow)

		printline = ''
		index = -1
		# assert len(sents_to_significance_matrix[bestID]) - 1 == len(bestRow)

		# having identified the most significant sentence..
		for l in bestRow:


			# debug
			# index += 1
			# # printline += l.split()[1]
			# if sents_to_significance_matrix[bestID][index] > 0:
			# 	printline += l.split()[1]
			# 	printline += '-'+str(round(sents_to_significance_matrix[bestID][index],3))
			# printline += ' '


			# write out the sentnece
			output.write('{}\n'.format(l))

			# update summed significances of every sentence and the list of UNK words
			word = l.split()[1]
			if word in UNKs_to_cells:
				for coordinates in UNKs_to_cells[word]:
					sents_to_significance_matrix[coordinates[0]][-1] -= sents_to_significance_matrix[coordinates[0]][coordinates[1]]
				del UNKs_to_cells[word]

		output.write('\n')

		### debug
			# if addedSents <= 10:
			# 	printline += '\t'+str(round(bestSum,3))
			# 	print(printline)
			# 	print(addedSents)
			# 	print()
			# else:
			# 	sys.exit()

	# add the UNKless sentences at the end of the while loop
	for s in UNKless:
		rankedSents.append(s)
		for line in s:
			output.write('{}\n'.format(line))
		output.write('\n')
	output.close()

	os.system("sed '/./,$!d' "+filename+" > "+filename+".2")
	os.system("mv "+filename+".2 "+filename)

	return rankedSents, len(sents_to_significance_matrix)

def rank_sents_and_write_out(sents_to_UNKs, UNKs_to_Egains, UNKless, filename, sents_annotated_to_error_reduction, totalUNKs, sentNum2length, avg_sent_length):
	output = open(filename,'w')

	# rank all of the sentences
	Egains_sents_list = 'start'
	progress = 0
	lastTens = '0'
	while len(Egains_sents_list) > 0:
		progress += 1
		# loop through all UNK containing sents
		add_to_UNKless = {}
		Egains_sents_list = []
		for s in sents_to_UNKs:
			denominator = max(sentNum2length[s], avg_sent_length)
			# sum the Egains of all UNKs therein
			Egain = 0.0
			for u in sents_to_UNKs[s]:
				if u in UNKs_to_Egains:
					Egain += UNKs_to_Egains[u] / denominator
			Egains_sents_list.append([Egain,s])
			if Egain == 0.0:
				add_to_UNKless[s] = True

		# sort sentences
		Egains_sents_list.sort(reverse=True)

		# pop the highest Egain sentence off the top
		l = Egains_sents_list.pop(0)
		s = l[1]

		# write out the sentnece
		for line in unannotated[s]:
			output.write('{}\n'.format(line))
		output.write('\n')

		# update sents_to_UNKs, UNKs_to_Egains, UNKless, sents_annotated_to_error_reduction
		UNKs = list(sents_to_UNKs[s].keys())
		new_gains = 0
		del sents_to_UNKs[s]
		for u in UNKs:
			if u in UNKs_to_Egains:
				new_gains += UNKs_to_Egains[u]
				del UNKs_to_Egains[u]
		sents_annotated_to_error_reduction[progress] = sents_annotated_to_error_reduction[progress-1] + new_gains
		for s in add_to_UNKless:
			del sents_to_UNKs[s]
			UNKless[s] = True

		proportionDone = str(round(100*(progress/(progress+len(sents_to_UNKs))),2))
		m = proportionDone.split('.')[0]
		if m[0] != lastTens and len(m) > 1:
			lastTens = m[0]
			print('SENTENCE RANKING PROGRESS: {}%'.format(proportionDone))

	# add the UNKless sentences at the end of the while loop
	for s in UNKless:
		for line in unannotated[s]:
			output.write('{}\n'.format(line))
		output.write('\n')
	output.close()

	os.system("sed '/./,$!d' "+filename+" > "+filename+".2")
	os.system("mv "+filename+".2 "+filename)

	for gains in sents_annotated_to_error_reduction:
		sents_annotated_to_error_reduction[gains] /= totalUNKs

	return sents_annotated_to_error_reduction, progress

def normalize_scores(dic, cieling):
	max_value = max(dic.values())
	for key in dic:
		try:
			dic[key] = dic[key] ** (math.log(cieling)/math.log(max_value))
		except OverflowError:
			print(dic[key])
			print(cieling)
			print(max_value)
			print(math.log(cieling))
			print(math.log(max_value))
			dic[key] = dic[key] ** (math.log(cieling)/math.log(max_value))

	return dic

def get_Seed_and_UNK_hists(corpus, args):
	unannotated = unrankedSort(corpus)
	seed = unrankedSort(args.seed)
	trainHist = {}
	if args.alwaysTrain != None:
		alwaysTrain = unrankedSort(args.alwaysTrain)
		trainHist = getHist(alwaysTrain)
	seedHist = getHist(seed)
	for w in trainHist:
		if w not in seedHist:
			seedHist[w] = trainHist[w]
		else:
			seedHist[w] += trainHist[w]
	### Get UNKhist and scale so the range is 0-2, controlling for outliers
	UNKhist = get_UNKhist(seedHist, unannotated)

	return seedHist, UNKhist

def updateDicts(sents, end_of_trusted_set, knownHist):
	avg_sent_length = [0,0]
	hardUNKs = {}
	word2sentNum = {}
	sentNum2word = {}
	sentNum2length = {}
	weight = 1
	for sNum in range(len(sents)):
		if sNum >= end_of_trusted_set:
			weight = 0.5
		s = sents[sNum]
		sent_length = len(s)
		sentNum2length[sNum] = sent_length
		avg_sent_length[0] += sent_length
		avg_sent_length[1] += 1
		for lNum in range(sent_length):
			l = s[lNum]
			word = l.split()[1]
			label = l.split()[0]
			if word not in knownHist:
				if word not in word2sentNum:
					word2sentNum[word] = {}
				if sNum not in sentNum2word:
					sentNum2word[sNum] = {}
				if word not in hardUNKs:
					hardUNKs[word] = 0
				word2sentNum[word][sNum] = True
				sentNum2word[sNum][word] = True
				if label != '0':
					hardUNKs[word] += weight
				else:
					hardUNKs[word] += 0.0000000000001

	return avg_sent_length, hardUNKs, word2sentNum, sentNum2word, sentNum2length

###################################################################

parser = argparse.ArgumentParser()
parser.add_argument('-corpus', type=str, help='Where is the prepared corpus located?', required=True)
parser.add_argument('-seed', type=str, help='Where is the seed corpus located?', required=False, default=None)
parser.add_argument('-alwaysTrain', type=str, help='Is there any annotation thats been done in addition to the seed?', required=False, default=None)
parser.add_argument('-predictions', type=str, help='Where is the models predictions for labeling the unannotated data? Predictions should record sentence and marginal probabilities.', required=False)
parser.add_argument('-sort_method', type=str, help='How should we rank the sentences to be annotated?', choices=['unranked','random','random_seed','set_seed','hardCappedUNKs','rapidUncertainty','rapidEntityDiversity','preTag_delex'], required=False, default='unranked')
parser.add_argument('-output', type=str, help='Where do you want the output file(s)?', required=False)
parser.add_argument('-annotate', type=str, help='Do you want to identify sentences to annotate?', required=False, default=None)
parser.add_argument('-entities', type=str, help='underscore delimited list of types of named entities', required=False, default=None)
parser.add_argument('-load_annotation', type=bool, help='Do you want to replace unannotated sentences with new annotations?', required=False, default=False)
parser.add_argument('-topXsents', type=int, help='How many sentences do you want to deal with?', required=False, default=99999999999999999999999999)
parser.add_argument('-topXlines', type=int, help='This should be the line number for the blank line separating the sentences you want to use as seed from the remaining sentences you want to tag.', required=False)
parser.add_argument('-topXentities', type=int, help='How many sentences do you want to deal with?', required=False, default=0)
args = parser.parse_args()

corpus = args.corpus
sortBy = args.sort_method
output = args.output
topXsents = args.topXsents
topXentities = args.topXentities
if args.alwaysTrain == 'None':
	args.alwaysTrain = None

if sortBy == 'random_seed':
	corpus = randomSort(corpus)
	if topXentities == 0:
		random_seed = corpus[0:topXsents]
		unannotated = corpus[topXsents:]
	else:
		NE_count = 0
		for s in range(len(random_corpus)):
			for l in random_corpus[s]:
				if l.split()[0] != '0':
					NE_count += 1
			if NE_count >= topXentities:
				cutoff = s 
				break
		random_seed = random_corpus[0:cutoff]
		unannotated = random_corpus[cutoff:]

	print_annotation(random_seed,output+'.seed')
	print("\nPlease annotate any relevant entities in the random seed file:\n\n\t{}\n\nMake sure the finished annotation gets saved with the same filename.\n".format(output+'.seed'))
	print_annotation(unannotated,output+'.unannotated')

elif sortBy == 'set_seed':
	corpus = unrankedSort(corpus)
	total_lines = 0
	set_seed = []
	unannotated = []
	for s in corpus:
		total_lines += len(s) + 1
		if total_lines > args.topXlines:
			unannotated.append(s)
		else:
			set_seed.append(s)

	print_annotation(set_seed, output+'.seed')
	print('\nPlease annotate the sentences in the file\n\t{}\n'.format(output+'.seed'))
	print_annotation(unannotated, output+'.unannotated')

elif sortBy == 'hardCappedUNKs':

	seed = unrankedSort(args.seed)
	trainHist = {}
	if args.alwaysTrain != None:
		alwaysTrain = unrankedSort(args.alwaysTrain)
		trainHist = getHist(alwaysTrain)
	seedHist = getHist(seed)
	for w in trainHist:
		if w not in seedHist:
			seedHist[w] = trainHist[w]
		else:
			seedHist[w] += trainHist[w]

	rankedSents, limit = hard_capped_UNK_sort_and_write_out(corpus, output, seedHist)
	print('\n\nPlease annotate (in order) the ranked sentences in:\n\t{}\n'.format(output))
	print('The marginal benefit of annotating an additional sentence will start high and decrease until youve annotated {} sentences, after which, marginal gains will be negligible'.format(str(limit)))

elif sortBy == 'random':
	rankedSents = random_sort_and_write_out(corpus, output)
	print('\n\nPlease annotate the random sentences in:\n\t{}'.format(output))

elif sortBy == 'preTag_delex':

	knownHist, UNKhist = get_Seed_and_UNK_hists(corpus, args)
	seed = args.seed
	unannotated = args.corpus
	if args.alwaysTrain == None:
		alwaysTrain = 'None'
	else:
		alwaysTrain = args.alwaysTrain

	### generate dummy seed, alwaysTrain, and unannotated corpora
		# preTag all of them
		# get features and deLexicalize them
	### train one system on the dummy seed + dummy alwaysTrain
		# test it on unannotated and save the results
	### train one system on half of dummy NE-containing sents from unannotated, another on the other half
		# test each on the opposite half + mutually exclusive completely exhaustive halves of the dummy unannotated sents lacking preTagged NEs
		# align the predictions with words and save alignment

	os.system('sh Scripts/preTag_deLex_pipeline.sh {} {} {} {}'.format(seed, alwaysTrain, unannotated, args.entities))

	# test results from training on delexicalized annotated labels, split 0
	sents_1 = unrankedSort('Data/Splits/test_0.aligned')
	end_of_trusted_set = len(sents_1)
	sents = list(sents_1)
	# test results from training on delexicalized preTagged labels, split 1
	sents.extend(unrankedSort('Data/Splits/test_1.aligned'))
	# test results from training on delexicalized preTagged labels, split 2
	sents.extend(unrankedSort('Data/Splits/test_2.aligned'))

	# UNK unannotated words that were labeled by split 0 get higher priority
	avg_sent_length, ignore, word2sentNum, sentNum2word, sentNum2length = updateDicts(sents_1, end_of_trusted_set, knownHist)

	ignore, hardUNKs, ignore_1, ignore_2, ignore_3 = updateDicts(sents, end_of_trusted_set, knownHist)
	sents = sents_1
	avg_sent_length = avg_sent_length[0]/avg_sent_length[1]

	# consider doing some sort of frequency based normalization to lessen the effect it has here
		# may not be necessary though, because we do want to address the more frequent words first
	rankedHardUNKs = sorted([(hardUNKs[k], k) for k in hardUNKs.keys()], reverse=True)

	### GET AS MANY HIGH WEIGHTED HARD UNK WORDS AS FAST AS POSSIBLE
	alreadyIncludedWords = dict(knownHist)
	alreadyIncludedSents = {}
	rankedSents = []
	for t in range(len(rankedHardUNKs)):
		word = rankedHardUNKs[t][1]
		if word not in alreadyIncludedWords:
			bestAddedFreqs = -1
			for sNum in word2sentNum[word]:
				if sNum not in alreadyIncludedSents:

					denominator = max(sentNum2length[sNum],avg_sent_length)

					addedFreqs = 0
					for w in sentNum2word[sNum]:

						# addedFreqs += hardUNKs[w]
						addedFreqs += hardUNKs[w] / denominator

					if addedFreqs > bestAddedFreqs:
						bestAddedFreqs = addedFreqs
						bestSent = sNum 
			for w in sentNum2word[bestSent]:
				alreadyIncludedWords[w] = True
			alreadyIncludedSents[bestSent] = True
			rankedSents.append(sents[bestSent])

	limit = len(rankedSents)
	# append the rest of the sents
	for sNum in range(len(sents)):
		if sNum not in alreadyIncludedSents:
			rankedSents.append(sents[sNum])

	os.system('rm Data/Splits/test_*aligned')

	sents2defaultTags = {}
	unannotated = unannotated.replace('.fts','')
	original = unrankedSort(unannotated)
	for s in original:
		sentence = []
		tags = []
		for l in s:
			word = l.split()[1]
			label = l.split()[0]
			sentence.append(word)
			tags.append(label)
		sents2defaultTags[' '.join(sentence)] = tags

	# write out
	op = open(output,'w')
	for s in rankedSents:
		sentence = []
		for l in s:
			sentence.append(l.split()[1])
		sent = ' '.join(sentence)
		defaultTags = sents2defaultTags[sent]

		for i in range(len(sentence)):
			op.write('{}\t{}\n'.format(defaultTags[i],sentence[i]))
		op.write('\n')
	op.close()

	os.system("sed '/./,$!d' "+output+" > "+output+".2")
	os.system("mv "+output+".2 "+output)

