rm -r myExperiment
mkdir myExperiment
cd myExperiment

# python ../Scripts/oracle.py myExperiment 100 random ../Scripts/preprocess_Davids_data.py fr 15000 30000

# python ../Scripts/oracle.py myExperiment 100 rapidUncertainty ../Scripts/preprocess_Davids_data.py fr 15000 30000

python ../Scripts/oracle.py myExperiment 300 hardCappedUNKs ../Scripts/preprocess_Davids_data.py fr 15000 30000

# python ../Scripts/oracle.py myExperiment 300 rapidEntityDiversity ../Scripts/preprocess_Davids_data.py fr 15000 30000

cd ../