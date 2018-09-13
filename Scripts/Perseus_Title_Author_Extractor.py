import sys
import os
import re
import fileinput

fileList = sys.argv[1:]

def ensure_unique_fileName(file, title, author, fileNames):
	fileName = '{}/{}--{}.0.xml'.format('/'.join(file.split('/')[0:-1]),author,title)
	suffix = 0
	while fileName in fileNames:
		suffix += 1
		fileName = '{}.{}.{}'.format(fileName.split('.')[0],str(suffix),fileName.split('.')[-1])
	return fileName

def ensure_well_formed(ta):
	ta = ta.replace('.','-').replace('/','-').replace(',','').replace('(','-').replace(')','-').replace("'",'').replace('"','').replace("<",'-').replace('>','-').replace('|','')
	if 'Machine_readable_text' in ta:
		ta = None
	return ta


fileNames = {}
### GO THROUGH ALL DATA FILES
for file in fileList:
	title = None
	author = None
	for line in fileinput.input(file):

		### EXTRACT TITLE AND AUTHOR FROM XML
		if title == None or author == None:
			if title == None and '<title' in line and '</title>' in line:
				if 'Machine_readable_text<-title><author' in line:
					line = line.split('Machine_readable_text<-title><author')[-1]
				try:
					title = '_'.join(re.search('>(.*)</title>', line).group(1).split())
					title = ensure_well_formed(title)
				except:
					title = None
			if author == None and '<author' in line and '</author>' in line:
				if 'Machine_readable_text<-title><author' in line:
					line = line.split('Machine_readable_text<-title><author')[-1]
				try:
					author = '_'.join(re.search('>(.*)</author>', line).group(1).split())
					author = ensure_well_formed(author)
				except:
					author = None

		### MAKE UP NEW, INFORMATIVE FILE NAME
		if title != None and author != None:
	
			### ENSURE FILENAME IS UNIQUE
			fileName = ensure_unique_fileName(file, title, author, fileNames)
			fileNames[fileName] = True
			break

	### EXCEPTION HANDLING
	if title == None or author == None:
		if title == None:
			title = 'UNK'
		if author == None:
			author = 'UNK'
		fileName = ensure_unique_fileName(file, title, author, fileNames)
		fileNames[fileName] = True

	fileinput.close()

	### MOVE FILE TO LOCATION WITH NEW NAME
	os.system('mv '+file+' '+fileName)
	# print('\n{} \n\t {}'.format(file,fileName))
