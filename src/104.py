# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 10:04:14 2018

@author: A6782
"""

'''
pip install --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org 
'''

import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import jieba
import re

from sklearn import tree
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from collections import Counter

os.chdir('D:\\python\\HR_104')
# initial the user dictionary
jieba.load_userdict('conf/userdict.txt')

stopWords = ''
with open('conf/stopword.txt', encoding="utf8") as f:
    stopWords = [line.strip() for line in f.readlines()] 

def getJiebaResult(str):
    new_words = list();

    for word in jieba.cut(str):
        new_words.append(word)
        # clean words whos length<2 and with only numbers and characters
        new_words = [w for w in new_words if len(w)>1 
         and not re.match('^[f-z|F-Z|0-9|.]*$',w)]
        
        # clean stop_words
        new_words = [w for w in new_words if w not in stopWords]
        #print(new_words)
    return new_words 


def replaceData(strData):
    strData = strData.replace("ORACLE1","ORACLE")
    strData = strData.replace("JAVA1","JAVA")
    strData = strData.replace("CSS3","CSS")
    strData = strData.replace("DATABASES","DATABASE")
    strData = strData.replace("DB2.1","DB2")
    strData = strData.replace("DBA1","DBA")
    strData = strData.replace("ANGULAR2",'ANGULARJS')
    strData = strData.replace("ANGULARJS3",'ANGULARJS')
    strData = strData.replace('ANALYTIC','ANALYTICS')
    strData = strData.replace('ANALYTICAL','ANALYTICS')
    strData = strData.replace('INFORMATICA1','INFORMATICA')
    strData = strData.replace('J2EE1','J2EE')
    strData = strData.replace('JASON','JSON')
    strData = strData.replace('JAVA5','JAVA')
    strData = strData.replace('JAVASCRIP','JAVASCRIPT')
    strData = strData.replace('JAVASCRIPT1','JAVASCRIPT')
    strData = strData.replace('JAVASCRIPT2','JAVASCRIPT')
    strData = strData.replace('JQUERY1','JQUERY')
    strData = strData.replace('JQUERY4','JQUERY')
    strData = strData.replace('MICROSERVICES','MICROSERVICE')
    strData = strData.replace('MYBATIS6','MYBATIS')
    strData = strData.replace('NET1','NET')
    strData = strData.replace('NET1.3','NET')
    strData = strData.replace('ORACLE3','ORACLE')
    strData = strData.replace('PROCEDURES','PROCEDURE')
    strData = strData.replace('SAS1','SAS')
    strData = strData.replace('SASS','SPSS')
    strData = strData.replace('VBSCRIPT1','VBSCRIPT')
    strData = strData.replace('','')
    
    
    return strData


# os.chdir('c:\\Users\\A6782\\Desktop\\Demo')

# read the data from excel file
#df = pd.read_excel('Data/jobs104_20190620.xlsx', sheetname='Sheet1')
df1 = pd.read_excel('Data/jobs104_20190624_2833.xlsx', sheet_name='Sheet1')
df2 = pd.read_excel('Data/jobs104_20190624_5846.xlsx', sheet_name='Sheet1')
df3 = pd.read_excel('Data/jobs104_20190624_5874.xlsx', sheet_name='Sheet1')

df = pd.concat([df1,df2,df3])

df = df.reset_index(drop=True)

df['other_info'] = ''
df['cut_meta'] = ''

# create a word list 
word_list = []

#print(df.iloc[2]['工作名稱']+df.iloc[2]['其他條件']+df.iloc[2]['工作內容'])


for i in range(0,len(df.index)): #len(df.index)
    df.at[i,'other_info'] = str(df.iloc[i]['工作名稱'])+str(df.iloc[i]['其他條件'])+str(df.iloc[i]['工作內容'])
    #print(str(df.iloc[i]['工作名稱'])+str(df.iloc[i]['其他條件'])+str(df.iloc[i]['工作內容']) )
    #print(df.iloc[i]['other_info'])
    
    record = df.iloc[i]['other_info']
    record = record.upper()
    record = replaceData(record)
    str_record = str(record)
    cut_data = getJiebaResult(str_record)
    
    # print(cut_data)
    for word in cut_data:
        word = word.upper()
       #  print(word)
        word_list.append(word)
    
    # combind the words
    new_record = "/".join(cut_data)
    df.at[i,'cut_meta'] = new_record
    
    # print(cut_data)
    for word in cut_data:
        word_list.append(word)
    

# word count
Counter(word_list).most_common()
d = {}

# counting number of times each word comes up in list of words (in dictionary)
for word in word_list: 
    d[word] = d.get(word, 0) + 1

#reverse the key and values so they can be sorted using tuples.  
word_freq = []
for key, value in d.items():
    word_freq.append((value, key))
    
word_freq.sort(reverse=True) 
print(word_freq)

word_freq_df = pd.DataFrame(word_freq)
writer = pd.ExcelWriter('D:\\python\\HR_104\\job_104_result_cathay_20190801.xlsx')
word_freq_df.to_excel(writer,'word_freq')
df.to_excel(writer,'source')
