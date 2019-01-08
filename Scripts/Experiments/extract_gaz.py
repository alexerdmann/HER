import sys
import fileinput

PRSout = open(sys.argv[1], 'w')
GEOout = open(sys.argv[2], 'w')

PRSs = {}
GEOs = {}

for line in sys.stdin:
	GEOline = line.split('<placeName')
	if len(GEOline) > 1:
		for GEOlin in GEOline[1:]:
			GEOli = GEOlin.split('</placeName>')[0]
			GEO = GEOli.split('>')[-1]
			GEOs[GEO] = True

	PRSline = line.split('<persName')
	if len(PRSline) > 1:
		for PRSlin in PRSline[1:]:
			PRSli = PRSlin.split('</persName>')[0]
			PRS = PRSli.split('>')[-1]
			PRSs[PRS] = True

for x in PRSs:
	PRSout.write('{}\n'.format(x))

for x in GEOs:
	GEOout.write('{}\n'.format(x))

PRSout.close()
GEOout.close()