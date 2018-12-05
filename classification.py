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
                    y.append(num_language)
            x_train.extend(X[:int(split*len(X))])
            x_test.extend(X[int(split * len(X)):])
            y_train.extend(y[:int(split*len(X))])
            y_test.extend(y[int(split * len(X)):])
            X=[]
            y=[]
    return (x_train,y_train),(x_test,y_test),language_list

def make_histogram(train,labels,Languages):
    phonemes_count = []  # 2 dimensional array , one list per language
    number_phoneme_read = []  # one per language
    for i in range (len(Languages)):
        phonemes_count.append([])
        number_phoneme_read.append(0)
    phonemes_list = []

    temp=""

    for num_sample,sample in enumerate(train):
        for num_language,language in enumerate(Languages):
            if num_language==labels[num_sample]:
                for letter in sample:
                    if letter != " ":
                        temp = temp + letter
                    else:
                        found = False
                        for num_phoneme, phoneme in enumerate(phonemes_list):
                            if phoneme == temp:
                                found = True
                                # print(num_language)
                                # print(rang_phoneme)
                                # print(np.asarray(phonemes_count).shape)
                                phonemes_count[num_language][num_phoneme] += 1
                                break
                        if not found:
                            new_phoneme(phonemes_count, phonemes_list, temp,num_language)
                        temp = ""
                        number_phoneme_read[num_language]+=1

                break
    print(number_phoneme_read)
    phonemes_count=np.asarray(phonemes_count,dtype=np.float32)
    for i in range(len(phonemes_count)):
        phonemes_count[i]=phonemes_count[i]/number_phoneme_read[i]
    return phonemes_count,phonemes_list


def make_histogram_sample(sample,all_phonemes):
    histogram = np.zeros(len(all_phonemes))
    number_phoneme_read = 0

    temp=""
    for letter in sample:
        if letter != " ":
            temp = temp + letter
        else:
            found = False
            for num_phoneme, phoneme in enumerate(all_phonemes):
                if phoneme == temp:
                    found = True
                    # print(num_language)
                    # print(rang_phoneme)
                    # print(np.asarray(phonemes_count).shape)
                    histogram[num_phoneme] += 1
                    break
            if not found:
                print("new phoneme in the sample")
            temp = ""
            number_phoneme_read+=1
    histogram=histogram/number_phoneme_read
    return histogram

def make_N2gram(train,labels,Languages):
    phonemes_count = []  # 2 dimensional array , one list per language
    number_phoneme_read = []  # one per language
    for i in range(len(Languages)):
        phonemes_count.append([])
        number_phoneme_read.append(0)
    phonemes_list = []

    temp = ""
    first_space=True
    for num_sample, sample in enumerate(train):
        for num_language, language in enumerate(Languages):
            if num_language == labels[num_sample]:
                for letter in sample:
                    if letter != " ":
                        temp = temp + letter
                    else:
                        if first_space:
                            first_space = False
                            temp = temp + "-"
                        else:
                            first_space = True
                            found = False
                            for num_phoneme, phoneme in enumerate(phonemes_list):
                                if phoneme == temp:
                                    found = True
                                    # print(num_language)
                                    # print(rang_phoneme)
                                    # print(np.asarray(phonemes_count).shape)
                                    phonemes_count[num_language][num_phoneme] += 1
                                    break
                            if not found:
                                new_phoneme(phonemes_count, phonemes_list, temp, num_language)
                            temp = ""
                            number_phoneme_read[num_language] += 1

                break
    print(number_phoneme_read)
    phonemes_count = np.asarray(phonemes_count, dtype=np.float32)
    for i in range(len(phonemes_count)):
        phonemes_count[i] = phonemes_count[i] / number_phoneme_read[i]
    return phonemes_count, phonemes_list

def likelihood_computation(err,hist,phon):
    for i in range (len(hist)):
        err[i]=err[i]*hist[i][phon]
    return err

def likelihood(sample,all_phonemes,histograms):
    temp=""
    temp_result = np.full(len(histograms), 1.0)
    for letter in sample:
        if letter != " ":
            temp = temp + letter
        else:
            found = False
            for num_phoneme, phoneme in enumerate(all_phonemes):
                if phoneme == temp:
                    temp_result = likelihood_computation(temp_result, histogram, num_phoneme)
                    found = True
                    break
            if not found:
                temp_result = np.zeros(len(histograms), dtype=np.float32)
                print("unfound phoneme")
            temp = ""
    # print(temp_result)
    return np.argmax(temp_result)


def kullback_leibler(sample,all_phoneme,global_histogram):
    histogram=make_histogram_sample(sample,all_phoneme)
    result=np.zeros(len(global_histogram))
    for lang in range(len(global_histogram)):
        for phon in range (len(histogram)):
            if (histogram[phon]!= 0) and (global_histogram[lang][phon]!=0):
                result[lang]+=histogram[phon]*np.log(histogram[phon]/global_histogram[lang][phon])
    return np.argmin(result)


def accuracy(CM):
    total=np.sum(CM)
    true=0.0
    for i in range (len(CM)):
        true+=CM[i][i]
    result=true/total
    return result

def test(x,y,histograms,all_phonemes):
    confusion_matrix=np.zeros((len(histograms),len(histograms)))
    for num_sample,sample in enumerate(x) :
        #predicted=likelihood(sample,all_phonemes,histograms)
        predicted=kullback_leibler(sample,all_phonemes,histograms)
        confusion_matrix[y[num_sample]][predicted] += 1
    return confusion_matrix

def test_2gram(x,y,histograms,all_phonemes):
    temp_result=np.full(len(histograms),1.0)
    confusion_matrix=np.zeros((len(histograms),len(histograms)))
    temp=""
    first_space=True
    for num_sample,sample in enumerate(x) :
        for letter in sample:
            if letter != " ":
                temp = temp + letter
            else:
                if first_space:
                    first_space = False
                    temp = temp + "-"
                else:
                    first_space = True
                    found = False
                    for num_phoneme, phoneme in enumerate(all_phonemes):
                        if phoneme == temp:
                            temp_result=likelihood(temp_result,histogram,num_phoneme)
                            found=True
                            break
                    if found==False:
                        temp_result=np.zeros(len(histograms),dtype=np.float32)
                        print("unfound phoneme")
                    temp = ""
        #print(temp_result)
        confusion_matrix[y[num_sample]][np.argmax(temp_result)]+=1
        temp_result = np.full(len(histograms),1.0)
    return confusion_matrix

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
print(histogram)


result=test(x_test,y_test,histogram,phonemes)
print(result)
acc=accuracy(result)
print(acc)