experiment_number=$1

############### CONLL-SPANISH EVALUATION #########################

if [[ $experiment_number == "1" ]]
then
	[ -d "Spanish_preTag_delex" ] rm -rf "Spanish_preTag_delex"
	mkdir Spanish_preTag_delex
	cd Spanish_preTag_delex
	cp ../Data/Original/heldOut.crf ../Data/Original/heldOut-preTag_delex.crf
	python ../Scripts/oracle_glample.py Spanish_preTag_delex 200 preTag_delex ../Scripts/preprocess.py es LOC_MISC_ORG_PER ../Data/Original/heldOut-preTag_delex.crf 1000 4000 5000 10000 20000 20000 20000 20000 50000 50000 50000 # should go up to about 250 k.. there is about 320 total b/w train and dev, another 50 in test
	rm ../Data/Original/heldOut-preTag_delex.crf*
	cd ../
fi

#######################

if [[ $experiment_number == "2" ]]
then
	[ -d "Spanish_hardCappedUNKs" ] rm -rf "Spanish_hardCappedUNKs"
	mkdir Spanish_hardCappedUNKs
	cd Spanish_hardCappedUNKs
	cp ../Data/Original/heldOut.crf ../Data/Original/heldOut-hardCappedUNKs.crf
	python ../Scripts/oracle_glample.py Spanish_hardCappedUNKs 200 hardCappedUNKs ../Scripts/preprocess.py es LOC_MISC_ORG_PER ../Data/Original/heldOut-hardCappedUNKs.crf 1000 4000 5000 10000 20000 20000 20000 20000 50000 50000 50000 # should go up to about 250 k.. there is about 320 total b/w train and dev, another 50 in test
	rm ../Data/Original/heldOut-hardCappedUNKs.crf*
	cd ../
fi

#######################

if [[ $experiment_number == "3" ]]
then
	[ -d "Spanish_random" ] rm -rf "Spanish_random"
	mkdir Spanish_random
	cd Spanish_random
	cp ../Data/Original/heldOut.crf ../Data/Original/heldOut-random.crf
	python ../Scripts/oracle_glample.py Spanish_random 200 random ../Scripts/preprocess.py es LOC_MISC_ORG_PER ../Data/Original/heldOut-random.crf 1000 4000 5000 10000 20000 20000 20000 20000 50000 50000 50000 # should go up to about 250 k.. there is about 320 total b/w train and dev, another 50 in test
	rm ../Data/Original/heldOut-random.crf*
	cd ../
fi



############### LATIN EVALUATION #########################

if [[ $experiment_number == "4" ]]
then
	[ -d "Latin_preTag_delex" ] rm -rf "Latin_preTag_delex"
	mkdir Latin_preTag_delex
	cd Latin_preTag_delex
	python ../Scripts/oracle_glample.py Latin_preTag_delex 200 preTag_delex ../Scripts/preprocess.py en GEO_GRP_PRS Data/Prepared/GW.test.crf__Data/Prepared/Pliny.test.crf__Data/Prepared/Ovid.test.crf 1000 4000 5000 10000 20000 
	rm ../Data/Original/heldOut-preTag_delex.crf*
	cd ../
fi

#######################

if [[ $experiment_number == "5" ]]
then
	[ -d "Latin_hardCappedUNKs" ] rm -rf "Latin_hardCappedUNKs"
	mkdir Latin_hardCappedUNKs
	cd Latin_hardCappedUNKs
	python ../Scripts/oracle_glample.py Latin_hardCappedUNKs 200 hardCappedUNKs ../Scripts/preprocess.py en GEO_GRP_PRS Data/Prepared/GW.test.crf__Data/Prepared/Pliny.test.crf__Data/Prepared/Ovid.test.crf 1000 4000 5000 10000 20000 
	rm ../Data/Original/heldOut-hardCappedUNKs.crf*
	cd ../
fi

#######################

if [[ $experiment_number == "6" ]]
then
	[ -d "Latin_random" ] rm -rf "Latin_random"
	mkdir Latin_random
	cd Latin_random
	python ../Scripts/oracle_glample.py Latin_random 200 random ../Scripts/preprocess.py en GEO_GRP_PRS Data/Prepared/GW.test.crf__Data/Prepared/Pliny.test.crf__Data/Prepared/Ovid.test.crf 1000 4000 5000 10000 20000
	rm ../Data/Original/heldOut-random.crf*
	cd ../
fi



############### FRENCH EVALUATION #########################

if [[ $experiment_number == "7" ]]
then
	[ -d "French_preTag_delex" ] rm -rf "French_preTag_delex"
	mkdir French_preTag_delex
	cd French_preTag_delex
	python ../Scripts/oracle_glample.py French_preTag_delex 200 preTag_delex ../Scripts/Useful/preprocess_Davids_data.py fr GEO None 1000 4000 5000 10000 20000 20000 20000 20000
	cd ../
fi

#######################

if [[ $experiment_number == "8" ]]
then
	[ -d "French_hardCappedUNKs" ] rm -rf "French_hardCappedUNKs"
	mkdir French_hardCappedUNKs
	cd French_hardCappedUNKs
	python ../Scripts/oracle_glample.py French_hardCappedUNKs 200 hardCappedUNKs ../Scripts/Useful/preprocess_Davids_data.py fr GEO None 1000 4000 5000 10000 20000 20000 20000 20000
	cd ../
fi

#######################

if [[ $experiment_number == "9" ]]
then
	[ -d "French_random" ] rm -rf "French_random"
	mkdir French_random
	cd French_random
	python ../Scripts/oracle_glample.py French_random 200 random ../Scripts/Useful/preprocess_Davids_data.py fr GEO None 1000 4000 5000 10000 20000 20000 20000 20000
	cd ../
fi



############### FRENCH CONSISTENCY EVALUATION #########################

if [[ $experiment_number == "10" ]]
then
	for i in `seq 1 100`
	do
		[ -d "French_con_preTag_delex" ] rm -rf "French_con_preTag_delex"
		mkdir French_con_preTag_delex
		cd French_con_preTag_delex
		python ../Scripts/oracle_glample.py French_con_preTag_delex 200 preTag_delex ../Scripts/Useful/preprocess_Davids_data.py fr GEO None 1000 4000 5000 10000 20000 20000 20000 20000
		cd ../
	done
fi

############### GERMAN EVALUATION #########################

if [[ $experiment_number == "11" ]]
then
	[ -d "German_random" ] rm -rf "German_random"
	mkdir German_random
	cd German_random
	cp ../Data/Original/heldOut.crf ../Data/Original/heldOut-random.crf
	python ../Scripts/oracle_glample.py German_random 200 random ../Scripts/preprocess.py de LOC_LOCderiv_LOCpart_OTH_OTHderiv_OTHpart_ORG_ORGderiv_ORGpart_PER_PERderiv_PERpart ../Data/Original/heldOut-random.crf 1000 4000 5000 10000 20000 20000 20000 20000 50000 50000 50000 50000 100000 100000
	rm ../Data/Original/heldOut-random.crf*
	cd ../
fi

############### CONLL-SPANISH DROPOUT EVALUATION #########################

if [[ $experiment_number == "12" ]]
then
	[ -d "Spanish_dropout25_preTag_delex" ] rm -rf "Spanish_dropout25_preTag_delex"
	mkdir Spanish_dropout25_preTag_delex
	cd Spanish_dropout25_preTag_delex
	cp ../Data/Original/heldOut.crf ../Data/Original/heldOut-preTag_dropout25_delex.crf
	python ../Scripts/oracle_glample.py Spanish_dropout25_preTag_delex 200 preTag_delex ../Scripts/preprocess.py es LOC_MISC_ORG_PER ../Data/Original/heldOut-preTag_dropout25_delex.crf 1000 4000 5000 10000 20000 20000 20000 20000 50000 50000 50000 # should go up to about 250 k.. there is about 320 total b/w train and dev, another 50 in test
	rm ../Data/Original/heldOut-preTag_dropout25_delex.crf*
	cd ../
fi

#######################

if [[ $experiment_number == "13" ]]
then
	[ -d "Spanish_dropout00_preTag_delex" ] rm -rf "Spanish_dropout00_preTag_delex"
	mkdir Spanish_dropout00_preTag_delex
	cd Spanish_dropout00_preTag_delex
	cp ../Data/Original/heldOut.crf ../Data/Original/heldOut-preTag_dropout00_delex.crf
	python ../Scripts/oracle_glample.py Spanish_dropout00_preTag_delex 200 preTag_delex ../Scripts/preprocess.py es LOC_MISC_ORG_PER ../Data/Original/heldOut-preTag_dropout00_delex.crf 1000 4000 5000 10000 20000 20000 20000 20000 50000 50000 50000 # should go up to about 250 k.. there is about 320 total b/w train and dev, another 50 in test
	rm ../Data/Original/heldOut-preTag_dropout00_delex.crf*
	cd ../
fi

############### ONTO ENGLISH EVALUATION #########################

if [[ $experiment_number == "14" ]]
then
	[ -d "English_preTag_delex" ] rm -rf "English_preTag_delex"
	mkdir English_preTag_delex
	cd English_preTag_delex
	cp ../Data/Original/heldOut.crf ../Data/Original/heldOut-preTag_delex.crf
	python ../Scripts/oracle_glample.py English_preTag_delex 200 preTag_delex ../Scripts/preprocess.py en CARDINAL_DATE_EVENT_FAC_GPE_LANGUAGE_LAW_LOC_MONEY_NORP_ORDINAL_ORG_PERCENT_PERSON_PRODUCT_QUANTITY_TIME_WORKOFART ../Data/Original/heldOut-preTag_delex.crf 1000 4000 5000 10000 20000 20000 20000 20000 50000 50000 50000 50000 100000 100000 250000 250000
	rm ../Data/Original/heldOut-preTag_delex.crf*
	cd ../
fi

#######################

if [[ $experiment_number == "15" ]]
then
	[ -d "English_hardCappedUNKs" ] rm -rf "English_hardCappedUNKs"
	mkdir English_hardCappedUNKs
	cd English_hardCappedUNKs
	cp ../Data/Original/heldOut.crf ../Data/Original/heldOut-hardCappedUNKs.crf
	python ../Scripts/oracle_glample.py English_hardCappedUNKs 200 hardCappedUNKs ../Scripts/preprocess.py en CARDINAL_DATE_EVENT_FAC_GPE_LANGUAGE_LAW_LOC_MONEY_NORP_ORDINAL_ORG_PERCENT_PERSON_PRODUCT_QUANTITY_TIME_WORKOFART ../Data/Original/heldOut-hardCappedUNKs.crf 1000 4000 5000 10000 20000 20000 20000 20000 50000 50000 50000 50000 100000 100000 250000 250000
	rm ../Data/Original/heldOut-hardCappedUNKs.crf*
	cd ../
fi

#######################

if [[ $experiment_number == "16" ]]
then
	[ -d "English_random" ] rm -rf "English_random"
	mkdir English_random
	cd English_random
	cp ../Data/Original/heldOut.crf ../Data/Original/heldOut-random.crf
	python ../Scripts/oracle_glample.py English_random 200 random ../Scripts/preprocess.py en CARDINAL_DATE_EVENT_FAC_GPE_LANGUAGE_LAW_LOC_MONEY_NORP_ORDINAL_ORG_PERCENT_PERSON_PRODUCT_QUANTITY_TIME_WORKOFART ../Data/Original/heldOut-random.crf 1000 4000 5000 10000 20000 20000 20000 20000 50000 50000 50000 50000 100000 100000 250000 250000
	rm ../Data/Original/heldOut-random.crf*
	cd ../
fi



############### ANERcorp ARABIC EVALUATION #########################

if [[ $experiment_number == "17" ]]
then
	[ -d "Arabic_preTag_delex" ] rm -rf "Arabic_preTag_delex"
	mkdir Arabic_preTag_delex
	cd Arabic_preTag_delex
	python ../Scripts/oracle_glample.py Arabic_preTag_delex 200 preTag_delex ../Scripts/preprocess.py en LOC_MISC_ORG_PERS Data/Prepared/ANERfull-0.crf__Data/Prepared/ANERfull-1.crf__Data/Prepared/ANERfull-2.crf__Data/Prepared/ANERfull-3.crf__Data/Prepared/ANERfull-4.crf__Data/Prepared/ANERfull-5.crf__Data/Prepared/ANERfull-6.crf__Data/Prepared/ANERfull-7.crf__Data/Prepared/ANERfull-8.crf__Data/Prepared/ANERfull-9.crf 1000 4000 5000 10000 20000 20000 20000
	cd ../
fi

#######################

if [[ $experiment_number == "18" ]]
then
	[ -d "Arabic_random" ] rm -rf "Arabic_random"
	mkdir Arabic_random
	cd Arabic_random
	python ../Scripts/oracle_glample.py Arabic_random 200 random ../Scripts/preprocess.py en LOC_MISC_ORG_PERS Data/Prepared/ANERfull-0.crf__Data/Prepared/ANERfull-1.crf__Data/Prepared/ANERfull-2.crf__Data/Prepared/ANERfull-3.crf__Data/Prepared/ANERfull-4.crf__Data/Prepared/ANERfull-5.crf__Data/Prepared/ANERfull-6.crf__Data/Prepared/ANERfull-7.crf__Data/Prepared/ANERfull-8.crf__Data/Prepared/ANERfull-9.crf 1000 4000 5000 10000 20000 20000 20000
	cd ../
fi

