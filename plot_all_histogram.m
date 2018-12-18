clear all;
path(path,[cd,filesep,'csv_histogram']);
data=csvread("0_global_file.csv",1,2);

phoneme=readtable("0_global_file.csv");
phoneme=phoneme(:,1);
phoneme_list=table2array(phoneme);
fct=data(:,133);
bar(fct)
set(gca,'xtick',[1:42],'xticklabel',phoneme_list)
