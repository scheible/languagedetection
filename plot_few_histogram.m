path(path,[cd,filesep,'csv_N2gram']);
data=csvread("0_global_file.csv",1,2);

fontsz=20;

phoneme=readtable("0_global_file.csv");
phoneme=phoneme(:,1);
phoneme_list=table2array(phoneme);
fct1=data(:,133);
% fct2=data(:,12);
% fct=[fct1 fct2];
bar(fct1)
% set(gca,'xtick',[1:length(phoneme_list)],'xticklabel',phoneme_list)
% title('Histogram of two languages : Polish and Arabic','Fontsize',fontsz+3)
% title('2-gram of one language : Polish','Fontsize',fontsz+3)
xlabel('Phonemes','Fontsize',fontsz)
ylabel('Probability','Fontsize',fontsz)
% legend({"Polish","Arabic"},'Location','northeast','Fontsize',fontsz);

equals_0=find(fct1==0);
mini=min(fct1(fct1>0));
min_rank=find(fct1==mini);