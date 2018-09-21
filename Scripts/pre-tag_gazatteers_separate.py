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
out_withNEs_1 = sys.argv[2]
out_withoutNEs_1 = sys.argv[3]
out_withNEs_2 = sys.argv[4]
out_withoutNEs_2 = sys.argv[5]
sents = unrankedSort(corpus)

if len(sys.argv) > 6:
	gazatteers = sys.argv[6:]

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

### WRITE OUT SENTS
out_withoutNEs_1 = open(out_withoutNEs_1,'w')
out_withNEs_1 = open(out_withNEs_1,'w')
out_withoutNEs_2 = open(out_withoutNEs_2,'w')
out_withNEs_2 = open(out_withNEs_2,'w')

with1 = True
without1 = True

for s in sents:
	foundNE = False
	for l in s:
		if l.split()[0] != '0':
			foundNE = True
			break
	if foundNE:
		if with1:
			for l in s:
				out_withNEs_1.write('{}\n'.format(l))
			out_withNEs_1.write('\n')
			with1 = False
		else:
			for l in s:
				out_withNEs_2.write('{}\n'.format(l))
			out_withNEs_2.write('\n')
			with1 = True
	else:
		if without1:
			for l in s:
				out_withoutNEs_1.write('{}\n'.format(l))
			out_withoutNEs_1.write('\n')
			without1 = False
		else:
			for l in s:
				out_withoutNEs_2.write('{}\n'.format(l))
			out_withoutNEs_2.write('\n')
			without1 = True







