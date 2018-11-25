import osgit stat


#wreate and read csv
import csv

import numpy as np


def second_norm(list_language,list_phoneme,data):
    result=np.zeros((len(list_language),len(list_language)))
    for i in range (0,len(list_language)) :
        for j in range (i,len(list_language)) :
            for p in range (0,len(list_phoneme)) :
                norm_2=pow(data[p][i]-data[p][j],2);
                result[i][j]=result[i][j]+norm_2
            result[i][j]=np.sqrt(result[i][j])
            result[j][i]=result[i][j]
    return result


def first_norm(list_language,list_phoneme,data):
    result=np.zeros((len(list_language),len(list_language)))
    for i in range (0,len(list_language)) :
        for j in range (i,len(list_language)) :
            for p in range (0,len(list_phoneme)) :
                norm_1=abs(data[p][i]-data[p][j]);
                result[i][j]=result[i][j]+norm_1
            result[j][i]=result[i][j]
    return result




file_path=os.path.dirname(__file__)+"\\csv_N2gram\\0_global_file.csv"


Data=[]
phonemes_list=[]
with open(file_path, "r") as csvfile :
    file=csv.reader(csvfile)
    for i,row in enumerate(file) :
        if i==0 :
            language_list=row[2:]
        else :
            phonemes_list.append(row[0])
            Data.append(list(map(float,row[2:])))



with open(os.path.dirname(__file__)+"\\csv_N2gram\\1_first_norm.csv", 'w',newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    norm=first_norm(language_list,phonemes_list,Data)
    for line in norm :
        filewriter.writerow(line)


print(language_list)
print(phonemes_list)
