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
	if word[0].isupper():
		line += '\twordShape=capped'
	return line

def getWordShapeAdvanced(line,corpus,ind):
	word = line.split()[1]
	if word[0].isupper():
		if word[-1] == '.':
			line += '\twordShape=abbrev'
		else:
			caps = 0
			for ch in word:
				if ch.isupper():
					caps += 1
			if caps == len(word):
				line += '\twordShape=allCaps'
			elif caps == 1:
				line += '\twordShape=titleCase'
			else:
				line += '\twordShape=mixedCase'
	return line

def getPrevWordShape(line,corpus,ind):
	try:
		for feat in getWordShape(corpus[ind-1],corpus,ind-1).split()[1:]:
			if 'wordShape=' in feat:
				line += '\tprev'+feat
	except IndexError:
		pass
	return line

def getNextWordShape(line,corpus,ind):
	try:
		if ind+1 != len(corpus):
			for feat in getWordShape(corpus[ind+1],corpus,ind+1).split()[1:]:
				if 'wordShape=' in feat:
					line += '\tnext'+feat
	except IndexError:
		pass
	return line

def getPrevBiWordShape(line,corpus,ind):
	feat2ad = 'prevBi'
	for bi in range(1,3):
		addedFeat = False
		if ind-bi >= 0:
			for feat in getWordShape(corpus[ind-bi],corpus,ind-bi).split()[1:]:
				if 'wordShape=' in feat:
					feat2ad += '-'+feat
					addedFeat = True
		if addedFeat == False:
			feat2ad += '-None'

	line += '\t'+feat2ad

	return line

def getNextBiWordShape(line,corpus,ind):
	feat2ad = 'nextBi'
	for bi in range(1,3):
		addedFeat = False
		if ind+bi < len(corpus):
			for feat in getWordShape(corpus[ind+bi],corpus,ind+bi).split()[1:]:
				if 'wordShape=' in feat:
					feat2ad += '-' + feat
					addedFeat = True
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
	for bi in range(1,3):
		try:
			prevWords += '-' + corpus[ind-bi].split()[1]
		except IndexError:
			prevWords += '-NONE'
	line += '\t'+prevWords
	return line

def getNextBiWord(line,corpus,ind):
	nextWords = 'prevBi'
	for bi in range(1,3):
		try:
			nextWords += '-' + corpus[ind+bi].split()[1]
		except IndexError:
			nextWords += '-NONE'
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

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	############# GENERAL ARGUMENTS ##################################
	parser.add_argument('-corpus', type=str, help='preprocessed corpus with one word per line and a blank space between each sentence. Each line contains the label followed by relevant lexical features, all tab separated.', required=True)
	parser.add_argument('-hist', type=str, help='pickled histogram of the corpus.', required=True)
	parser.add_argument('-fullCorpus', type=str, help='location of the full corpus.', required=False, default='Data/Prepared/fullCorpus.txt')
	parser.add_argument('-features', nargs='+', help='These are the features to include along with the word itself to help the crf classify.', required=False, choices=['wordShape','charNgrams','prevCharNgrams','postCharNgrams','prevWordShape','nextWordShape','prevWord','nextWord','prevBiWord','nextBiWord','prevBiWordShape','nextBiWordShape','histStats','None'], default=None)
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

	### for each line in the corpus, add any specified features
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

		print(line)
	
