import sys
import fileinput
import string

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


sents = unrankedSort(sys.argv[1])
file_prefix = '.'.join(sys.argv[1].split('.')[0:-1])
split_to_files = {}
for i in range(10):
	current_file_suffix = str(int(i))[-1]
	split_to_files[current_file_suffix] = open(file_prefix+'-'+current_file_suffix+'.crf','w')

for i in range(len(sents)):
	current_file_suffix = str(int(i))[-1]
	for line in sents[i]:
		split_to_files[current_file_suffix].write('{}\n'.format(line))
	split_to_files[current_file_suffix].write('\n')

for i in range(10):
	current_file_suffix = str(int(i))[-1]
	split_to_files[current_file_suffix].close()

# i = -1
# for line in fileinput.input(sys.argv[1]):
# 	i += 1

	#######
	# line = line.split()
	# word = line[0]
	# label = line[1]
	# if label == 'O':
	# 	label = '0'
	# else:
	# 	label = label.split('-')
	# 	label = label[1]+'-'+label[0]

	# print('{}\t{}'.format(label,word))

	# if word in ['.','?',':',';']:
	# 	print()
	#######


	#######
	# go = True
	# for c in string.punctuation:
	# 	if c in line:
	# 		go = False
	# 		break
	# if go:
	# 	print(' '.join(line.split()))
	#######

# fileinput.close()