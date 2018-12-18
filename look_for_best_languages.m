% path(path,[cd,filesep,'csv_histogram']);
data=csvread("1_kullback-leibler_few_languages.csv");
h=bar3(data,0.5)

for i = 1:length(h)
     zdata = get(h(i),'Zdata');
     set(h(i),'Cdata',zdata)
end
set(gca,'xtick',[1:5],'xticklabel',{'Arabic','Dutch','Korean', 'Polish', 'Romanian'},'FontWeight','Bold', 'LineWidth', 2)
set(gca,'ytick',[1:5],'yticklabel',{'Arabic','Dutch','Korean', 'Polish', 'Romanian'},'FontWeight','Bold', 'LineWidth', 2)
set(gca,'color','none')
set(gca,'linewidth',4)


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