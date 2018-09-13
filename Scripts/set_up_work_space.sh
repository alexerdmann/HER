name_of_project=$1

mkdir $name_of_project
for dir in Data Models Scripts Results; do cp -r $dir $name_of_project/.; done
cd $name_of_project
rm Data/Original/*

echo " "
echo "Please cp all raw texts in your corpus to Data/Original/."
echo "Make sure all such texts have a .txt or .xml extension and that you run the cp command from the new directory:"
echo $name_of_project
echo " "