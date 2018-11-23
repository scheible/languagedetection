import os

#read .txt
import codecs

#wreate and read csv
import csv


#graph
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def new_phoneme(counter,list_phoneme,phon):
    language_enumeration=0
    while language_enumeration <len(counter):                            #we add a row for the new phoneme in each language
        counter[language_enumeration].append(0)
        language_enumeration+=1
    counter[0][-1]=1;                                  #the one counting all the phoneme is incremented for this one
    counter[-1][-1]=1;                                   #the language in which we found the phoneme is incremented for this one
    list_phoneme.append(phon)                        #we add the new phoneme to the list
    return

def new_language(counter, list_phoneme, list_language,number_phoneme, lang):
    counter.append([0]*len(list_phoneme))
    list_language.append(lang[:-4])
    number_phoneme.append(0)
    return





files_path=os.path.dirname(__file__)+"\\phonemess2"
directories=os.listdir(files_path)
print(directories)
phonemes_count=[[]]  # 2 dimensional array , one list per language , first one = total
phonemes_list=[]
languages_list=["All"]
number_sample_read=[0]


#N_gram to do
N_gram_to_do=[2]

temp=""
for language in directories :
    if language[-3:]=="txt" :
        file_language=codecs.open(files_path+"\\"+language,'r',"utf-8-sig").read()
        new_language(phonemes_count,phonemes_list,languages_list,number_sample_read,language)
        file_language=file_language.replace("\n","")
        file_language = file_language.replace("\r", "")
        file_language = file_language.replace("+", "")
        for letter in file_language :
            if letter!=" ":
                temp=temp+letter
            else :
                found=False
                for rang_phoneme,phoneme in enumerate(phonemes_list) :
                    if phoneme==temp :
                        found=True
                        phonemes_count[0][rang_phoneme] += 1
                        phonemes_count[-1][rang_phoneme]+=1
                        break
                if not found:
                    new_phoneme(phonemes_count, phonemes_list, temp)
                number_sample_read[0] += 1
                number_sample_read[-1] += 1
                temp=""


print(languages_list)
print(phonemes_list)
# objects = phonemes_list
# y_pos = np.arange(len(objects))
# performance = [y/number_sample_read[0] for y in phonemes_count[0]]
# plt.figure(0)
# plt.bar(y_pos, performance, align='center', alpha=0.8)
# plt.xticks(y_pos, objects)
# plt.xticks(rotation=45)
# plt.xlabel('phoneme')
# plt.title('All languages')

#plt.show(block=False)
#
# plt.figure(1)
# for i in range (1,len(languages_list)):
#     objects = phonemes_list
#     y_pos = np.arange(len(objects))
#     performance = [y/number_sample_read[i] for y in phonemes_count[i]]
#
#     plt.bar(y_pos, performance, align='center', alpha=0.2)
#     plt.xticks(y_pos, objects)
#     plt.xticks(rotation=45)
#     plt.xlabel('phoneme')
#     plt.title('comparaison between language')
#
# #plt.show()


for numLang, language in enumerate(languages_list):
    with open(os.path.dirname(__file__)+"\\csv_histogram\\"+language+'.csv', 'w',newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        result=[phonemes_list,phonemes_count[numLang]]
        filewriter.writerow(phonemes_list)
        filewriter.writerow(phonemes_count[numLang])


with open(os.path.dirname(__file__)+"\\csv_histogram\\0_global_file.csv", 'w',newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(["list of phonemes"] + languages_list)
    for numPhoneme, phoneme in enumerate(phonemes_list):
        x=[]
        x.append(phoneme)
        for numLang,language in enumerate(languages_list):
            x.append(phonemes_count[numLang][numPhoneme]/number_sample_read[numLang])
        filewriter.writerow(x)


with open(os.path.dirname(__file__)+"\\csv_histogram\\0_language_list.csv", 'w',newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(languages_list[1:])







