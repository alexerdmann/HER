import sys
import fileinput

output = open(sys.argv[2],'w')

for line in fileinput.input(sys.argv[1]):
	if "-DOCSTART-" not in line:
		line = line.split()
		if len(line) == 0:
			output.write('\n')
		else:
			label = line[-1].split('-')
			if len(label) == 1:
				label = '0'
			else:
				label = '{}-{}'.format(label[1],label[0])
			output.write('{}\t{}\n'.format(label,line[0]))
fileinput.close()
