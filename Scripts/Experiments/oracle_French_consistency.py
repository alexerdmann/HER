import sys
import os
from customEval import *
import statistics

def record_results(train, test, predictions, Results):
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
	return Results

""" Run the README.sh script but calculate accuracy on full corpus at each step (requires oracle knowledge) """
""" Script must be run from the project directory """

name_of_project = sys.argv[1]
seed_size = sys.argv[2]
sort_method = sys.argv[3]
processing_script = sys.argv[4]
lg = sys.argv[5]
entities = sys.argv[6]
add_lines = sys.argv[7:]



List_results = {}
Context_results = {}
for q in range(100):

	trainingDataList = []
	Results = {}
	trainingData = 'seed-'+seed_size
	Results[trainingData] = {}
	trainingDataList.append(trainingData)
	if q == 0:
		List_results[trainingData] = []
		Context_results[trainingData] = []

	### RUN THE DATA THROUGH GETTING THE RANDOM SEED
	os.system('sh ../Scripts/oracle_1-4.sh '+name_of_project+' '+seed_size+' '+sort_method+' '+processing_script+' '+lg+' '+entities)

	### RECORD ACCURACY AFTER GETTING RANDOM SEED
	train = 'Data/Splits/fullCorpus.seed-'+seed_size+'.seed.fts'
	test = 'Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.fts'
	predictions = 'Data/Splits/predictions_from_seed.txt'
	Results = record_results(train, test, predictions, Results)

	### RUN THE DATA THROUGH CHECKS AND RERANK
	for lines_annotated in add_lines[0:-1]:
		os.system('sh ../Scripts/oracle_5-7.sh '+seed_size+' '+sort_method+' '+lines_annotated+' '+entities)
		trainingData += ' & '+lines_annotated
		if q == 0:
			List_results[trainingData] = []
			Context_results[trainingData] = []
		Results[trainingData] = {}
		trainingDataList.append(trainingData)
		Results = record_results(train, test, predictions, Results)

	### RUN THE DATA THROUGH ONE FINAL SET OF ANNOTATIONS
	os.system('sh Scripts/update_crossValidate_tag_get_final_results.sh '+add_lines[-1]+' Models/RankedSents/fullCorpus.seed-'+seed_size+'.'+sort_method+' Data/Splits/fullCorpus.seed-'+seed_size+'.alwaysTrain Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated Data/Splits/fullCorpus.seed-'+seed_size+'.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt crf')
	os.system('crfsuite tag -m Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.fts > Data/Splits/predictions_from_seed.txt')
	trainingData += ' & '+add_lines[-1]
	if q == 0:
		List_results[trainingData] = []
		Context_results[trainingData] = []
	Results[trainingData] = {}
	trainingDataList.append(trainingData)
	Results = record_results(train, test, predictions, Results)

	### PRINT OUT ALL THE RECORDED ACCURACIES AT EACH STEP WITH EACH METRIC
	print(sort_method.upper()+'\nAMOUNT OF TRAINING DATA\nRECALL-BIASED-F\nlist-F\tP,R\t\ttext-F\tP,R\n')
	for trainingData in trainingDataList:
		print('{}'.format(trainingData))
		print('{}'.format(str(round(100*Results[trainingData]['biased_F'],2))))
		printline = '\t'
		for evaluation in ['list-eval-in','eval-in']:

			l = Results[trainingData][evaluation]
			F = l[0]
			p = l[1]
			r = l[2]
			t = l[3]
			printline += '{}\t{}, {}'.format(str(int(round(100*F,0))),str(int(round(100*p,0))),str(int(round(100*r,0))))
			if evaluation == 'list-eval-in':
				printline += '\t\t'
				List_results[trainingData].append(F)
			else:
				Context_results[trainingData].append(F)
		print(printline)
			# print('\t{}: F (P, R) (COUNT): {}  ({}  {})  ({})'.format(evaluation, str(round(F, 2)), str(round(p, 2)), str(round(r, 2)), str(t)))

print()
print('CONTEXT-F MIN, MAX, MEAN, STDEV')
for td in Context_results:
	res = Context_results[td]
	printline = '{} train: {}\t{}\t{}\t{}'.format(str(td), str(min(res)), str(max(res)), str(sum(res)/len(res)), str(statistics.stdev(res)))
	print(printline)
print()

print('LIST-F MIN, MAX, MEAN, STDEV')
for td in List_results:
	res = List_results[td]
	printline = '{} train: {}\t{}\t{}\t{}'.format(str(td), str(min(res)), str(max(res)), str(sum(res)/len(res)), str(statistics.stdev(res)))
	print(printline)
print()

