import fileinput
import sys

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

corpus = unrankedSort(corpus)

NEs = {}
NE_so_far = []
currentLabel = None
for s in corpus:
	# if the last sentence ended with an NE
	if len(NE_so_far) > 0:
		if currentLabel not in NEs:
			NEs[currentLabel] = {}
		NE = ' '.join(NE_so_far)
		if NE not in NEs[currentLabel]:
			NEs[currentLabel][NE] = 0
		NEs[currentLabel][NE] += 1
		NE_so_far = []
		currentLabel = None
	# otherwise, loop through each line
	for l in s:
		newLabel = l.split()[0].split('-')[0]
		if newLabel == '0':
			if len(NE_so_far) > 0:
				if currentLabel not in NEs:
					NEs[currentLabel] = {}
				NE = ' '.join(NE_so_far)
				if NE not in NEs[currentLabel]:
					NEs[currentLabel][NE] = 0
				NEs[currentLabel][NE] += 1
				NE_so_far = []
			currentLabel = None
		else:
			try:
				position = l.split()[0].split('-')[1]
			except IndexError:
				print('ANNOTATION ERROR IN THE FOLLOWING SENTENCE, PLEASE FIX:\n{}'.format('\n'.join(s)))
				sys.exit()
			word = l.split()[1]
			if position == 'B':
				if len(NE_so_far) > 0:
					if currentLabel not in NEs:
						NEs[currentLabel] = {}
					NE = ' '.join(NE_so_far)
					if NE not in NEs[currentLabel]:
						NEs[currentLabel][NE] = 0
					NEs[currentLabel][NE] += 1
					NE_so_far = []
			currentLabel = newLabel
			NE_so_far.append(word)

for label in NEs:
	print(label.upper())
	for NE in NEs[label]:
		print('\t{} \t{}'.format(NE,str(NEs[label][NE])))

