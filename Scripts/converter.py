import sys
import fileinput
import random

"""
python converter.py input_file input_form output_form output_file

presently supported forms: crf conll
forms to add: bioes
"""

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

	if len(sent) > 0:
		rankedSents.append(sent)
	fileinput.close()
	return rankedSents

class converter:

	def __init__(self, input_file, f):
		self.corpus = unrankedSort(input_file)
		self.origFileName = input_file
		self.format = f

	def convert(self, output_format):
		
		if self.format == 'crf' and output_format == 'conll':

			newSents = []

			for sent in self.corpus:
				newSent = []
				label_base = None

				for line in sent:
					line = line.split()

					label = line[0].split('-')
					if len(label) == 1:
						newLabel = 'O'
						label_base = 'O'
					else:
						if label[0] != label_base:
							label_exponent = 'B'
						else:
							label_exponent = label[1]
						label_base = label[0]
						
						newLabel = '{}-{}'.format(label_exponent, label_base)
					newLine = '{} {}'.format(' '.join(line[1:]), newLabel)
					newSent.append(newLine)

				newSents.append(newSent)

		else:
			print('CONVERSION OF {} TO {} NOT YET IMPLEMENTED YET'.format(self.format, output_format))
			sys.exit()

		self.corpus = newSents

	def add_sents(self, moreSents):

		newSents = self.corpus[:]
		for sent in moreSents:
			newSents.append(sent)

		self.corpus = newSents

	def shuffle_sents(self):

		random.shuffle(self.corpus)

	def print_out_corpus(self):

		for sent in self.corpus:
			for line in sent:
				print(line)
			print()

	def write_out_corpus(self, output_file):

		output_file = open(output_file, 'w')
		for sent in self.corpus:
			for line in sent:
				output_file.write('{}\n'.format(line))
			output_file.write('\n')

if __name__ == '__main__':

	input_file = sys.argv[1]
	input_form = sys.argv[2]
	output_form = sys.argv[3]
	output_file = sys.argv[4]

	# read in the input annotation in the input form
	annotation = converter(input_file, input_form)
	# convert to output form
	annotation.convert(output_form)
	# write out to specified output file
	annotation.write_out_corpus(output_file)




"""
python converter.py fullCorpus.seed-200.seed fullCorpus.seed-200.alwaysTrain fullCorpus.seed-200.unannotated heldOut.crf crf conll
"""
	
	# seed = sys.argv[1]
	# alwaysTrain = sys.argv[2]
	# unannotated = sys.argv[3]
	# test = sys.argv[4]
	# input_form = sys.argv[5]
	# output_form = sys.argv[6]

	# # read in the seed, active learning, and test sentences and convert formats
	# seed = converter(seed, input_form)
	# seed.convert(output_form)

	# alwaysTrain = converter(alwaysTrain, input_form)
	# alwaysTrain.convert(output_form)

	# unannotated = converter(unannotated, input_form)
	# unannotated.convert(output_form)

	# test = converter(test, input_form)
	# test.convert(output_form)

	# # combine the alwaysTrain active learning sentences with the ordered rest of corpus sentences
	# extraTrain = converter(alwaysTrain.origFileName, input_form)
	# extraTrain.convert(output_form)
	# extraTrain.add_sents(unannotated.corpus)

	# # create a randomized version of this combined, post seed training data
	# extraTrain_random = converter(alwaysTrain.origFileName, input_form)
	# extraTrain_random.convert(output_form)
	# extraTrain_random.add_sents(unannotated.corpus)
	# extraTrain_random.shuffle_sents()

	# # write out the random training set of seed followed by randomly ordered alwaysTrain 
	# train_rand = converter(seed.origFileName, input_form)
	# train_rand.convert(output_form)
	# train_rand.add_sents(extraTrain_random.corpus)
	# train_rand.write_out_corpus('eng.train.rand')

	# # write out the random dev set as an inclusive evaluation set
	# train_rand.write_out_corpus('eng.testa.rand')

	# # write out the random test set
	# test.write_out_corpus('eng.testb.rand')

	# # write out wtf this is
	# seed.write_out_corpus('eng.train54019.rand')

	# # write out the ptdl training set of seed followed by extraTrain
	# train_ptdl = converter(seed.origFileName, input_form)
	# train_ptdl.convert(output_form)
	# train_ptdl.add_sents(extraTrain.corpus)
	# train_ptdl.write_out_corpus('eng.train.ptdl')

	# # write out the ptdl dev set as an inclusive evaluation set
	# train_ptdl.write_out_corpus('eng.testa.ptdl')

	# # write out the ptdl test set
	# test.write_out_corpus('eng.testb.ptdl')

	# # write out wtf this is
	# seed.write_out_corpus('eng.train54019.ptdl')

