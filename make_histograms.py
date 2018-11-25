from os import listdir, path

def addPhonemeToHistogram(phoneme, histogram, languageIndex):
	global MAX_LANG

	for h in histogram:
		if (h[0] == phoneme):
			h[languageIndex] +=1
			return

	new = [phoneme] + [0]*MAX_LANG
	new[languageIndex] = 1
	histogram.append(new)


def normalizeHistogram(histogram):
	global MAX_LANG

	for j in range(1,MAX_LANG):

		# first sum up the column
		summ = 0
		for h in histogram:
			summ+=h[j]

		# next divide every value by the sum
		for h in histogram:
			if (summ != 0):
				h[j] = int((h[j]/float(summ))*100000)

	#return histogram

def createHistogramForFile(inFileName, languageIndex, histogram):
	print(inFileName, "\t->")

	inFile = open(path.join(PHONEME_FOLDER,inFileName),"r")
	

	for line in inFile:

		for phoneme in line.split(" "):
			addPhonemeToHistogram(phoneme, histogram, languageIndex)

	inFile.close()


PHONEME_FOLDER = "phonemes"
HIST_FOLDER = "histograms"
MAX_LANG = 120

histogram = []
header = ["Phoneme"]

i=1
for file in listdir(PHONEME_FOLDER):
	header.append(file)
	createHistogramForFile(file, i, histogram)
	i+=1

normalizeHistogram(histogram)

outFile = open("histogram.csv", "w")

for h in header:
	outFile.write(h + ";")
outFile.write("\n")

for h in histogram:

	for j in range(0,MAX_LANG):
		outFile.write(str(h[j]) + ";")
	outFile.write("\n")

outFile.close()