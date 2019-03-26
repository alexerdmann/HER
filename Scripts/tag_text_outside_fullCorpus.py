from sys import argv, exit
import os



model = argv[1] # by default, crf model is Models/CRF/best_seed.cls; bilstm-crf is ../tagger/models/MyModel/
test = argv[2]
lg = argv[3]
architecture = argv[4]
if architecture == 'crf':
    fullCorpus = argv[5]
    featSet_file = argv[6]



### PREPROCESS NEW FILE
prepared_test = os.path.join('Data/External', os.path.basename(test))
os.system('mkdir Data/External')
if len(test) > 4 and '.crf' == test[-4:]:
    os.system('cp {} {}'.format(test, prepared_test))
else:
    os.system('python Scripts/preprocess.py {} > {}.1'.format(test, prepared_test))
    os.system('perl Scripts/Moses_Tokenizer/tokenizer/tokenizer.perl -l {} < {}.1 > {}.2'.format(lg, prepared_test, prepared_test))
    os.system('python Scripts/prepare4crf.py {}.2 > {}'.format(prepared_test, prepared_test))
    os.system('rm {}.*'.format(prepared_test))

### TAG WITH CRF TAGGER
if architecture == 'crf':

    ### get features
    for line in open(featSet_file):
        featList = line.strip().replace('_', ' ')
    os.system('python Scripts/addFeatures.py -corpus {} -fullCorpus {} -hist {}.hist -features {} -gazatteers Data/Gazatteers/* > {}.fts'.format(prepared_test, fullCorpus, fullCorpus, featList, prepared_test))
    ### tag
    os.system('crfsuite tag -m {} {}.fts > {}.pred'.format(model, prepared_test, prepared_test))

### TAG WITH BILSTM-CRF TAGGER
elif architecture == 'bilstm-crf':

    ### convert test set to conll format and tag
    os.system('sh Scripts/tag_outside_bilstm-crf_extension.sh {} {}'.format(prepared_test, model))

else:
    print('Sorry, the {} architecture is not supported yet'.format(architecture))
    exit()

### ALIGN PREDICTIONS WITH TEXT
os.system('paste {}.pred {} | cut -f 1,3 > {}.aligned'.format(prepared_test, prepared_test, prepared_test))

### GET NAMED ENTITY LIST
os.system('python Scripts/get_NE_list.py {}.aligned > {}.list'.format(prepared_test, prepared_test))
print('\n\nThe tagged text is located here: \n\t{}.aligned\n\nThe list of named entities extracted from said text is here: \n\t{}.list\n'.format(prepared_test, prepared_test))








