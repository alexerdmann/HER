import sys
import fileinput

output = open(sys.argv[2],'w')

for line in fileinput.input(sys.argv[1]):
	line = line.split()
	if len(line) == 0:
		output.write('\n')
	else:
		if '#' != line[0]:		
			label = line[2].split('-')
			if len(label) == 1:
				label = '0'
			else:
				label = '{}-{}'.format(label[1],label[0])
			output.write('{}\t{}\n'.format(label,line[1]))
fileinput.close()
