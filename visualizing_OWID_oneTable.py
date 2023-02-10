#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 13:16:22 2023

@author: annika

Using data from https://ourworldindata.org/ we create static and animated figures visualizing the data

it is assumed the file is given as csv table

at most 2 files of data can be compared
both are csv files from Our World in Data (OWID) 

it can specified which columns will be compared to each other. 
depending on the types of analyses other columns can be inlcuded for more 
details in the figures

"""


from matplotlib import pyplot as plt
import plotly.express as px
import pandas as pd
import os
import geojson
import json
from matplotlib import animation
import seaborn as sns
import numpy as np
from textwrap import wrap
import textwrap
import plotly.express as px

# %% declare variables
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

# if set to False, the plots won't be generated. 
# if y is not given, scatterplots are'n generated
# note that the animated map plots can take long
do_scatterplots = True
do_animated_scatterplots = True
do_mapplots = True
do_animated_mapplots = True

# %% Output folders:
folder_maps = 'output/maps/'
if not os.path.exists(folder_maps):
    os.makedirs(folder_maps)  
folder_maps = folder_maps  + name_project + '_'

folder_gifs = 'output/gifs/'
if not os.path.exists(folder_gifs):
    os.makedirs(folder_gifs)
folder_gifs = folder_gifs + name_project + '_'
    
folder_scatterplots = 'output/scatterplots/' 
if not os.path.exists(folder_scatterplots):
    os.makedirs(folder_scatterplots)
folder_scatterplots = folder_scatterplots + name_project + '_'
 
folder_QC = 'output/QC/'
if not os.path.exists(folder_QC):
    os.makedirs(folder_QC)
folder_QC = folder_QC + name_project + '_'
 
# %% read in data 
df = pd.read_csv(path_to_data_folder + name_file + '.csv')  # co2 emission per year per country

columns = list(df.columns)

df_iso_countries = pd.read_excel(path_to_data_folder + 'all_iso_countries.xlsx')  # info about coutnries, like codes, continent, capital, etc
df_iso_countries.rename(columns={'ISO3':'Code'}, inplace=True)  # have to rename the 3-iso code for merging it with the other df

if 'Continent' in df.columns:
    df.drop(labels=['Continent'], axis=1, inplace=True)

df.set_index(['Code'], inplace=True)
df_iso_countries.set_index(['Code'], inplace=True)

df = df.join(df_iso_countries).reset_index()

time_frame = list(range(end_year,year_to_consider+1))


if not dict_variables['y']:
    do_scatterplots = False
    do_animated_scatterplots = False
    
# %% x-axis lables often too many and we want them rotated
def prep_xaxis(ax, n=20):
    # keep only part of the labels
    # n = 20  # Keeps every nth label
    [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
    
    # rotate ticks, better readible
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    
    # remove ticks (annoying, looks ugly)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    
    ax.xaxis.label.set_size(fontsize=14)  # increase fontsize

# %% QC 
# count number of x and y variables for given year:
df_of_year_to_consider = df[df[column_name_of_year]==year_to_consider]
number_name_unique = len(set(df[dict_variables['name']]))
number_name_unique_in_year_to_consider = len(set(df_of_year_to_consider[dict_variables['name']]))
number_x_in_year_to_consider = len(df_of_year_to_consider[dict_variables['x']].dropna())

if dict_variables['y']:
    number_y_in_year_to_consider = len(df_of_year_to_consider[dict_variables['y']].dropna())    
    overlap_x_y = df_of_year_to_consider.dropna(subset=[dict_variables['x'], dict_variables['y']], how='any')
    number_overlap_x_y = len(overlap_x_y)

    print('\n#####################################################################')
    print(f'Number of ALL names in year {year_to_consider} is: {number_name_unique_in_year_to_consider}\n')
    print(f'Number of x values in year {year_to_consider} is: {number_x_in_year_to_consider}\n')
    print(f'Number of y values in year {year_to_consider} is: {number_y_in_year_to_consider}\n')
    print(f'Number of overlap x and y names in year {year_to_consider} is: {number_overlap_x_y}\n')
    print('Details are in the QC folder')
    print('#####################################################################\n')
    overlap_x_y.to_csv(folder_QC + 'overlap_x_y.csv')
    
else:
    print('\n#####################################################################')
    print(f'Number of ALL names in year {year_to_consider} is: {number_name_unique_in_year_to_consider}\n')
    print(f'Number of x values in year {year_to_consider} is: {number_x_in_year_to_consider}\n')
    print('Note: no y variable is given')
    print('#####################################################################\n')
        

df_time_frame_consider = df[df[column_name_of_year].isin(time_frame)]

relevant_keys = ['x', 'y', 'color', 'size', 'name']
subset = [dict_variables[key] for key in relevant_keys if dict_variables[key]]  # remove false
# if dict_variables['y']:
#     df_time_frame_consider_nonan = df_time_frame_consider.dropna(subset=[dict_variables['x'], 
#             dict_variables['y'], dict_variables['color'], dict_variables['size'], dict_variables['name']], how='any')
# else:
#     df_time_frame_consider_nonan = df_time_frame_consider.dropna(subset=[dict_variables['x'], 
#             dict_variables['color'], dict_variables['size'], dict_variables['name']], how='any')

df_time_frame_consider_nonan = df_time_frame_consider.dropna(subset=subset, how='any')

# we want to keep only those countries which appear a certain amount of time
number_countries = df_time_frame_consider_nonan[dict_variables['name']].value_counts()
int(len(time_frame)/2)
keep_countries = list(number_countries[number_countries>=len(time_frame)/2].index)


df_time_frame_consider_nonan = df_time_frame_consider_nonan[df_time_frame_consider_nonan[dict_variables['name']].isin(keep_countries)]
number_names_time_frame_nonans = len(set(df_time_frame_consider_nonan[dict_variables['name']]))
print('\n#####################################################################')
print(f'Number of names in given time frame {year_to_consider} until {end_year} after removing nan values  is: {number_names_time_frame_nonans}\n')
print('#####################################################################\n')


# check how many nans for x and y values:
df['non_nan_x'] = df[dict_variables['x']].count()#isnull()
if dict_variables['y']:
    df['non_nan_y'] = df[dict_variables['y']].count()#isnull()
df_counted_non_nans = df.groupby([dict_variables['name']]).sum()
df_counted_non_nans.reset_index(inplace=True)
df_counted_non_nans.sort_values(by=['non_nan_x'], inplace=True)

fig, ax = plt.subplots(figsize=(6, 26), dpi=600)
sns.barplot(data=df_counted_non_nans, y=dict_variables['name'], x='non_nan_x', palette="PuBuGn")
plt.title("\n".join(wrap('Number of non nan values for ' + dict_variables['x'])))
plt.yticks(fontsize=5)
plt.tight_layout()
plt.savefig(folder_QC + 'number_non_nanvalues_x.png')

if dict_variables['y']:
    fig, ax = plt.subplots(figsize=(6, 26), dpi=600)
    sns.barplot(data=df_counted_non_nans, y=dict_variables['name'], x='non_nan_y', palette="PuBuGn")
    plt.title("\n".join(wrap('Number of non nan values for ' + dict_variables['y'])))
    plt.yticks(fontsize=5)
    plt.tight_layout()
    plt.savefig(folder_QC + 'number_non_nanvalues_y.png')

# have to remove all the nans
# relevant_keys = ['x', 'y', 'color', 'size', 'name']
# subset = [dict_variables[key] for key in relevant_keys if dict_variables[key]]  # remove false
# if dict_variables['y']:
#     df_of_year_to_consider_nonan = df_of_year_to_consider.dropna(subset=[dict_variables['x'], 
#                 dict_variables['y'], dict_variables['color'], dict_variables['size'], dict_variables['name']], how='any')
# else:
#     df_of_year_to_consider_nonan = df_of_year_to_consider.dropna(subset=[dict_variables['x'], 
#                 dict_variables['color'], dict_variables['size'], dict_variables['name']], how='any')
df_of_year_to_consider_nonan = df_of_year_to_consider.dropna(subset=subset, how='any')
print('\n#####################################################################')
print(f'Number of data points after removing all nan values is: {len(df_of_year_to_consider_nonan)}\n')
print('#####################################################################\n')

# %% Scatter plots:
if do_scatterplots:

    # - bubble-scatter plot: x and y given (in one or two files), third variable 
    #   is size. 4th variable is color (example: gdp, gini, inhibitants, continent)
    
    # sns.scatterplot(data=df_of_year_to_consider, x=dict_variables['x'], y=dict_variables['y'], 
    #                 size=dict_variables['size'], hue=dict_variables['color'], palette='Pastel2', 
    #                 sizes=(20,2000))
    
    # first static, but interactive plot
   
    fig = px.scatter(df_of_year_to_consider_nonan, x=dict_variables['x'], y=dict_variables['y'],
                     color=dict_variables['color'], size=dict_variables['size'], 
                     hover_data=[dict_variables['name']], size_max=50, text=dict_variables['name'], 
                     log_x=True, title="\n".join(wrap(name_project + ' in year ' + str(year_to_consider))))
    fig.update_traces(marker_sizemin=5, textposition='top center')
    fig.write_html(folder_scatterplots + "scatterplot_" + str(dict_variables['x']) + '_vs_' + dict_variables['y'] + ".html")
    fig.write_image(folder_scatterplots + "scatterplot_" + str(dict_variables['x']) + '_vs_' + dict_variables['y'] + ".png")

if do_animated_scatterplots:
    # animated plot
    df_time_frame_consider_nonan.sort_values(by=[column_name_of_year], inplace=True)
    fig = px.scatter(df_time_frame_consider_nonan, x=dict_variables['x'], y=dict_variables['y'],
                     color=dict_variables['color'], size=dict_variables['size'], 
                     hover_data=[dict_variables['name']], size_max=50, text=dict_variables['name'], 
                     animation_frame=column_name_of_year, animation_group=dict_variables['name'])
    fig.update_traces(marker_sizemin=5, textposition='top center')
    fig.write_html(folder_scatterplots + "scatterplot_time_" + str(dict_variables['x']) + '_vs_' + dict_variables['y'] + ".html")



# %% maps

# for x and given year
# for y (if given)
# --> end_year given for time if animated


# choro maps

# we need geo data for the countries in order to color them based on their borders:
with open('../../Daten/countries.geojson') as f:
    gj = geojson.load(f)

# co2 country
# Kuwait is way higher than the rest. Will replace the value:
# row_kuwait = df_co2_last_year_use[df_co2_last_year_use['country']=='Kuwait']

def draw_choropleth(df,
                    locations,
                    color,
                    title_text,
                    file_name,
                    color_continuous_scale='Viridis',
                    locationmode='ISO-3',
                    geojson=gj,
                    animation_frame=False,
                    ):
    split_text = textwrap.wrap(title_text,width=70)  # in case title is too long
    
    if not animation_frame:    
        fig = px.choropleth(df, locations=locations, color=color,
                                   color_continuous_scale=color_continuous_scale, 
                                   locationmode=locationmode,
                                   geojson=gj,
                                   range_color=(min(df[color]), max(df[color]))
                                  )
        
        # make the colorbar where it is supposed to be and a nice size 
        fig.update_layout(coloraxis_colorbar=dict(
            title="",
            thicknessmode="pixels", thickness=20,
            lenmode="pixels", len=200
        ), 
            title_text='<br>'.join(split_text), title_x=0.5, title_y=.85
            )
        
        # save figure
        fig.write_image(folder_maps + file_name + ".png")
    else:
        fig = px.choropleth(df, locations=locations, color=color,
                                   color_continuous_scale=color_continuous_scale, 
                                   locationmode=locationmode,
                                   geojson=gj,
                                   animation_frame = animation_frame,
                                   range_color=(min(df[color]), max(df[color]))
                                  )
        fig.write_html(folder_maps + file_name + ".html")

if dict_variables['y']:
    var_list = ['x', 'y']
    # have to remove all the nans
    
    df_of_year_to_consider_nonan_maps = df_of_year_to_consider.dropna(subset=[dict_variables['x'], 
                dict_variables['y'], dict_variables['name']], how='any')
else:
    var_list = ['x']
    df_of_year_to_consider_nonan_maps = df_of_year_to_consider.dropna(subset=[dict_variables['x'], 
                dict_variables['name']], how='any')
if do_mapplots:
    # for x and y static images    
    for var_xy in var_list:
        draw_choropleth(df=df_of_year_to_consider_nonan_maps,
                            locations='Code',
                            color=dict_variables[var_xy],
                            title_text=dict_variables[var_xy] + ' in ' + str(year_to_consider),
                            file_name=dict_variables[var_xy],
                            color_continuous_scale='Viridis',
                            locationmode='ISO-3',
                            geojson=gj,
                            )
    
    # in log:
    for var_xy in var_list:
        df_of_year_to_consider_nonan_maps[dict_variables[var_xy] + '_log'] = np.log(df_of_year_to_consider_nonan_maps[dict_variables[var_xy]])
        draw_choropleth(df=df_of_year_to_consider_nonan_maps,
                            locations='Code',
                            color=dict_variables[var_xy] + '_log',
                            title_text=dict_variables[var_xy] + '_log' + ' in ' + str(year_to_consider),
                            file_name=dict_variables[var_xy]+ '_log',
                            color_continuous_scale='Viridis',
                            locationmode='ISO-3',
                            geojson=gj,
                            )
    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Animated
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if do_animated_mapplots:
    
    if dict_variables['y']:
        df_time_frame_consider_nonan_maps = df_time_frame_consider.dropna(subset=[dict_variables['x'], 
                dict_variables['y'], dict_variables['name']], how='any')
    else:
        df_time_frame_consider_nonan_maps = df_time_frame_consider.dropna(subset=[dict_variables['x'], 
                dict_variables['name']], how='any')
        
    df_time_frame_consider_nonan_maps.sort_values(by=[column_name_of_year], inplace=True)
    # for x and y
    for var_xy in var_list:
        draw_choropleth(df=df_time_frame_consider_nonan_maps,
                            locations='Code',
                            color=dict_variables[var_xy],
                            title_text=dict_variables[var_xy] + ' in ' + str(year_to_consider),
                            file_name=dict_variables[var_xy],
                            color_continuous_scale='Viridis',
                            locationmode='ISO-3',
                            geojson=gj,
                            animation_frame=column_name_of_year,
                            )
        
    # in log:
    for var_xy in var_list:
        df_time_frame_consider_nonan_maps[dict_variables[var_xy] + '_log'] = np.log(df_time_frame_consider_nonan_maps[dict_variables[var_xy]])
        draw_choropleth(df=df_time_frame_consider_nonan_maps,
                            locations='Code',
                            color=dict_variables[var_xy] + '_log',
                            title_text=dict_variables[var_xy] + '_log' + ' in ' + str(year_to_consider),
                            file_name=dict_variables[var_xy]+ '_log',
                            color_continuous_scale='Viridis',
                            locationmode='ISO-3',
                            geojson=gj,
                            animation_frame=column_name_of_year,
                            )
        
