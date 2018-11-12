import sys
import argparse
import string
import pickle
import fileinput

def pickleIn(file):
	pklFile = open(file,'rb')
	ofTheKing =pickle.load(pklFile)
	pklFile.close()
	return ofTheKing

def pickleOut(shit,file):
	pklFile = open(file,'wb')
	pickle.dump(shit,pklFile)
	pklFile.close()
	
def getHist(fullCorpus, hist_dest):
	hist = {}
	try:
		for line in fileinput.input(fullCorpus):
			if len(line.split()) > 1:
				w = line.split()[1]
				if w not in hist:
					hist[w] = 0
				hist[w] += 1
		fileinput.close()
	except FileNotFoundError:
		print('Pray tell, where is the full corpus located? Please add the argument -fullCorpus <path-to-fullCorpus> to your command.')
		sys.exit()
	pickleOut(hist,hist_dest)

def getWordShape(line,corpus,ind):

	word = line.split()[1]
	moreCaps = False
	digits = False
	puncts = False
	letters = False

	start = True
	for char in word:
		if char in string.punctuation:
			puncts = True 
		elif char.isdigit():
			digits = True
		elif char.isalpha():
			letters = True
		elif start == False and char.isupper():
			moreCaps = True
		start = False

	# ABBREV
	if word[-1] == '.' and letters and digits == False: #word[0].isupper():
		line += '\twordShape=abbrev'

	# OTHER WORD INITIAL CAPS
	elif word[0].isupper():
		# MIXED
		if digits or puncts:
			line += '\twordShape=mixed'
		# ALL CAPS
		elif moreCaps:
			line += '\twordShape=allCaps'
		# CAPPED
		else:
			line += '\twordShape=capped'

	# NON ALPHABETICAL
	elif letters == False:
		# PUNCTUATION
		if puncts and digits == False:
			line += '\twordShape=punct'
		# NUMBERS WITH PUNCTUATION
		elif digits and puncts:
			line += '\twordShape=mixedNumber'
		# JUST NUMBERS
		elif digits:
			line += '\twordShape=number'

	# ALPHABETICAL WITH PUNCTUATION AND OR DIGITS
	elif puncts or digits:
		line += '\twordShape=mixed'

	return line

def getPrevWordShape(line,corpus,ind):
	try:
		for feat in getWordShape(corpus[ind-1],corpus,ind-1).split()[1:]:
			if 'wordShape=' in feat and 'wordShape=' == feat[0:10]:
				line += '\tprev'+feat
	except IndexError:
		pass
	return line

def getNextWordShape(line,corpus,ind):
	try:
		if ind+1 != len(corpus):
			for feat in getWordShape(corpus[ind+1],corpus,ind+1).split()[1:]:
				if 'wordShape=' in feat and 'wordShape=' == feat[0:10]:
					line += '\tnext'+feat
	except IndexError:
		pass
	return line

def getWordLength(line,corpus,ind):
	word = line.split()[1]
	line += '\t{}'.format(str(len(word)))

	return line

def getPrevBiWordShape(line,corpus,ind):
	feat2ad = 'prevBiWS'
	go = True
	for bi in range(1,3):
		addedFeat = False
		try:
			if go:
				for feat in getWordShape(corpus[ind-bi],corpus,ind-bi).split()[1:]:
					if 'wordShape=' in feat and 'wordShape=' == feat[0:10]:
						feat2ad += '-'+feat
						addedFeat = True
		except IndexError:
			go = False
		if addedFeat == False:
			feat2ad += '-None'

	line += '\t'+feat2ad

	return line

def getNextBiWordShape(line,corpus,ind):
	feat2ad = 'nextBiWS'
	go = True
	for bi in range(1,3):
		addedFeat = False
		try:
			if go:
				for feat in getWordShape(corpus[ind+bi],corpus,ind+bi).split()[1:]:
					if 'wordShape=' in feat and 'wordShape=' == feat[0:10]:
						feat2ad += '-'+feat
						addedFeat = True
		except IndexError:
			go = False
		if addedFeat == False:
			feat2ad += '-None'

	line += '\t'+feat2ad

	return line

def getPrevWord(line,corpus,ind):
	try:
		prevWord = corpus[ind-1].split()[1]
	except IndexError:
		prevWord = 'NONE'
	line += '\tprevWord='+prevWord
	return line

def getNextWord(line,corpus,ind):
	try:
		nextWord = corpus[ind+1].split()[1]
	except IndexError:
		nextWord = 'NONE'
	line += '\tnextWord='+nextWord
	return line

def getPrevBiWord(line,corpus,ind):
	prevWords = 'prevBi'
	go = True
	for bi in range(1,3):
		try:
			if go:
				prevWords += '-' + corpus[ind-bi].split()[1]
			else:
				prevWords += '-NONE'
		except IndexError:
			prevWords += '-NONE'
			go = False
	line += '\t'+prevWords
	return line

def getNextBiWord(line,corpus,ind):
	nextWords = 'nextBi'
	go = True
	for bi in range(1,3):
		try:
			if go:
				nextWords += '-' + corpus[ind+bi].split()[1]
			else:
				nextWords += '-NONE'
		except IndexError:
			nextWords += '-NONE'
			go = False
	line += '\t'+nextWords
	return line

def getCharNgrams(line,corpus,ind):
	word = line.split()[1]
	for i in range(len(word)):
		for n in range(2,7):
			if i+n < len(word):
				### comment this next line out if you want to get word medial n-grams
				if i == 0 or i+n == len(word):
				####
					line += '\tcharNgram='+word[i:i+n]
	return line

def getHistStats(line,corpus,ind,hist):
	word = line.split()[1]
	if word[0].isupper():
		word2 = word[0].lower() + word[1:]
		if word2 in hist:
			line += '\telsewhereLower\t'+word2
	
	elif word[0].islower():
		word2 = word[0].upper() + word[1:]
		if word2 in hist:
			line += '\telsewhereUpper\t'+word2

	return line

def getContextPosition(line,corpus,ind):
	if ind-1 < 0 or len(corpus[ind-1].split()) == 0:
		line += '\tsentInitial'
	if ind+1 == len(corpus) or len(corpus[ind+1].split()) == 0:
		line += '\tsentFinal'

	return line

def getGazMembership(line,corpus,ind,NEs2labels):
	word = line.split()[1]
	if word in NEs2labels:
		for label in NEs2labels[word]:
			line += '\tGaz-{}'.format(label)
	else:
		lWord = word.lower()
		if lWord in NEs2labels:
			for label in NEs2labels[lWord]:
				line += '\tGaz-{}'.format(label)

	return line

def getNEs2labels(gazatteers):
	NEs2labels = {}
	for gaz in gazatteers:
		label = gaz.split('/')[-1].split('.')[0]
		for line in fileinput.input(gaz):
			line = ' '.join(line.split())
			if len(line.split()) > 0:
				if line not in NEs2labels:
					NEs2labels[line] = {}
				NEs2labels[line][label] = True
		fileinput.close()

	return NEs2labels

def deLex(line):
	line = line.split()

	if len(line) > 0:
		label = line[0]
		if label != '0':
			label = 'NE' #-{}'.format(label.split('-')[1])
		newLine = [label]
		for i in range(2,len(line)):
			feat = line[i]
			if 'Gaz-' not in feat and 'charNgram=' not in feat:
				newLine.append(feat)
		if 'elsewhereLower' in newLine:
			del newLine[newLine.index('elsewhereLower')+1]
		if 'elsewhereUpper' in newLine:
			del newLine[newLine.index('elsewhereUpper')+1]

		line = '\t'.join(newLine)
	else:
		line = ''

	return line

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	############# GENERAL ARGUMENTS ##################################
	parser.add_argument('-corpus', type=str, help='preprocessed corpus with one word per line and a blank space between each sentence. Each line contains the label followed by relevant lexical features, all tab separated.', required=True)
	parser.add_argument('-hist', type=str, help='pickled histogram of the corpus.', required=True)
	parser.add_argument('-fullCorpus', type=str, help='location of the full corpus.', required=False, default='Data/Prepared/fullCorpus.txt')
	parser.add_argument('-features', nargs='+', help='These are the features to include along with the word itself to help the crf classify.', required=False, choices=['wordShape','charNgrams','prevCharNgrams','postCharNgrams','prevWordShape','nextWordShape','prevWord','nextWord','prevBiWord','nextBiWord','prevBiWordShape','nextBiWordShape','histStats','contextPosition','gazatteers','wordLength','deLex','None'], default=None)
	parser.add_argument('-gazatteers', nargs='+', help='These are the gazatteer files.', required=False, default=None)
	parser.add_argument('-simplify', type=bool, help='Do you want to ignore multi-word entity spans?', required=False, default=False)
	##################################################################

	args = parser.parse_args()

	corpus = (open(args.corpus).read().splitlines())

	try:
		hist = pickleIn(args.hist)
	except:
		getHist(args.fullCorpus, args.hist)
		hist = pickleIn(args.hist)

	features = args.features

	if 'gazatteers' in features:
		if args.gazatteers == None:
			print('YOU NEED TO SPECIFY WHERE THE GAZATTEERS ARE LOCATED WITH THE OPTION -gazatteers')
			sys.exit()
		NEs2labels = getNEs2labels(args.gazatteers)

	### for each line in the corpus, add any specified features
	lines = []
	for ind in range(len(corpus)):

		line = corpus[ind]

		if len(line.split()) == 1:
			print('PROBLEM!!!')
			print(line)
			sys.exit()


		if len(line.split()) > 0:

			### SIMPLIFY SEQUENCE BASED TAGS
			# simplify by ignoring multi-word entity spans
			# label = line.split()[0]
			# if len(label) > 0 and '-simplify' in sys.argv:
			# 	if label[-1] in ['-B','-I']:
			# 		label = label[0:-1]
			# 	line = label+'\t'+'\t'.join(line.split()[1:])

			### REMOVE ANY FEATURES BEYOND THE WORD ITSELF
			line = '\t'.join(line.split()[0:2])

			# capitalization
			if 'wordShape' in features:
				line = getWordShape(line,corpus,ind)

			if 'prevWordShape' in features:
				line = getPrevWordShape(line,corpus,ind)

			if 'nextWordShape' in features:
				line = getNextWordShape(line,corpus,ind)

			if 'prevWord' in features:
				line = getPrevWord(line,corpus,ind)

			if 'nextWord' in features:
				line = getNextWord(line,corpus,ind)

			# character n-grams
			if 'charNgrams' in features:
				line = getCharNgrams(line,corpus,ind)

			# preceding bigrams
			if 'prevBiWord' in features:
				line = getPrevBiWord(line,corpus,ind)

			# following bigrams
			if 'nextBiWord' in features:
				line = getNextBiWord(line,corpus,ind)

			# preceding bigram wordshape
			if 'prevBiWordShape' in features:
				line = getPrevBiWordShape(line,corpus,ind)

			# following bigrams wordshape
			if 'nextBiWordShape' in features:
				line = getNextBiWordShape(line,corpus,ind)

			# mark words elsewhere capitalized or elsewhere uncapitalized
			if 'histStats' in features:
				line = getHistStats(line,corpus,ind,hist)

			if 'contextPosition' in features:
				line = getContextPosition(line,corpus,ind)

			if 'gazatteers' in features:
				line = getGazMembership(line,corpus,ind,NEs2labels)

			if 'wordLength' in features:
				line = getWordLength(line,corpus,ind)

		if 'deLex' not in features:
			print(line)
		else:
			lines.append(line)

				###

	if 'deLex' in features:
		for line in lines:
			print(deLex(line))
	
