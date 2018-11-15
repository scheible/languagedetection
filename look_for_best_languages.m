clear all;
path(path,[cd,filesep,'csv_histogram']);
data=csvread("1_first_norm.csv");
surf(exp(20*data))

sum=zeros(size(data,1),1);
treshold=30;
N=size(data,1);
for i=1:N
    for j=1:N
        sum(i)=sum(i)+data(j,i);
    end
end
    
rank_language_against_all=zeros(10,1);
for i=1:10 
    [val,rank_language_against_all(i)]=max(sum);
    sum(rank_language_against_all(i))=0;
end

data_bis=data;
rank_language_against_language=zeros(10,2);
for i=1:10 
    [val,rank]=max(data_bis(:));
    [rank_language_against_language(i,1), rank_language_against_language(i,2)] = ind2sub(size(data_bis),rank);
    data_bis(rank_language_against_language(i,1), rank_language_against_language(i,2))=0;
    data_bis(rank_language_against_language(i,2), rank_language_against_language(i,1))=0;
end
    