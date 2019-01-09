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

def glample_lat_eval(Results, trainingData, name_of_project, train, test, trainChars, multiple_tests):

	if multiple_tests != None and multiple_tests != 'None': # re-run evaluations over each test set
		for ts in multiple_tests.split('__'):

			fname = ts.split('/')[-1]
			ts_g = ts+'.glample'
			ts_g_p = ts_g+'.pred'

			# change from crf format to glample/conll format
			trainChars = prepare_for_glample(ts, ts_g, trainChars)

			# tag unannotated data -> crf format -> desired location
			os.system('sh Scripts/tag_glample.sh '+name_of_project+' '+ts_g+' '+ts_g_p)

			F, prec, rec, total = custom_list_eval_exclusive(ts, ts_g_p)
			Results[trainingData][fname+'_Glample_list-eval-ex'] = [F, prec, rec, total]
			F, prec, rec, total = custom_eval_exclusive(ts, ts_g_p)
			Results[trainingData][fname+'_Glample_eval-ex'] = [F, prec, rec, total]
			biased_F, total = custom_eval_biased_recall_exclusive(ts, ts_g_p)
			Results[trainingData][fname+'_Glample_biasedF-ex'] = biased_F

	return Results

def glample_eval(seed_size, name_of_project, preTrained, Results, trainingData, train, test, n_epochs, multiple_tests):

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

	### HELDOUT DEV - comment out these three lines to not use a heldOut dev set
	os.system('cat '+trainSet+' '+devSet+' > '+trainSet+'.2')
	os.system('mv '+trainSet+'.2 '+trainSet)
	trainChars = prepare_for_glample('../Data/Original/heldOut.dev.crf', devSet, trainChars)
	###

	trainChars = prepare_for_glample('Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated', testSet, trainChars)

	os.system('sh Scripts/train_glample.sh '+name_of_project+' '+trainSet+' '+devSet+' '+devSet+' '+preTrained+' '+n_epochs)

	trainedProperly = True
	try:
		assert os.path.isfile('../tagger/models/'+name_of_project+'/green_flag.txt')
	except AssertionError:
		print()
		print('NOT ENOUGH DATA FOR GLAMPLE MODEL')
		print(trainingData)
		print('SKIPPING NEURAL TRAINING AND EVALUATION THIS ROUND')
		print()
		trainedProperly = False

	if trainedProperly:
		# tag the unannotated data, convert to .crf, send to desired location
		os.system('sh Scripts/tag_glample.sh '+name_of_project+' '+testSet+' '+gPred)

		# evaluate
		F, prec, rec, total = custom_list_eval_inclusive(train, test, gPred)
		Results[trainingData]['Glample_list-eval-in'] = [F, prec, rec, total]
		F, prec, rec, total = custom_eval_inclusive(train, test, gPred)
		Results[trainingData]['Glample_eval-in'] = [F, prec, rec, total]
		biased_F = custom_eval_biased_recall_inclusive(train, test, gPred)
		Results[trainingData]['Glample_biasedF'] = biased_F

		if multiple_tests != None and multiple_tests != 'None': # re-run evaluations over each test set

			Results = glample_lat_eval(Results, trainingData, name_of_project, train, test, trainChars, multiple_tests)

	else:

		Results[trainingData]['Glample_list-eval-in'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_eval-in'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_biasedF'] = 0

		Results[trainingData]['Glample_list-eval-ex'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_eval-ex'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_biasedF-ex'] = 0

		if multiple_tests != None and multiple_tests != 'None': # re-run evaluations over each test set
			for ts in multiple_tests.split('__'):
				fname = ts.split('/')[-1]
				Results[trainingData][fname+'_Glample_list-eval-in'] = [0, 0, 0, 0]
				Results[trainingData][fname+'_Glample_eval-in'] = [0, 0, 0, 0]
				Results[trainingData][fname+'_Glample_biasedF'] = 0

				Results[trainingData][fname+'_Glample_list-eval-ex'] = [0, 0, 0, 0]
				Results[trainingData][fname+'_Glample_eval-ex'] = [0, 0, 0, 0]
				Results[trainingData][fname+'_Glample_biasedF-ex'] = 0

	return Results

def record_results(train, test, predictions, Results, seed_size, go, name_of_project, preTrained, trainingData, n_epochs, multiple_tests):

	for fn in [train,test,predictions]:
		os.system("sed '/./,$!d' "+fn+" > "+fn+".2")
		os.system("mv "+fn+".2 "+fn)

	F, prec, rec, total = custom_list_eval_inclusive(train, test, predictions)
	Results[trainingData]['list-eval-in'] = [F, prec, rec, total]
	F, prec, rec, total = custom_eval_inclusive(train, test, predictions)
	Results[trainingData]['eval-in'] = [F, prec, rec, total]
	biased_F = custom_eval_biased_recall_inclusive(train, test, predictions)
	Results[trainingData]['biased_F'] = biased_F

	if multiple_tests != None and multiple_tests != 'None': # re-run evaluations over each test set
		for ts in multiple_tests.split('__'):
			fname = ts.split('/')[-1]

			### tag ts with model
			os.system('crfsuite tag -m Models/CRF/best_seed.cls '+ts+'.fts > '+ts+'.pred')

			F, prec, rec, total = custom_list_eval_exclusive(ts, ts+'.pred')
			Results[trainingData][fname+'_list-eval-ex'] = [F, prec, rec, total]
			F, prec, rec, total = custom_eval_exclusive(ts, ts+'.pred')
			Results[trainingData][fname+'_eval-ex'] = [F, prec, rec, total]
			biased_F, total = custom_eval_biased_recall_exclusive(ts, ts+'.pred')
			Results[trainingData][fname+'_biasedF-ex'] = biased_F


	### RUN GLAMPLE MODEL AND EVALUATE -> change this to always train and seed, pass go from outside function

	if go:
		Results = glample_eval(seed_size, name_of_project, preTrained, Results, trainingData, train, test, n_epochs, multiple_tests)

	else:
		Results[trainingData]['Glample_list-eval-in'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_eval-in'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_biasedF'] = 0

		Results[trainingData]['Glample_list-eval-ex'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_eval-ex'] = [0, 0, 0, 0]
		Results[trainingData]['Glample_biasedF-ex'] = 0

		if multiple_tests != None and multiple_tests != 'None': # re-run evaluations over each test set
			for ts in multiple_tests.split('__'):
				fname = ts.split('/')[-1]
				Results[trainingData][fname+'_Glample_list-eval-in'] = [0, 0, 0, 0]
				Results[trainingData][fname+'_Glample_eval-in'] = [0, 0, 0, 0]
				Results[trainingData][fname+'_Glample_biasedF'] = 0

				Results[trainingData][fname+'_Glample_list-eval-ex'] = [0, 0, 0, 0]
				Results[trainingData][fname+'_Glample_eval-ex'] = [0, 0, 0, 0]
				Results[trainingData][fname+'_Glample_biasedF-ex'] = 0

		print()
		print('NOT ENOUGH DATA FOR GLAMPLE MODEL')
		print(trainingData)
		print()

	return Results

def print_out(sort_method, trainingData, trainingDataList, Results, name_of_project, multiple_tests):

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

	###############################

	if multiple_tests != None and multiple_tests != 'None': # re-run evaluations over each test set
		for ts in multiple_tests.split('__'):
			fname = ts.split('/')[-1]
				
			# context eval test
			printline = "{}_CONTEXT_EVAL_EXCLUSIVE".format(fname)
			for x in trainingDataList:
				printline += '\t'
				printline += str(x)
			print(printline)
			# shallow results
			printline = sort_method
			for x in trainingDataList:
				printline += '\t'
				l = Results[x][fname+'_eval-ex']
				printline += '{} ({}, {})'.format(str(round(100*l[0],2)), str(round(100*l[1],2)), str(round(100*l[2],2)))
			print(printline)
			# neural inference results
			printline = '{}_neural'.format(sort_method)
			for x in trainingDataList:
				printline += '\t'
				l = Results[x][fname+'_Glample_eval-ex']
				printline += '{} ({}, {})'.format(str(round(100*l[0],2)), str(round(100*l[1],2)), str(round(100*l[2],2)))
			print(printline)
			print('\n')


			# context eval test
			printline = "{}_LIST_EVAL_EXCLUSIVE".format(fname)
			for x in trainingDataList:
				printline += '\t'
				printline += str(x)
			print(printline)
			# shallow results
			printline = sort_method
			for x in trainingDataList:
				printline += '\t'
				l = Results[x][fname+'_list-eval-ex']
				printline += '{} ({}, {})'.format(str(round(100*l[0],2)), str(round(100*l[1],2)), str(round(100*l[2],2)))
			print(printline)
			# neural inference results
			printline = '{}_neural'.format(sort_method)
			for x in trainingDataList:
				printline += '\t'
				l = Results[x][fname+'_Glample_list-eval-ex']
				printline += '{} ({}, {})'.format(str(round(100*l[0],2)), str(round(100*l[1],2)), str(round(100*l[2],2)))
			print(printline)
			print('\n')







#############################

name_of_project = sys.argv[1]
seed_size = sys.argv[2]
sort_method = sys.argv[3]
processing_script = sys.argv[4]
lg = sys.argv[5]
entities = sys.argv[6]
multiple_tests = sys.argv[7]
add_lines = sys.argv[8:]
glampleSwitch = True
if add_lines[-1] == 'no_glample':
	add_lines = add_lines[0:-1]
	glampleSwitch = False

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
elif 'German' in name_of_project:
	preTrained = "../../Embeddings/preTrained.de.vec"
elif 'French' in name_of_project:
	preTrained = "../../Embeddings/preTrained.fr.vec"
elif 'English' in name_of_project:
	preTrained = "../../Embeddings/preTrained.en.vec"
elif 'Spanish' in name_of_project:
	preTrained = "../../Embeddings/preTrained.es.vec"

### RUN THE DATA THROUGH GETTING THE RANDOM SEED
os.system('sh ../Scripts/oracle_1-4_glample.sh '+name_of_project+' '+seed_size+' '+sort_method+' '+processing_script+' '+lg+' '+entities+' '+multiple_tests)

### RECORD ACCURACY AFTER GETTING RANDOM SEED
train = 'Data/Splits/fullCorpus.seed-'+seed_size+'.seed.fts'
test = 'Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.fts'
predictions = 'Data/Splits/predictions_from_seed.txt'

Results = record_results(train, test, predictions, Results, seed_size, False, name_of_project, preTrained, trainingData, "5", multiple_tests)

### RUN THE DATA THROUGH CHECKS AND RERANK
for lines_annotated in add_lines:	
	os.system('sh ../Scripts/oracle_glample_5-7.sh '+seed_size+' '+sort_method+' '+lines_annotated+' '+entities+' '+multiple_tests)
	trainingData += ' & '+lines_annotated
	Results[trainingData] = {}
	trainingDataList.append(trainingData)
	Results = record_results(train, test, predictions, Results, seed_size, glampleSwitch, name_of_project, preTrained, trainingData, "5", multiple_tests)

# ### RUN THE DATA THROUGH ONE FINAL SET OF ANNOTATIONS
# os.system('sh Scripts/update_crossValidate_tag_get_final_results.sh '+add_lines[-1]+' Models/RankedSents/fullCorpus.seed-'+seed_size+'.'+sort_method+' Data/Splits/fullCorpus.seed-'+seed_size+'.alwaysTrain Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated Data/Splits/fullCorpus.seed-'+seed_size+'.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt crf')
# os.system('crfsuite tag -m Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.fts > Data/Splits/predictions_from_seed.txt')
# trainingData += ' & '+add_lines[-1]
# Results[trainingData] = {}
# trainingDataList.append(trainingData)
# Results = record_results(train, test, predictions, Results, seed_size, True, name_of_project, preTrained, trainingData, "5")


############################################################################

print_out(sort_method, trainingData, trainingDataList, Results, name_of_project, multiple_tests)


