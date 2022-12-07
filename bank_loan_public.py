# -*- coding: utf-8 -*-
"""
Created on Mon Dec 5, 2022

@author: Lorenzo Tanada
"""

import json
import pandas as pd
import numpy as np

#method 1 to read json data.
#json_file = open('bank_loan_snippet_json.json')
#data = json.load(json_file)

#method 2 to read json data.
with open('bank_loan_snippet_json.json') as json_file:
    data = json.load(json_file)

#transform the list/dictionary of 'data' into new dataframe using pandas DataFrame function
loandata = pd.DataFrame(data)

#need numpy to calculate the exponent for the log annual inc
income = np.exp(loandata['log.annual.inc'])
#add annualincome to loandata
loandata['annualincome'] = income

#apply for loops to loandata to categorize by fico score
length=len(loandata) #number of rows of loandata dataframe
ficocat=[] #new list

for x in range(0,length):
    category=loandata['fico'][x]
    if category >= 300 and category < 400:
        cat='Very Poor'
    elif category >= 400 and category < 600:
        cat='Poor'
    elif category >= 600 and category < 660:
        cat='Fair'
    elif category >= 660 and category < 700:
        cat='Good'
    elif category >= 700:
        cat='Excellent'
    else:
        cat='Unknown'
    ficocat.append(cat) #append adds current cat value to ficocat list

#turn ficocat list into a Series
ficocat=pd.Series(ficocat)
#we add the ficocat series data as new column in loandata dataframe
loandata['fico.category']=ficocat

#add column int.rate.type to loandata, if > 0.12 then 'High', if <= 0.12 then 'Low'
loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'

# writing DataFrame loandata to csv
loandata.to_csv('bank_loan_cleaned.csv', index=True) # since no unique id, the keep the index by having True value

print('done')



