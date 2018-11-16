## Setting Up Your Workspace

If you have *git* installed, run the commands below (you can install git via these [instructions](https://www.linode.com/docs/development/version-control/how-to-install-git-on-linux-mac-and-windows/))
```
git clone https://github.com/alexerdmann/HER
cd HER
```
Otherwise, download HER from this [url](https://github.com/alexerdmann/AgnosticNER.git) and navigate to the downloaded HER directory in the terminal by typing *cd* followed by a space, then dragging the HER directory into your terminal window, then pressing enter.

Now it's time to come up with a name for your project and let HER create a folder to work in:
```
name_of_project=[name-of-your-project]
sh Scripts/set_up_work_space.sh $name_of_project
cd $name_of_project
```
*At this point, you are now in the directory HER/$name_of_project/. All future commands will be run from within this $name_of_project folder, not outside of it, and all data should be stored within this $name_of_project folder as well.*

*By the way, if you have used HER for one project and now want to use her for another, you don't need re-download HER from github. Simply re-define your parameters as described earlier, navigate out of the* name_of_project *subdirectory to the* HER *super-directory, run the commands immediately above, and then continue from here*

Upload all the raw texts that you want to extract named entities from
* Put texts in the *Data/Original/* folder in your new project directory
	* *Make sure you don't accidentally put them in* HER/Data/Original/
* The data you put in *Data/Original/* must be *.txt* or *.xml* files, no folders and no other formats/extensions
	* Handling HTML files is on the to-do list

Upload any relevant gazetteers (lists of entities you want to identify) if you have them.
* Gazatteer files should have one entity per line and be placed in *Data/Gazatteers/* with the filename [type-of-entity].gaz
	* A sample gazatteer is located at *../Data/Gazatteers/GEO.gaz*
	* The type of entities in the gazatteer need not exactly match any of the types of entities you want to identify, though if it does, make sure that [type-of-entity] in the filename matches exactly one of the underscore-separated entity types you defined in the *entities* variable

No filenames in either *Data/Original/* or *Data/Gazatteers/* should contain any of the following abominations:
* spaces
* non-ascii characters, e.g., accents, diacritics, chinese letters, etc.
* punctuation other than dash (-) and underscore (\_), i.e., avoid characters like quotations, comments, any form of bracket, etc.

*For the sake of example, I'll use the sample texts and sample gazatteer included with the download by running the following commands.. if you are using your own data and own gazatteers, don't run the following commands:*
```
cp ../Data/Original/French.zip Data/. # This copies the zipped file into the Data/ subdirectory of your new work space
unzip Data/French.zip
mv French/* Data/Original/. # Moves the unzipped data into the Data/Original/ folder
rm -rf French # Gets rid of the now empty folder the data came in
rm Data/French.zip # Gets rid of the original zipped copy of the folder
cp ../Data/Gazatteers/GEO.gaz Data/Gazatteers/GEO.gaz # Copies the sample gazatteer into your new project's Data/Gazatteers/ folder
```