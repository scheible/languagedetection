import sys, os
from shutil import copyfile


if (len(sys.argv) != 4):
	print("usage: "+os.path.split(sys.argv[0])[1]+" <path_to_MP3_data> <folder_to_store_the_MP3_data_in> <label.csv_file>")
	sys.exit()

pathToMP3Data = sys.argv[1]
pathToStoreMP3Data = sys.argv[2]
labelFileName = sys.argv[3]

labelFile = open(labelFileName,"r")

for line in labelFile:
	[audioFileName, languageLabel] = line.split(",")

	audioFileName = audioFileName.strip()
	languageLabel = languageLabel.strip()

	#Check if there is a folder with the same name as the language
	folderName = os.path.join(pathToStoreMP3Data,languageLabel)
	if not os.path.isdir(folderName):
		os.mkdir(folderName)

	mp3source = os.path.join(pathToMP3Data,audioFileName)
	mp3target = os.path.join(folderName,audioFileName)
	copyfile(mp3source, mp3target)

	print(mp3source + " -> " + mp3target)

	#print(audioFileName + " -  " + languageLabel)
