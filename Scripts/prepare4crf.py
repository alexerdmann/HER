from __future__ import print_function
from __future__ import division

""" USERS WILL NEED TO DEFINE WHAT TYPES OF ANNOTATIONS THEY WANT TO PRESERVE IF THERE IS PRE EXISTING ANNOTATION """

import sys
import fileinput
import string
import time

file = sys.argv[1]

""" THE USER SHOULD DEFINE WHAT ANNOTATIONS THEY ARE USING HERE """
labelMapping = {}
labelMapping['$'] = 'GEO'
###################################################################


### tokens that will stop a sentence
stops = {}
for s in ['.',';','!','?']:
	stops[s] = True
### non-word tokens that should never stop a sentence
notWords = {}
# i.e., punctuation
for p in string.punctuation:
	notWords[p] = True
# and named entity labels
for l in labelMapping:
	notWords[l] = True


### break test into sentences
sentences = []
sentence = []
lookingForClosure = False
for line in fileinput.input(file):
	line = line.replace('&apos;',"'").replace('&quot;','"')
	line = line.split()
	for i in range(len(line)):
		w = line[i]
		if lookingForClosure:
			if w in notWords:
				sentence.append(w)
			else:
				sentences.append(sentence)
				sentence = [w]
				lookingForClosure = False

		else:
			sentence.append(w)
			if w in stops:
				lookingForClosure = True

fileinput.close()


### require that all named entities not start or end with punctuation
lookingForClosure = None
for s in range(len(sentences)):
	for i in range(len(sentences[s])):
		w = sentences[s][i]
		### IF WE ARE EITHER AT THE BEGINNING OR END OF A NAMED ENTITY SPAN
		if w in labelMapping:
			sentences[s][i] = ''
			### IF WE'VE FOUND THE END OF A SPAN
			if lookingForClosure != None:

				### HANDLE STARTING NON-WORD SEQUENCE
				start = lookingForClosure
				for k in range(lookingForClosure,i):
					if sentences[s][k] in notWords:
						sentences[s][k] = '0\t'+sentences[s][k]
						start += 1
					else:
						break

				### HANDLE ENDING NON-WORD SEQUENCE
				end = i
				for k in range(i-1,start-1,-1):
					if sentences[s][k] in notWords:
						sentences[s][k] = '0\t'+sentences[s][k]
						end -= 1

				### LABEL THE TRUE NAMED ENTITY SPAN
				length = end - start
				if length == 1:
					labels = ['-B']
				elif length == 2:
					labels = ['-B','-I']
				else:
					labels = ['-B']
					for t in range(1,length-1):
						labels.append('-I')
					labels.append('-I')
				for k in range(start,end):
					label = labelMapping[w]+labels.pop(0)
					sentences[s][k] = label+'\t'+sentences[s][k]

				### TURN OFF LOOKING FOR CLOSURE
				lookingForClosure = None

			### IF WE'VE FOUND THE BEGINNING OF A SPAN, REMEMBER WHERE IT WAS
			else:
				lookingForClosure = i+1
		elif lookingForClosure == None:
			sentences[s][i] = '0\t'+sentences[s][i]


### PRINT OUT THE FINAL LABELS IN CRFSUITE FORMAT
for s in sentences:
	lenSent = 0
	for w in s:

		# disallow extremely long sentences that might break CRFsuite
		lenSent += 1
		if lenSent > 200:
			print()

		if len(w.split()) == 2:
			print(w)
	print()

