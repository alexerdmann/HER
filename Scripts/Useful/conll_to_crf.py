import sys
import fileinput

output = open(sys.argv[2],'w')

lastWasBlank = True
for line in fileinput.input(sys.argv[1]):
	line = line.split()

	if len(line) == 0:
		if lastWasBlank == False:
			output.write('\n')
		lastWasBlank = True

	else:
		lastWasBlank = False
		label = line[-1].split('-')
		if len(label) == 1:
			label = '0'
		else:
			label = '{}-{}'.format(label[1],label[0])
		output.write('{}\t{}\n'.format(label,line[0]))

output.close()
fileinput.close()
