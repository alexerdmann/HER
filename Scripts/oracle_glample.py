import sys
import os
import time
from customEval import *

def prepare_for_glample(fileIn, fileOut, trainChars):

	origIn = fileIn
	if 'alwaysTrain' in origIn:
		trainChars = {}

	fileOut = open(fileOut,'w')
	
	for tl in fileinput.input(fileIn):

		line = tl.split()

		if len(line) == 0:

			fileOut.write('\n')

		else:

			label = line[0]
			line = line[1:]
			if label == '0':
				label = 'O'
			else:
				label = label.split('-')
				label = '{}-{}'.format(label[-1],label[0])
			line.append(label)

			wrd = line[0]
			newWrd = ''
			
			for l in wrd:
				if 'alwaysTrain' in origIn:
					trainChars[l] = True
					newWrd += l
				else:
					if l in trainChars:
						newWrd += l

			if len(newWrd) == 0:
				newWrd = 'UNICODE-ERROR'

			line[0] = newWrd

			line = '\t'.join(line)

			fileOut.write('{}\n'.format(line))

	fileinput.close()
	fileOut.close()

	return trainChars

def glample_lat_eval(Results, trainingData, name_of_project, train, test, trainChars):

	testGWcrf = 'Data/Prepared/GW.test.crf'
	testOvidCrf = 'Data/Prepared/Ovid.test.crf'
	testPlinyCrf = 'Data/Prepared/Pliny.test.crf'

	testGW = '../tagger/dataset/GW.test'
	testOvid = '../tagger/dataset/Ovid.test'
	testPliny = '../tagger/dataset/Pliny.test'

	predGW = 'Data/Splits/GW.test.gPred'
	predOvid = 'Data/Splits/Ovid.test.gPred'
	predPliny = 'Data/Splits/Pliny.test.gPred'

	# change from crf format to glample/conll format
	trainChars = prepare_for_glample(testGWcrf, testGW, trainChars)
	trainChars = prepare_for_glample(testOvidCrf, testOvid, trainChars)
	trainChars = prepare_for_glample(testPlinyCrf, testPliny, trainChars)

	# tag unannotated data -> crf format -> desired location
	os.system('sh Scripts/tag_glample.sh '+name_of_project+' '+testGW+' '+predGW)
	# evaluate
	F, prec, rec, total = custom_list_eval_inclusive(train, testGWcrf, predGW)
	Results[trainingData]['Glample_GW_list-eval-in'] = [F, prec, rec, total]
	F, prec, rec, total = custom_eval_inclusive(train, testGWcrf, predGW)
	Results[trainingData]['Glample_GW_eval-in'] = [F, prec, rec, total]
	biased_F = custom_eval_biased_recall_inclusive(train, testGWcrf, predGW)
	Results[trainingData]['Glample_GW_biasedF'] = biased_F


	# tag unannotated data -> crf format -> desired location
	os.system('sh Scripts/tag_glample.sh '+name_of_project+' '+testOvid+' '+predOvid)
	# evaluate
	F, prec, rec, total = custom_list_eval_inclusive(train, testOvidCrf, predOvid)
	Results[trainingData]['Glample_Ovid_list-eval-in'] = [F, prec, rec, total]
	F, prec, rec, total = custom_eval_inclusive(train, testOvidCrf, predOvid)
	Results[trainingData]['Glample_Ovid_eval-in'] = [F, prec, rec, total]
	biased_F = custom_eval_biased_recall_inclusive(train, testOvidCrf, predOvid)
	Results[trainingData]['Glample_Ovid_biasedF'] = biased_F


	# tag unannotated data -> crf format -> desired location
	os.system('sh Scripts/tag_glample.sh '+name_of_project+' '+testPliny+' '+predPliny)
	# evaluate
	F, prec, rec, total = custom_list_eval_inclusive(train, testPlinyCrf, predPliny)
	Results[trainingData]['Glample_Pliny_list-eval-in'] = [F, prec, rec, total]
	F, prec, rec, total = custom_eval_inclusive(train, testPlinyCrf, predPliny)
	Results[trainingData]['Glample_Pliny_eval-in'] = [F, prec, rec, total]
	biased_F = custom_eval_biased_recall_inclusive(train, testPlinyCrf, predPliny)
	Results[trainingData]['Glample_Pliny_biasedF'] = biased_F

	return Results

def glample_eval(seed_size, name_of_project, preTrained, Results, trainingData, train, test, n_epochs):

	trainSet = '../tagger/dataset/'+name_of_project+'.train'
	devSet = '../tagger/dataset/'+name_of_project+'.dev'
	testSet = '../tagger/dataset/'+name_of_project+'.test'
	gPred = 'Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.gPred'

	trainChars = {}

	for fn in ['Data/Splits/fullCorpus.seed-'+seed_size+'.alwaysTrain', 'Data/Splits/fullCorpus.seed-'+seed_size+'.seed', 'Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated']:
		os.system("sed '/./,$!d' "+fn+" > "+fn+".2")
		os.system("mv "+fn+".2 "+fn)

	# change from crf format to glample/conll format
	trainChars = prepare_for_glample('Data/Splits/fullCorpus.seed-'+seed_size+'.alwaysTrain', trainSet, trainChars)
	trainChars = prepare_for_glample('Data/Splits/fullCorpus.seed-'+seed_size+'.seed', devSet, trainChars)
	trainChars = prepare_for_glample('Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated', testSet, trainChars)

	# train but don't let it do inference on the test set yet
	os.system('sh Scripts/train_glample.sh '+name_of_project+' '+trainSet+' '+devSet+' '+devSet+' '+preTrained+' '+n_epochs)

	# tag the unannotated data, convert to .crf, send to desired location
	os.system('sh Scripts/tag_glample.sh '+name_of_project+' '+testSet+' '+gPred)

	# evaluate
	F, prec, rec, total = custom_list_eval_inclusive(train, test, gPred)
	Results[trainingData]['Glample_list-eval-in'] = [F, prec, rec, total]
	F, prec, rec, total = custom_eval_inclusive(train, test, gPred)
	Results[trainingData]['Glample_eval-in'] = [F, prec, rec, total]
	biased_F = custom_eval_biased_recall_inclusive(train, test, gPred)
	Results[trainingData]['Glample_biasedF'] = biased_F

	if 'Latin' in name_of_project: # re-run evaluations over each test set

		Results = glample_lat_eval(Results, trainingData, name_of_project, train, test, trainChars)

	return Results

def record_results(train, test, predictions, Results, seed_size, go, name_of_project, preTrained, trainingData, n_epochs):

	for fn in [train,test,predictions]:
		os.system("sed '/./,$!d' "+fn+" > "+fn+".2")
		os.system("mv "+fn+".2 "+fn)

	F, prec, rec, total = custom_list_eval_inclusive(train, test, predictions)
	Results[trainingData]['list-eval-in'] = [F, prec, rec, total]
	# F, prec, rec, total = custom_list_eval_exclusive(test, predictions)
	# Results[trainingData]['list-eval-ex'] = [F, prec, rec, total]
	F, prec, rec, total = custom_eval_inclusive(train, test, predictions)
	Results[trainingData]['eval-in'] = [F, prec, rec, total]
	# F, prec, rec, total = custom_eval_exclusive(test, predictions)
	# Results[trainingData]['eval-out'] = [F, prec, rec, total]
	biased_F = custom_eval_biased_recall_inclusive(train, test, predictions)
	Results[trainingData]['biased_F'] = biased_F


	### RUN GLAMPLE MODEL AND EVALUATE -> change this to always train and seed, pass go from outside function

	try:

		if go:
			Results = glample_eval(seed_size, name_of_project, preTrained, Results, trainingData, train, test, n_epochs)

		else:
			Results[trainingData]['Glample_list-eval-in'] = [0, 0, 0, 0]
			Results[trainingData]['Glample_eval-in'] = [0, 0, 0, 0]
			Results[trainingData]['Glample_biasedF'] = 0

			if 'Latin' in name_of_project: # re-run evaluations over each test set
				Results[trainingData]['Glample_GW_list-eval-in'] = [0, 0, 0, 0]
				Results[trainingData]['Glample_GW_eval-in'] = [0, 0, 0, 0]
				Results[trainingData]['Glample_GW_biasedF'] = 0

				Results[trainingData]['Glample_Ovid_list-eval-in'] = [0, 0, 0, 0]
				Results[trainingData]['Glample_Ovid_eval-in'] = [0, 0, 0, 0]
				Results[trainingData]['Glample_Ovid_biasedF'] = 0

				Results[trainingData]['Glample_Pliny_list-eval-in'] = [0, 0, 0, 0]
				Results[trainingData]['Glample_Pliny_eval-in'] = [0, 0, 0, 0]
				Results[trainingData]['Glample_Pliny_biasedF'] = 0

	except KeyError:

		Results[trainingData]['Glample_list-eval-in'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_eval-in'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_biasedF'] = 0

		if 'Latin' in name_of_project: # re-run evaluations over each test set
			Results[trainingData]['Glample_GW_list-eval-in'] = [0, 0, 0, 0]
			Results[trainingData]['Glample_GW_eval-in'] = [0, 0, 0, 0]
			Results[trainingData]['Glample_GW_biasedF'] = 0

			Results[trainingData]['Glample_Ovid_list-eval-in'] = [0, 0, 0, 0]
			Results[trainingData]['Glample_Ovid_eval-in'] = [0, 0, 0, 0]
			Results[trainingData]['Glample_Ovid_biasedF'] = 0

			Results[trainingData]['Glample_Pliny_list-eval-in'] = [0, 0, 0, 0]
			Results[trainingData]['Glample_Pliny_eval-in'] = [0, 0, 0, 0]
			Results[trainingData]['Glample_Pliny_biasedF'] = 0


		print()
		print('NOT ENOUGH DATA FOR GLAMPLE MODEL')
		print(trainingData)
		print()


	return Results

# def print_out(sort_method, trainingData, trainingDataList, Results, name_of_project):

# 	### PRINT OUT ALL THE RECORDED ACCURACIES AT EACH STEP WITH EACH METRIC
# 	print(sort_method.upper()+'\nAMOUNT OF TRAINING DATA\nRECALL-BIASED-F\nlist-F\tP,R\t\ttext-F\tP,R\n')
# 	for trainingData in trainingDataList:
# 		print('{}'.format(trainingData))
# 		print('{}'.format(str(round(100*Results[trainingData]['biased_F'],2))))
# 		printline = '\t'
# 		for evaluation in ['list-eval-in','eval-in']:

# 			l = Results[trainingData][evaluation]
# 			F = l[0]
# 			p = l[1]
# 			r = l[2]
# 			t = l[3]
# 			printline += '{}\t{}, {}'.format(str(int(round(100*F,0))),str(int(round(100*p,0))),str(int(round(100*r,0))))
# 			if evaluation == 'list-eval-in':
# 				printline += '\t\t'
# 		print(printline)
# 			# print('\t{}: F (P, R) (COUNT): {}  ({}  {})  ({})'.format(evaluation, str(round(F, 2)), str(round(p, 2)), str(round(r, 2)), str(t)))

# 	### PRINT OUT ALL THE RECORDED ACCURACIES AT EACH STEP WITH GLAMPLE MODEL
# 	print('___________________________________________\n'+sort_method.upper()+' -- GLAMPLE\nAMOUNT OF TRAINING DATA\nGLAMPLE RECALL-BIASED-F\nlist-F\tP,R\t\ttext-F\tP,R\n(GW, OVID, PLINY)\n')
# 	for trainingData in trainingDataList:

# 		### RECORDING BIASED F SCORES
# 		print('{}'.format(trainingData))
# 		print('{}'.format(str(round(100*Results[trainingData]['Glample_biasedF'],2))))
# 		if 'Latin' in name_of_project:
# 			print('{}'.format(str(round(100*Results[trainingData]['Glample_GW_biasedF'],2))))
# 			print('{}'.format(str(round(100*Results[trainingData]['Glample_Ovid_biasedF'],2))))
# 			print('{}'.format(str(round(100*Results[trainingData]['Glample_Pliny_biasedF'],2))))
# 		printline = '\t'

# 		if 'Latin' in name_of_project:
# 			evalList = ['Glample_list-eval-in','Glample_eval-in','Glample_GW_list-eval-in','Glample_GW_eval-in','Glample_Ovid_list-eval-in','Glample_Ovid_eval-in','Glample_Pliny_list-eval-in','Glample_Pliny_eval-in']
# 		else:
# 			evalList = ['Glample_list-eval-in','Glample_eval-in']

# 		for evaluation in evalList:

# 			l = Results[trainingData][evaluation]
# 			F = l[0]
# 			p = l[1]
# 			r = l[2]
# 			t = l[3]
# 			printline += '{}\t{}, {}'.format(str(int(round(100*F,0))),str(int(round(100*p,0))),str(int(round(100*r,0))))
# 			if evaluation in ['Glample_list-eval-in','Glample_GW_list-eval-in','Glample_Ovid_list-eval-in','Glample_Pliny_list-eval-in']:
# 				printline += '\t\t'
# 		print(printline)
# 			# print('\t{}: F (P, R) (COUNT): {}  ({}  {})  ({})'.format(evaluation, str(round(F, 2)), str(round(p, 2)), str(round(r, 2)), str(t)))

def print_out(sort_method, trainingData, trainingDataList, Results, name_of_project):

	### PRINT OUT ALL THE RECORDED ACCURACIES AT EACH STEP WITH EACH METRIC

	# context eval inclusive
	printline = "CONTEXT_EVAL_INCLUSIVE"
	for x in trainingDataList:
		printline += '\t'
		printline += str(x)
	print(printline)
	# shallow results
	printline = sort_method
	for x in trainingDataList:
		printline += '\t'
		l = Results[x]['eval-in']
		printline += '{} ({}, {})'.format(str(round(100*l[0],2)), str(round(100*l[1],2)), str(round(100*l[2],2)))
	print(printline)
	# neural inference results
	printline = '{}_neural'.format(sort_method)
	for x in trainingDataList:
		printline += '\t'
		l = Results[x]['Glample_eval-in']
		printline += '{} ({}, {})'.format(str(round(100*l[0],2)), str(round(100*l[1],2)), str(round(100*l[2],2)))
	print(printline)
	print('\n')


	# list eval inclusive
	printline = "LIST_EVAL_INCLUSIVE"
	for x in trainingDataList:
		printline += '\t'
		printline += str(x)
	print(printline)
	# shallow results
	printline = sort_method
	for x in trainingDataList:
		printline += '\t'
		l = Results[x]['list-eval-in']
		printline += '{} ({}, {})'.format(str(round(100*l[0],2)), str(round(100*l[1],2)), str(round(100*l[2],2)))
	print(printline)
	# neural inference results
	printline = '{}_neural'.format(sort_method)
	for x in trainingDataList:
		printline += '\t'
		l = Results[x]['Glample_list-eval-in']
		printline += '{} ({}, {})'.format(str(round(100*l[0],2)), str(round(100*l[1],2)), str(round(100*l[2],2)))
	print(printline)
	print('\n')



	# context eval test
	printline = "CONTEXT_EVAL_TEST"
	for x in trainingDataList:
		printline += '\t'
		printline += str(x)
	print(printline)
	# neural inference results
	printline = '{}_neural'.format(sort_method)
	for x in trainingDataList:
		printline += '\t'
		l = Results[x]
		printline += '{}, {}, {}'.format(str(round(100*l['Glample_GW_eval-in'][0],2)), str(round(100*l['Glample_Pliny_eval-in'][0],2)), str(round(100*l['Glample_Ovid_eval-in'][0],2)))
	print(printline)
	print('\n')

	# list eval test
	printline = "LIST_EVAL_TEST"
	for x in trainingDataList:
		printline += '\t'
		printline += str(x)
	print(printline)
	# neural inference results
	printline = '{}_neural'.format(sort_method)
	for x in trainingDataList:
		printline += '\t'
		l = Results[x]
		printline += '{}, {}, {}'.format(str(round(100*l['Glample_GW_list-eval-in'][0],2)), str(round(100*l['Glample_Pliny_list-eval-in'][0],2)), str(round(100*l['Glample_Ovid_list-eval-in'][0],2)))
	print(printline)
	print('\n')









#############################

name_of_project = sys.argv[1]
seed_size = sys.argv[2]
sort_method = sys.argv[3]
processing_script = sys.argv[4]
lg = sys.argv[5]
entities = sys.argv[6]
add_lines = sys.argv[7:]

trainingDataList = []
Results = {}
trainingData = 'seed-'+seed_size
Results[trainingData] = {}
trainingDataList.append(trainingData)

# locate preTrained embeddings and gunzip
preTrained = '""'
if 'Latin' in name_of_project:
	preTrained = "../../Embeddings/preTrained.lat.vec"
elif 'Greek' in name_of_project:
	preTrained = "../../Embeddings/preTrained.grk.vec"
elif 'medFrench' in name_of_project:
	preTrained = "../../Embeddings/preTrained.mf.vec"
elif 'GermEval' in name_of_project:
	preTrained = "../../Embeddings/preTrained.de.vec"
elif 'French' in name_of_project:
	preTrained = "../../Embeddings/preTrained.fr.vec"
elif 'English' in name_of_project:
	preTrained = "../../Embeddings/preTrained.en.vec"

if preTrained != '""':
	os.system('gunzip '+preTrained+'.gz')

### RUN THE DATA THROUGH GETTING THE RANDOM SEED
os.system('sh ../Scripts/oracle_1-4.sh '+name_of_project+' '+seed_size+' '+sort_method+' '+processing_script+' '+lg+' '+entities)

### RECORD ACCURACY AFTER GETTING RANDOM SEED
train = 'Data/Splits/fullCorpus.seed-'+seed_size+'.seed.fts'
test = 'Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.fts'
predictions = 'Data/Splits/predictions_from_seed.txt'

Results = record_results(train, test, predictions, Results, seed_size, False, name_of_project, preTrained, trainingData, "5")

### RUN THE DATA THROUGH CHECKS AND RERANK
for lines_annotated in add_lines:	
	os.system('sh ../Scripts/oracle_5-7.sh '+seed_size+' '+sort_method+' '+lines_annotated+' '+entities)
	trainingData += ' & '+lines_annotated
	Results[trainingData] = {}
	trainingDataList.append(trainingData)
	Results = record_results(train, test, predictions, Results, seed_size, True, name_of_project, preTrained, trainingData, "5")

# ### RUN THE DATA THROUGH ONE FINAL SET OF ANNOTATIONS
# os.system('sh Scripts/update_crossValidate_tag_get_final_results.sh '+add_lines[-1]+' Models/RankedSents/fullCorpus.seed-'+seed_size+'.'+sort_method+' Data/Splits/fullCorpus.seed-'+seed_size+'.alwaysTrain Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated Data/Splits/fullCorpus.seed-'+seed_size+'.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt')
# os.system('crfsuite tag -m Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.fts > Data/Splits/predictions_from_seed.txt')
# trainingData += ' & '+add_lines[-1]
# Results[trainingData] = {}
# trainingDataList.append(trainingData)
# Results = record_results(train, test, predictions, Results, seed_size, True, name_of_project, preTrained, trainingData, "5")


############################################################################

print_out(sort_method, trainingData, trainingDataList, Results, name_of_project)

if preTrained != '""':
	os.system('gzip '+preTrained)


