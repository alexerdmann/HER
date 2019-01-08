import pickle
import sys
import os 
import fileinput
import random
import argparse
import itertools
import time
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

corpus = sys.argv[1]
predefinedEntities = sys.argv[2]
predefinedEntities = predefinedEntities.split('_')
sents = unrankedSort(corpus)

if len(sys.argv) > 3:
	gazatteers = sys.argv[3:]

	NEs2labels = {}
	gazzes = {}
	gaz2max = {}
	for gaz in gazatteers:
		try:
			maxLen = 0
			label = gaz.split('/')[-1].split('.')[0]
			if label in predefinedEntities:
				gazzes[label] = {}
				for line in fileinput.input(gaz):
					line = ' '.join(line.split())
					for ch in line:
						if ch in string.punctuation:
							line = line.replace(ch,'')
					if len(line.split()) > 0:
						length = len(line.split())
						if length not in gazzes:
							gazzes[label][length] = {}
						gazzes[label][length][line] = True
						NEs2labels[line] = label
						if length > maxLen:
							maxLen = length
							gaz2max[gaz] = maxLen
				fileinput.close()
			# else:
			# 	# os.system('echo "THE '+label+' GAZATTEER WILL ONLY BE USED FOR FEATURES AND NOT FOR TAGGING BECAUSE IT WAS NOT LISTED AMONG THE DESIRED ENTITIES TO EXTRACT:"')
			# 	# os.system('echo "'+' '.join(predefinedEntities)+'"')
			# 	# os.system('echo "PLEASE ENSURE THAT THIS WAS INTENTIONAL AND NOT DUE TO A TYPO"')
			# 	# time.sleep(0.1)

		except FileNotFoundError:
			pass

	maxLens = list(gaz2max.values())
	maxLens.sort(reverse=True)
	if len(maxLens) > 0:
		maxLen = maxLens[0]
	else:
		maxLen = 0

	for s in range(len(sents)):
		sent = []
		sentLabels = []
		for l in range(len(sents[s])):
			word = sents[s][l].split()[1]
			for ch in word:
				if ch in string.punctuation:
					word = word.replace(ch,'')
			sent.append(word)
			sentLabels.append(sents[s][l].split()[0])

		for n in range(maxLen,0,-1):
			for start in range(0,len(sent)):
				if start + n <= len(sent):
					ngram = ' '.join(sent[start:start+n])
					if ngram in NEs2labels:
						

						### got a match, checking to make sure it hasn't already been incorporated into a larger NE span
						go = True
						for ind in range(start, start+n):
							if sentLabels[ind] != '0':
								go = False

						### pre-tagging
						if go:
							counter = -1
							for ind in range(start, start+n):
								counter += 1
								label = '{}-'.format(NEs2labels[ngram])
								if counter == 0:
									label += 'B'
								else:
									label += 'I'
								sentLabels[ind] = label
								sents[s][ind] = '{}\t{}'.format(label,'\t'.join(sents[s][ind].split()[1:]))

### DEBUG print just sents with pretagged entities
# for s in sents:
# 	go = False
# 	for l in s:
# 		if l.split()[0] != '0':
# 			go = True
# 	if go:
# 		for l in s:
# 			print(l)
# 		print()

### PRINT SENTS
for s in sents:
	for l in s:
		print(l)
	print()





