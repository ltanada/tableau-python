# -*- coding: utf-8 -*-
"""
Created on Sat Dec 03 2022

@author: Lorenzo Tanada

https://public.tableau.com/app/profile/lorenzo.tanada/viz/SalesDashboard01-filtersmap/SalesDashboard
"""

import pandas as pd

data = pd.read_csv('sales_dashboard_01_transaction_snippet.csv', sep=';') # separator is ';'

#bring dataframe CostPerItem values into series CostPerItem
CostPerItem = data['CostPerItem']
NumberOfItemsPurchased = data['NumberOfItemsPurchased']

#this creates a calculated series
CostPerTransaction = CostPerItem * NumberOfItemsPurchased

#add new column to dataframe. both will do same thing
#data['CostPerTransaction'] = CostPerTransaction
data['CostPerTransaction'] = data['CostPerItem'] * data['NumberOfItemsPurchased']

#add new column to dataframe
data['SalesPerTransaction'] = data['SellingPricePerItem'] * data['NumberOfItemsPurchased']

#add new column to dataframe
data['ProfitePerTransaction'] = data['SalesPerTransaction'] - data['CostPerTransaction']

#add new column to dataframe
data['MarkUp'] = data['ProfitePerTransaction'] / data['CostPerTransaction']

#cleanup MarkUp since some numbers are too long like 1.1234566, round to 2 places
data['MarkUp'] = round(data['MarkUp'],2)

#cleanup date
#format to be 'Day'+'-'+'Month'+'-'+'Year'
day = data['Day'].astype(str) #this turns the Day field from number to string so can be added to other strings
year = data['Year'].astype(str) #this turns the Year field from number to string so can be added to other strings
my_date = day+'-'+data['Month']+'-'+year
data['date'] = my_date #add column to dataframe


#use split to separate ClientKeywords 
split_col = data['ClientKeywords'].str.split(',' , expand=True)

#creating new columns from the split of ClientKeywords
data['ClientAge'] = split_col[0] #adds column to data, notice column are numbers if not defined
data['ClientType'] = split_col[1]
data['LengthOfContract'] = split_col[2]

#cleanup since 1st rown ClientAge is "['Senior'"  >> need to get rid of open bracket and close bracket
data['ClientAge'] = data['ClientAge'].str.replace('[','')
data['LengthOfContract'] = data['LengthOfContract'].str.replace(']','')

#make ItemDescription lower case
data['ItemDescription'] = data['ItemDescription'].str.lower()

#merge/join files
seasons = pd.read_csv('sales_dashboard_01_season.csv', sep=';') 
data = pd.merge(data,seasons,on='Month') #creates new column in  dataframe 'data' with the col name of 'Season' from new dataframe and assign the Season value where the Month are equal

#we don't need certain columns now, so drop columns
data = data.drop('ClientKeywords', axis = 1) #this will drop ClientKeywords col
data = data.drop('Day', axis = 1) #this will drop Day col
#drop multiple columns, put them in a list format
data = data.drop(['Year','Month'], axis = 1) #this will drop Month and Year cols

#Export into CSV, uses a pandas function to_csv
data.to_csv('sales_dashboard_01_cleaned.csv', index = False) #it will export in working directory, False means it wont export the Index col, True would include Index col
 