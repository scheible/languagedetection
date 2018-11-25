clear all;
path(path,[cd,filesep,'csv_histogram']);
data=csvread("0_global_file.csv",1,2);

surf(exp(20*data))
