import sys
import fileinput

bareFile = sys.argv[1]
featFile = sys.argv[2]

bare_sents = {}
feat_sents = {}

sent_words = []
sent_feats = []
for line in fileinput.input(featFile):

	line = line.split()
	if len(line) == 0:
		sent = ' '.join(sent_words)
		feat_sents[sent] = sent_feats
		sent_words = []
		sent_feats = []
	else:
		sent_words.append(line[1])
		if len(line) > 2:
			sent_feats.append('\t'.join(line[2:]))
fileinput.close()
if len(sent_words) > 0:
	sent = ' '.join(sent_words)
	feat_sents[sent] = sent_feats



sent = []
lines = []
for line in fileinput.input(bareFile):
	line = line.split()
	if len(line) > 0:
		sent.append(line[1])
		lines.append('\t'.join(line))
	else:
		sent = ' '.join(sent)
		sent_feats = feat_sents[sent]
		for i in range(len(lines)):
			print('{}\t{}'.format(lines[i],sent_feats[i]))
		print()
		sent = []
		lines = []
fileinput.close()
if len(sent) > 0:
	sent = ' '.join(sent)
	sent_feats = feat_sents[sent]
	for i in range(len(lines)):
		print('{}\t{}'.format(lines[i],sent_feats[i]))
	print()
