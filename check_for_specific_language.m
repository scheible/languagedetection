path(path,[cd,filesep,'csv_N2gram']);
run open_list_languages
number_of_language_in_list=zeros(5,1);

number_of_language_in_list(1)=find(languagelist=="Arabic");
number_of_language_in_list(2)=find(languagelist=="Korean South");
number_of_language_in_list(3)=find(languagelist=="Dutch");
number_of_language_in_list(4)=find(languagelist=="Romanian");
number_of_language_in_list(5)=find(languagelist=="Polish");