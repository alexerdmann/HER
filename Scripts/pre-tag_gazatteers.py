import pickle
import sys
import os 
import fileinput
import random
import argparse
import itertools
import time
import math

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

corpus = sys.argv[1]
sents = unrankedSort(corpus)

if len(sys.argv) > 2:
	gazatteers = sys.argv[2:]

	NEs2labels = {}
	gazzes = {}
	gaz2max = {}
	for gaz in gazatteers:
		maxLen = 0
		label = gaz.split('/')[-1].split('.')[0]
		gazzes[label] = {}
		for line in fileinput.input(gaz):
			line = ' '.join(line.split())
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

	maxLens = list(gaz2max.values())
	maxLens.sort(reverse=True)
	maxLen = maxLens[0]

	for s in range(len(sents)):
		sent = []
		sentLabels = []
		for l in range(len(sents[s])):
			sent.append(sents[s][l].split()[1])
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





