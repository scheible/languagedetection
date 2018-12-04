import os
import codecs
import numpy as np



def new_phoneme(counter,list_phoneme,phon,num_language):
    language_enumeration=0
    while language_enumeration <len(counter):                            #we add a row for the new phoneme in each language
        counter[language_enumeration].append(0)
        language_enumeration+=1
    counter[num_language][-1]=1;                     #the language in which we found the phoneme is incremented for this one
    list_phoneme.append(phon)                        #we add the new phoneme to the list
    return




def split_data(path,split):
    files_path = path
    directories = os.listdir(files_path)
    print(directories)
    X=[]
    x_train = []
    x_test = []
    y=[]
    y_train=[]
    y_test=[]
    language_list=[]
    temp = ""

    for num_language,language in enumerate(directories):
        if language[-3:] == "txt":
            language_list.append(language[:-4])
            file_language = codecs.open(files_path + "\\" + language, 'r', "utf-8-sig").read()
            file_language = file_language.replace("\r", "")
            file_language = file_language.replace("+", "")
            for letter in file_language:
                if letter != "\n":
                    temp = temp + letter
                else:
                    X.append(temp)
                    temp=""
                    y.append(language[:-4])
            x_train.extend(X[:int(split*len(X))])
            x_test.extend(X[int(split * len(X)):])
            y_train.extend(y[:int(split*len(X))])
            y_test.extend(y[int(split * len(X)):])
            X=[]
            y=[]
    return (x_train,y_train),(x_test,y_test),language_list


def make_histogram(train,labels,Languages):
    phonemes_count = []  # 2 dimensional array , one list per language
    number_sample_read = []  # one per language
    for i in range (1,len(Languages)):
        phonemes_count.append([])
        number_sample_read.append(0)
    phonemes_list = []

    temp=""

    for num_sample,sample in enumerate(train):
        for num_language,language in enumerate(Languages):
            if language==labels[num_sample]:
                for letter in sample:
                    if letter != " ":
                        temp = temp + letter
                    else:
                        found = False
                        for rang_phoneme, phoneme in enumerate(phonemes_list):
                            if phoneme == temp:
                                found = True
                                phonemes_count[num_language][rang_phoneme] += 1
                                break
                        if not found:
                            new_phoneme(phonemes_count, phonemes_list, temp,num_language)
                        temp = ""
                        number_sample_read[num_language]+=1

                break

    phonemes_count=np.asarray(phonemes_count)
    return phonemes_count,phonemes_list



path=os.path.dirname(__file__)+"/phonemes_few_languages"
split=0.7
(x_train,y_train),(x_test,y_test),language_list=split_data(path,split)

print(len(x_train))
print(len(y_train))
print(len(x_test))
print(len(y_test))
print(language_list)
print(x_train[0])
print(x_test[-1])
print(y_train[0])
print(y_test[-1])

histogram,phonemes=make_histogram(x_train,y_train,language_list)
print(phonemes)
print(histogram.shape)

