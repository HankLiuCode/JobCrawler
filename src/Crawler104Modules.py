import numpy
import pandas
import jieba
import re
import os
import datetime
from settings import configPath,workingAreaSheet,appliedNumberSheet

class Parser104:
    
    def __init__ (self,configPath,appliedNumberSheet,workingAreaSheet):
        self.appliedNumberDict = self.__getAppliedNumberDict(configPath,appliedNumberSheet)
        self.workingAreaDict = self.__getWorkingAreaDict(configPath,workingAreaSheet)
    

    def parse104Excel(self,filepath,sheet="Sheet1"):
        df = pandas.read_excel(io=filepath,sheet_name=sheet)
        df = self.parse104Dataframe(df)
        dirname = os.path.dirname(filepath)
        filename = os.path.splitext(filepath)[0] + "_parsed.xlsx"
        df.to_excel(os.path.join(dirname,filename))
        print("finished parsing 104excel at {}...".format(filepath))
        
    def parse104Dataframe(self,df):
        df['合併欄位'] = ''
        df['斷詞分析'] = ''
        for i in df.index:
            df.at[i,'應徵人數'] = self.__getAppliedNumber(df.at[i,'應徵人數'])
            df.at[i,'上班地點'] = self.__getWorkingArea(df.at[i,'上班地點'])
            df.at[i,'工作待遇'] = self.__getSalary(df.at[i,'工作待遇'])
            df.at[i,'需求人數'] = self.__getRequiredEmp(df.at[i,'需求人數'])
            df.at[i,'學歷要求'] = self.__getRequiredDegree(df.at[i,'學歷要求'])
            df.at[i,'語文條件'] = self.__getLanguageData(df.at[i,'語文條件'])
            df.at[i,'管理責任'] = self.__getManage(df.at[i,'管理責任'])
            df.at[i,'工作經歷'] = self.__getJobExperience(df.at[i,'工作經歷'])
            df.at[i,'職務類別'] = self.__getJobCategory(df.at[i,'職務類別'])

            df.at[i,'合併欄位'] = str(df.at[i,'工作名稱']) + str(df.at[i,'工作內容']) + str(df.at[i,'其他條件'])
            df.at[i,'合併欄位'] = df.at[i,'合併欄位'].upper()
            with open('../conf/stopword.txt', encoding="utf8") as f:
                stopwords = [self.__cleanJiebaText(line) for line in f.readlines()]
                df.at[i,'斷詞分析'] = "、".join( [word for word in jieba.cut(self.__cleanJiebaText(df.at[i,'合併欄位']), cut_all=False) if word not in stopwords] )
        df = self.arrangeDataFrameOrder(df)
        return df

    def arrangeDataFrameOrder(self,df):
        jobmapping = self.jobMappingDict()
        df = df[[k for k in jobmapping]]
        #rename columns from chinese to english
        #df = df.rename(columns=jobmapping)
        return df

    def jobMappingDict(self):
        #Chinese to English Dict
        CEDict = {
            '工作編號':'jobno',
            '工作名稱':'jobname', 
            '公司':'company', 
            '應徵人數':'appliedNumber',
            '需求人數':'required',
            '工作待遇':'salary',
            '職務類別':'jobCategory',
            '擅長工具':'tool',
            '上班地點':'workingAddress',
            '工作性質':'nature',
            '管理責任':'manage',
            '出差外派':'travel',
            '工作經歷':'experience',
            '學歷要求':'education',
            '科系要求':'department',
            '語文條件':'language',
            '工作技能':'skill',
            '其他條件':'other',
            '工作內容':'jobContent',
            '合併欄位':'combinedColumns',
            '斷詞分析':'wordAnalysis',
            '工作連結':'joblink',
            '聯絡人':'contact',
            '上班時段':'working',
            '休假制度':'vacation',
            '可上班日':'available',
            '接受身份':'identity', 
        }
        return CEDict

    def __cleanJiebaText(self,uncleanStr):
        uncleanStr = re.sub(r"\d+"," ",uncleanStr)
        return uncleanStr.replace(' ','').replace('\n','').replace('\r','')

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

    def __getJobCategory(self,jobCateStr):
        jobCateStr = str(jobCateStr)
        return jobCateStr.replace(" ",'').replace("認識「」職務詳細職類分析(工作內容、薪資分布..)更多相關工作","")

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
        return jobExp
        
    def __getManage(self,manageStr):
        isManage = False
        manageStr = str(manageStr)
        if(manageStr.find('不需負擔')>=0):
            isManage = False
        else:
            isManage = True
        return isManage

    #bug!
    def __getWorkingArea(self,workingStr):
        retVal = ""
        workingStr = str(workingStr)
        try:
            for key in self.workingAreaDict:
                if(workingStr.find(key)>=0):
                    retVal = self.workingAreaDict[key]
        except:
            print("Error in Crawler104Modules.__getWorkingArea: {}".format(workingStr))
        return retVal     

    #抓薪水
    # input  = "月薪 28,000~40,000元"
    # output = 28000
    #bug!
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
        return baseSalary



    # 抓需求人數
    # input  = "1至2人"
    # output = 1
    def __getRequiredEmp(self,requiredStr):
        requiredStr = str(requiredStr)
        if(requiredStr.find('人')>=0):
            requiredStr = requiredStr[0: min(requiredStr.find('人'),requiredStr.find('至'))] 
        elif(requiredStr.find('不限')>=0):
            requiredStr = '999'

        requiredNum = 0
        try:
            requiredNum = int(requiredStr)
        except:
            print("Error in Crawler104Modules.__getRequiredEmp: {}".format(requiredStr))
        return requiredNum
        
    #抓學歷要求
    # input  = "專科、大學、碩士", "高中以上"
    # output = "專科" , "高中"
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
            return '英文 讀寫/精通'
        else:
            return 'NA'

 

class URLMaker104:
    def paradef(self):
        return ""
        #### 參數解釋 ####
        # ro:         0(全部),1(全職),2(兼職),3(高階),4(派遣),5(接案),6(家教)
        # order:     11(依日期排序), 4(依學歷排序), asc: 1(ascending=true), 0(ascending=false), mode: s(摘要),l(列表)
        # page:      <int>(第幾頁)
        # jobsource: 
        # example: 'https://www.104.com.tw/jobs/search/?ro=1&order=11&asc=0&mode=s&jobsource=indexpoc2018&page=1

        #### 額外參數 ####
        # 參數使用範例:  多於一個參數用 % 隔開
        #              url = url + &<PARAMETER>=2007001000%2007002000%2007000000
        # ro 工作型態        
        # jobcat 職務類別
        # area 地區
        # indcat 公司產業
        # keyword 額外關鍵字搜尋

    def __init__(self,keywordList,singleRoList,areaList,jobcatList,indcatList):
        self.roDict = self.ro_dict()
        self.areaDict = self.area_dict()
        self.jobcatDict = self.jobcat_dict()
        self.indcatDict = self.indcat_dict()
        
        self.query= self.generate_query(
                keywordList,
                [self.roDict[ro] for ro in singleRoList],   
                [self.areaDict[area] for area in areaList],
                [self.jobcatDict[jobcat] for jobcat in jobcatList],
                [self.indcatDict[indcat] for indcat in indcatList],
            )
    def ro_dict(self):
        ro_dict = {"":"","全部":"0","全職":"1","兼職":"2","高階":"3","派遣":4,"接案":5,"家教":6 }
        return ro_dict
    def area_dict(self):
        area_dict = {
            "":"",
            "台北市" : "6001001000", "新北市" : "2C6001002000" , "桃園市" : "6001005000",
            "基隆市" : "6001004000", "台中市" : "6001008000"
        }
        return area_dict
    def jobcat_dict(self):
        jobcat_dict = {
            "":"",
            "資訊軟體系統類" : "2007000000", "軟體／工程類人員" : "2007001000" , "MIS程式設計師" : "2007002000" ,
            "財會/金融專業類":"2003000000","金融專業相關類人員" : "2003002000", "財務/會計/稅務類" : "2003001000", 
            "國外業務人員":"2005003005",
        }
        return jobcat_dict
    def indcat_dict(self):
        indcat_dict = {
            "":"",
            "金融投顧及保險業" : "1004000000", "投資理財相關業" : "1004002000" , "金融機構及其相關業" : "1004001000", 
        }
        return indcat_dict

    def generate_query(self,keywordList,singleRoList,areaList,jobcatList,indcatList):
        fullurl = 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}'
        fullurl +=self.generate_query_segment("ro",singleRoList,False)
        fullurl += self.generate_query_segment("keyword",keywordList,False)
        fullurl += self.generate_query_segment("area",areaList,False)
        fullurl += self.generate_query_segment("jobcat",jobcatList,False)
        fullurl += self.generate_query_segment("indcat",indcatList,False)
        return fullurl

    def generate_query_segment(self,parameterName,parameterList,isFirstParameter):
        url_segment = ""
        if(not isFirstParameter):
            url_segment += "&" 
        url_segment += parameterName + "="
        
        for i in range(len(parameterList)):
            url_segment = url_segment + parameterList[i]
            if i < len(parameterList) - 1:
                url_segment = url_segment + "%"

        return url_segment

    def get_query(self):
        return self.query
    

def test_parse104_excel():
    filepath = '../Data/test.xlsx'
    parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
    parser104.parse104Excel(filepath)

def test_parse104_dataframe(user):
    testdf = pandas.read_excel('../Data/test.xlsx')
    parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
    parsed_df = parser104.parse104Dataframe(testdf)
    parsed_df.to_excel(user.get_filename('test_parsed'))

if __name__ == "__main__":
    singleRoTestList = ['全部']
    keywordTestList = ["新光","銀行"]
    areaTestList = ["台北市"]
    jobcatTestList = ["資訊軟體系統類"]
    indcatTestList = ["金融投顧及保險業"]
    user = User104(
        keywordList=keywordTestList,
        singleRoList=singleRoTestList,
        areaList=areaTestList,
        jobcatList=jobcatTestList,
        indcatList=indcatTestList)
    print(user.get_query())

    