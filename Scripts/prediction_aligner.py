import sys
import fileinput

preds = []
words = []

predFile = sys.argv[1]
wordFile = sys.argv[2]

for line in fileinput.input(predFile):
	line = line.split()
	if len(line) > 0:
		preds.append(line[0])
	else:
		preds.append(None)
fileinput.close()

for line in fileinput.input(wordFile):
	line = line.split()
	if len(line) > 0:
		words.append(line[1])
	else:
		words.append(None)
fileinput.close()

for i in range(len(preds)):
	if preds[i] == None:
		assert words[i] == None
		print()
	else:
		print('{}\t{}'.format(preds[i],words[i]))
