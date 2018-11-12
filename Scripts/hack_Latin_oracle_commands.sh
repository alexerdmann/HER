rm -r Latin_experiment
mkdir Latin_experiment
cd Latin_experiment

python ../Scripts/oracle_glample.py Latin_experiment 200 preTag_delex ../Scripts/preprocess.py en GEO_GRP_PRS 5000 5000 5000 5000 5000 5000 

cd ../
