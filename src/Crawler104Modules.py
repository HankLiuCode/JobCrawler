import pandas
import jieba
import jieba.analyse
import re
import os
from settings import configPath,configDirectory,workingAreaSheet,appliedNumberSheet

class Parser104:
    
    def __init__ (self,configPath,appliedNumberSheet,workingAreaSheet):
        self.appliedNumberDict = self.__getAppliedNumberDict(configPath,appliedNumberSheet)
        self.workingAreaDict = self.__getWorkingAreaDict(configPath,workingAreaSheet)
        
    def parse104Dataframe(self,df):
        stopwords = self.__getStopwords()
        jieba.load_userdict(os.path.join(configDirectory,'userdict.txt'))
        df['合併欄位'] = ''
        df['斷詞分析'] = ''
        for i in df.index:
            df.at[i,'應徵人數'] = self.__getAppliedNumber(df.at[i,'應徵人數'])
            df.at[i,'上班地點'] = self.__getWorkingArea(df.at[i,'上班地點'])
            df.at[i,'工作待遇'] = self.__getSalary(df.at[i,'工作待遇'])
            df.at[i,'需求人數'] = self.__getRequiredEmp(df.at[i,'需求人數'])
            df.at[i,'學歷要求'] = self.__getRequiredDegree(df.at[i,'學歷要求'])
            df.at[i,'語文條件'] = self.__getLanguageData(df.at[i,'語文條件'])
            df.at[i,'工作經歷'] = self.__getJobExperience(df.at[i,'工作經歷'])

            df.at[i,'合併欄位'] = (str(df.at[i,'工作名稱']) + str(df.at[i,'工作內容']) + str(df.at[i,'其他條件'])).lower()
            wordsWanted = []
            for word in jieba.cut(df.at[i,'合併欄位']):
                word = self.__cleanJiebaText(word)
                if word not in stopwords:
                    wordsWanted.append(word)
            df.at[i,'斷詞分析'] = "、".join(wordsWanted)
            #df.at[i,'關鍵字'] = jieba.analyse.extract_tags(df.at[i,'合併欄位'],topK=10)
        return df


    def job_eng_chi_mapping(self):
        #Chinese to English Dict
        CEDict = {
            '工作編號':'jobno',
            '工作名稱':'jobname', 
            '公司':'company', 
            '應徵人數':'appliedNumber',
            '需求人數':'required',
            '工作待遇':'salary',
            '職務類別':'jobCategory',
            '上班地點':'workingAddress',
            '工作性質':'nature',
            '管理責任':'manage',
            '出差外派':'travel',
            '工作經歷':'experience',
            '學歷要求':'education',
            '科系要求':'department',
            '語文條件':'language',
            '擅長工具':'tool',
            '具備證照':'certificates',
            '工作技能':'skill',
            '其他條件':'otherRequirements',
            '工作內容':'jobContent',
            '合併欄位':'combinedColumns',
            '斷詞分析':'wordAnalysis',
            '工作連結':'joblink',
            
            #columns that are not important
            #'聯絡人':'contact',
            #'上班時段':'working',
            #'休假制度':'vacation',
            #'可上班日':'available',
            #'接受身份':'identity', 
            #'雇用類型':'employType',
            #'代徵企業':'hunterCompany',
            #'應徵回復':'reply',
            #'其他':'others',
        }
        return CEDict

    def __getStopwords(self):
        stopwords = []
        with open('../conf/stopword.txt', encoding="utf8") as f:
                stopwords = [self.__cleanJiebaText(line) for line in f.readlines()]
        return stopwords

    def __cleanJiebaText(self,uncleanStr):
        uncleanStr = re.sub(r"\d+"," ",uncleanStr)
        return uncleanStr.replace(' ','').replace('\n','').replace('\r','').replace('\t','')

    def __getAppliedNumberDict(self,filepath,sheet):
        appliedNumberDict = {}
        dfAppliedNumber = pandas.read_excel(filepath, sheet)
        for index,row in dfAppliedNumber.iterrows():
            appliedNumberDict[row[0]] = row[1]
        #print(appliedNumberDict)
        return appliedNumberDict
        
    def __getWorkingAreaDict(self,filepath,sheet):
        workingAreaDict = {}
        dfWorkingArea = pandas.read_excel(filepath,sheet)
        for index,row in dfWorkingArea.iterrows():
            workingAreaDict[row[0]] = row[1]
        #print(workingAreaDict)
        return workingAreaDict

    def __getAppliedNumber(self,appliedNumberStr):
        return self.appliedNumberDict.get(appliedNumberStr)

    def __getJobExperience(self,jobExpStr):
        jobExpStr = str(jobExpStr)
        if(jobExpStr.find('年')>=0):
            jobExpStr = jobExpStr[0:jobExpStr.find('年')]
        elif(jobExpStr.find('不拘')>=0):
            jobExpStr = "0"
        
        jobExp = 0
        try:
            jobExp = int(jobExpStr)
        except:
            print("Error in Crawler104Modules.__getJobExperience: {}".format(jobExpStr))
            return jobExpStr
        return jobExp

    def __getWorkingArea(self,workingStr):
        retVal = ""
        workingStr = str(workingStr)
        try:
            for key in self.workingAreaDict:
                if(workingStr.find(key)>=0):
                    retVal = self.workingAreaDict[key]
        except:
            print("Error in Crawler104Modules.__getWorkingArea: {}".format(workingStr))
            return workingStr
        return retVal     
    # input = "月薪 28,000~40,000元"  output = 28000
    def __getSalary(self,salaryStr):
        startIndex = 999
        endIndex = 999
        salaryStr = str(salaryStr)
        salaryStr = salaryStr.replace(' ','').replace(',','')
        if(salaryStr.find('月薪')>=0):
            startIndex = salaryStr.find('薪')+1
            endIndex = salaryStr.find('~')
            if (endIndex == -1):
                endIndex = salaryStr.find('元')
            salaryStr = salaryStr[startIndex:endIndex]
                
        elif(salaryStr.find('時薪')>=0):
            startIndex = salaryStr.find('薪')+1
            endIndex = salaryStr.find('~')
            if (endIndex == -1):
                endIndex = salaryStr.find('元')
            salaryStr = salaryStr[startIndex:endIndex]

        elif(salaryStr.find('年薪')>=0):
            startIndex = salaryStr.find('薪')+1
            endIndex = salaryStr.find('~')
            if (endIndex == -1):
                endIndex = salaryStr.find('元')
            salaryStr = salaryStr[startIndex:endIndex]
        
        elif (salaryStr.find('面議')>=0) :
            salaryStr = "40000"
        baseSalary = 0    
        try:
            baseSalary = int(salaryStr)
        except:
            print("Error in Crawler104Modules.__getSalary: {}".format(salaryStr))
            return salaryStr

        return baseSalary
    # input  = "1至2人" output = 1
    def __getRequiredEmp(self,requiredStr):
        requiredStr = str(requiredStr)
        if(requiredStr.find('人')>=0):
            requiredStr = requiredStr[0: min(requiredStr.find('人'),requiredStr.find('至'))] 
        elif(requiredStr.find('不限')>=0):
            requiredStr = '不拘'
        return requiredStr
    
    # input  = "專科、大學、碩士", "高中以上" output = "專科" , "高中"
    def __getRequiredDegree(self,requiredDegreeStr):
        requiredDegreeStr = str(requiredDegreeStr)
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
    def __getLanguageData(self,languageStr):
        languageStr = str(languageStr)
        if(languageStr.find('英文')>=0 and
           languageStr.find('讀 /精通')>=0 and
           languageStr.find('寫 /精通')>=0 ):
            return '英文 讀寫精通'
            #return True
        else:
            return 'NA'
            #return False
    


    
