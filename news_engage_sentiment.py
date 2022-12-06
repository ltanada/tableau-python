# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 2022

@author: Lorenzo Tanada
https://public.tableau.com/app/profile/lorenzo.tanada/viz/NewsEngagementSentimentAnalysis/NewsDashboard
"""

# pandas function to read excel files
import pandas as pd

# VADER Sentiment Analysis. VADER (Valence Aware Dictionary and Sentiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media, and works well on texts from other domains. Need to install it first.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

# reading excel or xlsx files
data = pd.read_excel('news_articles_snippet.xlsx')
# you may receive error "ImportError: Missing optional dependency 'openpyxl'.  Use pip or conda to install openpyxl."


# Keyword Flag function. add try due to the float error
def keywordflag(keyword):
    length=len(data) # gets number of rows of datafile
    keyword_flag=[] # define this array/list
    # for loop to iterate though each row
    for x in range(0,length):
        text_to_check=data['title'][x]+' '+data['description'][x]
        try:  
            if keyword.lower() in text_to_check.lower(): # use lower to make it case insensitive
                flag=1
            else:
                flag=0
        except:
            flag=0
        keyword_flag.append(flag)
    return keyword_flag
    
# run the function to flag articles with keyword "Brexit"
keywordflag=keywordflag('Brexit')

#creating a new column keyword_flag in the data datafram
data['keyword_flag'] = pd.Series(keywordflag)


# adding a for loop to extract sentiment per title
# define variables
title_neg_sentiment=[]
title_pos_sentiment=[]
title_neu_sentiment=[]

# run sentiment on all titles with "try" to handle exception for the float/nan error for title
length=len(data)
for x in range(0,length):
    try:
        text=data['title'][x]
        sent_int=SentimentIntensityAnalyzer() #need to initialize Analyzer
        sent=sent_int.polarity_scores(text) 
        neg=sent['neg']
        pos=sent['pos']
        neu=sent['neu']
    except:
        neg=0
        pos=0
        neu=0
    title_neg_sentiment.append(neg)
    title_pos_sentiment.append(pos)
    title_neu_sentiment.append(neu)

# convert the 3 lists to series
title_neg_sentiment=pd.Series(title_neg_sentiment)
title_pos_sentiment=pd.Series(title_pos_sentiment)
title_neu_sentiment=pd.Series(title_neu_sentiment)

# add the 3 columns to the dataframe data
data['title_neg_sentiment']=title_neg_sentiment
data['title_pos_sentiment']=title_pos_sentiment
data['title_neu_sentiment']=title_neu_sentiment

# write dataframe data to .xlsx
data.to_excel('news_engage_sentiment_clean.xlsx',sheet_name='newsdata',index=False) #no need for index since there is an article id

print('done')


