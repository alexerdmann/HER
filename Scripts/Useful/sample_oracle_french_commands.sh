rm -r myExperiment
mkdir myExperiment
cd myExperiment

# python ../Scripts/oracle.py myExperiment 300 random ../Scripts/preprocess_Davids_data.py fr GEO 5000 5000 5000 5000 5000 5000 

# python ../Scripts/oracle.py myExperiment 300 hardCappedUNKs ../Scripts/preprocess_Davids_data.py fr GEO 5000 5000 5000 5000 5000 5000 

python ../Scripts/oracle.py myExperiment 300 preTag_delex ../Scripts/preprocess_Davids_data.py fr GEO 5000 5000 5000 5000 5000 5000 

cd ../
