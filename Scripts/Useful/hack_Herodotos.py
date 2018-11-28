import sys
import fileinput

output = open(sys.argv[2],'w')

for line in fileinput.input(sys.argv[1]):
	line = line.split()
	if len(line) == 0:
		output.write('\n')
	else:
		label = line[0]
		if label != '0':
			if label[-1] == 'U':
				label = '{}-{}'.format(label[0:-1],'B')
			elif label[-1] == 'F':
				label = '{}-{}'.format(label[0:-1],'B')
			elif label[-1] == 'L':
				label = '{}-{}'.format(label[0:-1],'I')
			else:
				label = '{}-{}'.format(label[0:-1],'I')
		output.write('{}\t{}\n'.format(label,line[1]))
fileinput.close()
