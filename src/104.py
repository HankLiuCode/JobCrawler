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


# read excel file as config
dfWorkingArea = pd.read_excel('conf/104_config.xlsx', sheet_name='上班地點')
# create a dictionary object
workingAreaDict =  dict()
for index, row in dfWorkingArea.iterrows():
    workingAreaDict[row[0]] = row[1]
       
  
    
def getWorkingArea(workingStr):
    #print(workingStr)
    for key in workingAreaDict:
        if(workingStr.find(key)>=0):
            return workingAreaDict.get(key)            
    #print('after loop')
    return ""    

dfAppliedNumber = pd.read_excel('conf/104_config.xlsx', sheet_name='目前應徵人數')

appliedNumberDict = dict()

for index, row in dfAppliedNumber.iterrows():
    print(row[0])
    appliedNumberDict[row[0]] = row[1]

def getAppliedNumber(appliedNumberStr):
    return appliedNumberDict.get(appliedNumberStr)
#print(getWorkingArea('高雄市苓雅區中正二路175號3樓'))    

def getSalary(salaryStr):
    baseSalary = 0
    try:
        if(salaryStr.find('月薪')>=0):
            # get position of ~
            endPosition = salaryStr.find('~')
            baseSalaryStr = salaryStr[salaryStr.find('月薪')+3:endPosition]
            baseSalaryStr = baseSalaryStr.replace(',','')
            baseSalaryStr = baseSalaryStr.replace('元','')
            baseSalary = int(baseSalaryStr)
        elif (salaryStr.find('面議')>=0) :
            baseSalary = 40000
    except:
        print(salaryStr)
    return baseSalary
# 抓需求人數
def getRequiredEmp(requiredStr):
    requiredNum = 0
    if(requiredStr.find('至')>=0):
        requiredNum = int(requiredStr[0:requiredStr.find('至')])
    elif(requiredStr.find('人')>=0):
        requiredNum = int(requiredStr[0:requiredStr.find('人')-1])
        #.strip()
    elif(requiredStr.find('不限')>=0):  
        return '不限'
    
    if(requiredNum >= 10):
        return '不限'
    else:
        return requiredNum
    
#抓學歷要求
def getRequiredDegree(requiredDegreeStr):
    if(requiredDegreeStr.find('高中')>=0):
        return '高中'
    elif(requiredDegreeStr.find('專科')>=0):
        return '專科'
    elif(requiredDegreeStr.find('大學')>=0):
        return '大學'
    elif(requiredDegreeStr.find('碩士')>=0):
        return '碩士'
    elif(requiredDegreeStr.find('博士')>=0):
        return '博士'
    else:
        return '不拘'

# 英文要求
def getLanguageData(languageStr):
    if(languageStr.find('英文')>=0 and
       languageStr.find('讀 /精通')>=0 and
       languageStr.find('寫 /精通')>=0 ):
        return '英文 讀寫/精通'
    else:
        return 'NA'

df['工作區域'] = list(map(getWorkingArea,list(df['上班地點'])))

df['應徵人數'] = list(map(getAppliedNumber,list(df['目前應徵人數'])))

df['薪水'] = list(map(getSalary,list(df['工作待遇'])))

df['需求數量'] = list(map(getRequiredEmp,list(df['需求人數'])))

df['需求學歷'] = list(map(getRequiredDegree,list(df['學歷要求'])))

df['需求語言'] = list(map(getLanguageData,list(df['語文條件'])))

'''
    
type(df[['上班地點']])

for data in workingAreaList:
    print(data)


df.columns
df[['目前應徵人數']]

df_required = df.groupby(['語文條件']).size()

df_required.index
for row in df_required.index:
    print(row)

df[['工作待遇']]

df.groupby(['工作待遇']).size()

salary = '月薪 37,000~70,000元'

# contains '月薪'
if(salary.find('月薪')>=0):
    # get position of ~
    endPosition = salary.find('~')
    baseSalaryStr = salary[salary.find('月薪')+3:endPosition]
    baseSalaryStr = baseSalaryStr.replace(',','')
    baseSalary = int(baseSalaryStr)
elif (salary.find('面議')>=0) :
    baseSalary = 40000

df[['上班地點']]

df.groupby(['上班地點']).size()

'''

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
    record = record.upper();
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
# Initializing Dictionary
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
