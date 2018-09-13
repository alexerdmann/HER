import sys
import os
from customEval import *

def record_results(train, test, predictions, Results):
	F, prec, rec, total = custom_list_eval_inclusive(train, test, predictions)
	Results[trainingData]['list-eval-in'] = [F, prec, rec, total]
	F, prec, rec, total = custom_list_eval_exclusive(test, predictions)
	Results[trainingData]['list-eval-ex'] = [F, prec, rec, total]
	F, prec, rec, total = custom_eval_inclusive(train, test, predictions)
	Results[trainingData]['eval-in'] = [F, prec, rec, total]
	F, prec, rec, total = custom_eval_exclusive(test, predictions)
	Results[trainingData]['eval-out'] = [F, prec, rec, total]
	return Results

""" Run the README.sh script but calculate accuracy on full corpus at each step (requires oracle knowledge) """
""" Script must be run from the project directory """

name_of_project = sys.argv[1]
seed_size = sys.argv[2]
sort_method = sys.argv[3]
processing_script = sys.argv[4]
lg = sys.argv[5]
add_lines_1 = sys.argv[6]
add_lines_2 = sys.argv[7]

Results = {}
trainingData = 'seed-'+seed_size
Results[trainingData] = {}

### RUN THE DATA THROUGH GETTING THE RANDOM SEED
os.system('sh ../Scripts/oracle_1-4.sh '+name_of_project+' '+seed_size+' '+sort_method+' '+processing_script+' '+lg)

### RECORD ACCURACY AFTER GETTING RANDOM SEED
train = 'Data/Splits/fullCorpus.seed-'+seed_size+'.seed.fts'
test = 'Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.fts'
predictions = 'Data/Splits/predictions_from_seed.txt'
Results = record_results(train, test, predictions, Results)

### RUN THE DATA THROUGH THE FIRST CHECK AND RERANK
os.system('sh ../Scripts/oracle_5-7.sh '+seed_size+' '+sort_method+' '+add_lines_1)
trainingData += ' & '+add_lines_1
Results[trainingData] = {}
Results = record_results(train, test, predictions, Results)

### RUN THE DATA THROUGH ONE FINAL SET OF ANNOTATIONS
os.system('sh Scripts/update_crossValidate_tag_get_final_results.sh '+add_lines_2+' Models/RankedSents/fullCorpus.seed-'+seed_size+'.'+sort_method+' Data/Splits/fullCorpus.seed-'+seed_size+'.alwaysTrain Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated Data/Splits/fullCorpus.seed-'+seed_size+'.seed Data/Prepared/fullCorpus.txt Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.pred Results/fullCorpus.final.txt Results/fullCorpus.final-list.txt')
os.system('crfsuite tag -m Models/CRF/best_seed.cls Data/Splits/fullCorpus.seed-'+seed_size+'.unannotated.fts > Data/Splits/predictions_from_seed.txt')
trainingData += ' & '+add_lines_2
Results[trainingData] = {}
Results = record_results(train, test, predictions, Results)

### PRINT OUT ALL THE RECORDED ACCURACIES AT EACH STEP WITH EACH METRIC
for trainingData in Results:
	print('{}'.format(trainingData))
	printline = '\t'
	for evaluation in Results[trainingData]:
		l = Results[trainingData][evaluation]
		F = l[0]
		p = l[1]
		r = l[2]
		t = l[3]
		printline += str(int(round(100*F,0)))+','
	print(printline[0:-1])
		# print('\t{}: F (P, R) (COUNT): {}  ({}  {})  ({})'.format(evaluation, str(round(F, 2)), str(round(p, 2)), str(round(r, 2)), str(t)))
