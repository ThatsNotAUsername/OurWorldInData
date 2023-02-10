# OurWorldInData

Mostly for data from "our world in data"

visualizing_OWID_oneTable: Can read in one given table. Creates scatter and map plots

examples:
********************************************************************************************
national-average-learning-outcomes-vs-government-expenditure-per-primary-student.csv
********************************************************************************************
```
name_project ='Learning_expenditure'

path_to_data_folder = '../../Daten/OurWorldInData/'  # where the data is stored

# name of the csv file
name_file = 'national-average-learning-outcomes-vs-government-expenditure-per-primary-student'

# year to consider for all static figures:
year_to_consider = 1
column_name_of_year = 'Year'
# if animation, until which year:
end_year = 1


# variables for the first file (eg column names). x (y) is the variable for x(y)-axis, 
# time: variable specifying the element if we want to do animated figures
# size: variable specifying the size of the element
# color: variable specifying the color of the element
# geo_code: geo data for drawing on maps
# name: name of the variable

# all variables defaults are FALSE, except for size which is None
# if y is set to FALSE only maps are drawn. 
# If x and y are given, one map each will be get drawn
dict_variables = {'x': 'Average harmonised learning outcome score in 2005-2015 (Altinok, Angrist, and Patrinos, 2018) ',
                   'y': 'Government expenditure per primary student (PPP$, 2006-2014)', 
                   'time': 'Year',
                   'size': None, 
                   'color': 'Continent', 
                   'name': 'Entity',
                   'geo_code': 'Code'}
                   
```                   
                   
********************************************************************************************
gdp-per-capita-vs-economic-inequality.csv
********************************************************************************************
```
name_project ='GDP_Gini'

path_to_data_folder = '../../Daten/OurWorldInData/'  # where the data is stored

# name of the csv file
name_file = 'gdp-per-capita-vs-economic-inequality'
# name_file = 'national-average-learning-outcomes-vs-government-expenditure-per-primary-student'

# year to consider for all static figures:
year_to_consider = 2018  
column_name_of_year = 'Year'
# if animation, until which year:
end_year = 2000


# variables for the first file (eg column names). x (y) is the variable for x(y)-axis, 
# time: variable specifying the element if we want to do animated figures
# size: variable specifying the size of the element
# color: variable specifying the color of the element
# geo_code: geo data for drawing on maps
# name: name of the variable

# all variables defaults are FALSE, except for size which is None
# if y is set to FALSE only maps are drawn. 
# If x and y are given, one map each will be get drawn
dict_variables = {'x': 'GDP per capita (expenditure, multiple price benchmarks)', 
                   'y': 'Gini coefficient', 
                   'time': 'Year',
                   'size': 'Population (historical estimates)',
                   'color': 'Continent', 
                   'name': 'Entity',
                   'geo_code': 'Code'}
```                   

********************************************************************************************
deaths-conflict-terrorism-per-100000.csv
********************************************************************************************                   
```
name_project ='death_terrorism'

path_to_data_folder = '../../Daten/OurWorldInData/'  # where the data is stored

# name of the csv file
name_file = 'deaths-conflict-terrorism-per-100000'

# year to consider for all static figures:
year_to_consider = 2018  
column_name_of_year = 'Year'
# if animation, until which year:
end_year = 2000


# variables for the first file (eg column names). x (y) is the variable for x(y)-axis, 
# time: variable specifying the element if we want to do animated figures
# size: variable specifying the size of the element
# color: variable specifying the color of the element
# geo_code: geo data for drawing on maps
# name: name of the variable

# all variables defaults are FALSE, except for size which is None
# if y is set to FALSE only maps are drawn. 
# If x and y are given, one map each will be get drawn
dict_variables = {'x': 'Deaths - Conflict and terrorism - Sex: Both - Age: All Ages (Rate)', 
                   'y': False, 
                   'time': 'Year',
                   'size': None, 
                   'color': False, 
                   'name': 'Entity',
                   'geo_code': 'Code'}       
                   
```                   

********************************************************************************************
mean-body-mass-index-bmi-in-adult-males.csv
********************************************************************************************                   
```
name_project ='BMI_males'

path_to_data_folder = '../../Daten/OurWorldInData/'  # where the data is stored

# name of the csv file
name_file = 'mean-body-mass-index-bmi-in-adult-males'


# year to consider for all static figures:
year_to_consider = 2016  
column_name_of_year = 'Year'
# if animation, until which year:
end_year = 2000


# variables for the first file (eg column names). x (y) is the variable for x(y)-axis, 
# time: variable specifying the element if we want to do animated figures
# size: variable specifying the size of the element
# color: variable specifying the color of the element
# geo_code: geo data for drawing on maps
# name: name of the variable

# all variables defaults are FALSE, except for size which is None
# if y is set to FALSE only maps are drawn. 
# If x and y are given, one map each will be get drawn
dict_variables = {'x': 'Mean BMI (male)', 
                   'y': False, 
                   'time': 'Year',
                   'size': None, 
                   'color': 'Continent', 
                   'name': 'Entity',
                   'geo_code': 'Code'}            
```                   
