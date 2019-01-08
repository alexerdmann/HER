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

	if len(sent) > 0:
		rankedSents.append(sent)

	return rankedSents

annotated = sys.argv[1]
sents = unrankedSort(annotated)
NEs2labels = {}

if len(sys.argv) > 2:
	gazatteers = sys.argv[2:]

	NEs2labels = {}
	gazzes = {}
	gaz2max = {}
	for gaz in gazatteers:
		try:
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

					if line not in NEs2labels:
						NEs2labels[line] = {}

					NEs2labels[line][label] = True
					if length > maxLen:
						maxLen = length
						gaz2max[gaz] = maxLen
			fileinput.close()
		except FileNotFoundError:
			pass

### GO THROUGH ANNOTATED CORPUS AND ADD TO NES2LABELS
NE = []
label = None
for s in sents:
	for l in s:
		l = l.split()

		# IF IT'S IN AN NE
		if '-' in l[0]:
			tag = l[0].split('-')[0]
			pos = l[0].split('-')[1]
			word = l[1]

			# IF IT'S THE START OF AN NE
			if pos == 'B' or tag != label:

				# IF A PREVIOUS NE HAS NOT BEEN RECORDED YET
				if label != None:
					ne = ' '.join(NE)
					if ne not in NEs2labels:
						NEs2labels[ne] = {}
					NEs2labels[ne][label] = True

				# REGARDLESS OF PREVIOUS NE, WE WANT TO RESET NE AND LABEL NOW
				NE = [word]
				label = tag

			# IF WE ARE AT A NON INITIAL WORD IN MWE NE
			else:
				NE.append(word)

		# IF WE DO NOT HAVE AN NE
		else:

			# IF WE HAVEN'T RECORDED A PREVIOUS NE YET 
			if label != None:
				ne = ' '.join(NE)
				if ne not in NEs2labels:
					NEs2labels[ne] = {}
				NEs2labels[ne][label] = True

			# RESET LABEL AND NE TO EMPTY DEFAULT
			label = None
			NE = []

	# IF WE HAVEN'T RECORDED A PREVIOUS NE BY THE TIME WE REACH A SENTENCE ENDING
	if label != None:
		ne = ' '.join(NE)
		if ne not in NEs2labels:
			NEs2labels[ne] = {}
		NEs2labels[ne][label] = True
		label = None
		NE = []

labels2NEs = {}
for NE in NEs2labels:
	for label in NEs2labels[NE]:
		if label not in labels2NEs:
			labels2NEs[label] = {}
		labels2NEs[label][NE] = True

### OVERWRITE THE GAZATTEERS
for label in labels2NEs:
	f = open('Data/Gazatteers/'+label+'.gaz','w')
	for NE in labels2NEs[label]:
		f.write('{}\n'.format(NE))
	f.close()



