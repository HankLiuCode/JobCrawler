import numpy
import pandas
import os
import datetime

class Parser104:
    
    def __init__(self,configPath,appliedNumberSheet,workingAreaSheet):
        self.appliedNumberDict = self.__getAppliedNumberDict(configPath,appliedNumberSheet)
        self.workingAreaDict = self.__getWorkingAreaDict(configPath,workingAreaSheet)
            
    def parse104Excel(self,filepath,sheet):
        df = pandas.read_excel(io=filepath,sheet_name=sheet)
        for i in df.index:
            df.at[i,'應徵人數'] = self.__getAppliedNumber(df.at[i,'應徵人數'])
            df.at[i,'上班地點'] = self.__getWorkingArea(df.at[i,'上班地點'])
            df.at[i,'工作待遇'] = self.__getSalary(df.at[i,'工作待遇'])
            df.at[i,'需求人數'] = self.__getRequiredEmp(df.at[i,'需求人數'])
            df.at[i,'學歷要求'] = self.__getRequiredDegree(df.at[i,'學歷要求'])
            df.at[i,'語文條件'] = self.__getLanguageData(df.at[i,'語文條件'])
            
        dirname = os.path.dirname(filepath)
        filename = os.path.splitext(filepath)[0] + "_parsed.xlsx"
        df.to_excel(os.path.join(dirname,filename))
        print("finished parsing 104excel at {}...".format(os.path.join(dirname,filename)))
        

    def parse104Dataframe(self,df):
        for i in df.index:
            df.at[i,'appliedNumber'] = self.__getAppliedNumber(df.at[i,'view_count'])
            df.at[i,'addr'] = self.__getWorkingArea(df.at[i,'addr'])
            df.at[i,'salary'] = self.__getSalary(df.at[i,'salary'])
            df.at[i,'required'] = self.__getRequiredEmp(df.at[i,'required'])
            df.at[i,'education'] = self.__getRequiredDegree(df.at[i,'education'])
            df.at[i,'language'] = self.__getLanguageData(df.at[i,'language'])
            #print(df.at[i,'view_count'])
            #print(df.at[i,'address'])
            #print(df.at[i,'salary'])
            #print(df.at[i,'required'])
            #print(df.at[i,'education'])
            #print(df.at[i,'language'])
        return df
    
    def getChinesetoEnglishDict(self):
        CtoEDict = {
            '應徵人數':'appliedNumber',
            '職務類別':'jobCategory',
            '工作待遇':'salary',
            '工作性質':'nature',
            '上班地點':'workingAddress',
            '管理責任':'manage',
            '出差外派':'travel',
            '上班時段':'working',
            '休假制度':'vacation',
            '可上班日':'available',
            '需求人數':'required',
            '接受身分':'identity',
            '工作經歷':'experience',
            '學歷要求':'education',
            '科系要求':'department',
            '語文條件':'language',
            '擅長工具':'tool',
            '工作技能':'skill',
            '其他條件':'other',
            '聯絡人':'contact',
            '工作編號':'jobno',
            '工作名稱':'jobname', 
            '公司':'company', 
            '工作連結':'joblink',
            '工作內容':'jobContent',
        }
        return CtoEDict

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

    #bug!
    def __getWorkingArea(self,workingStr):
        retVal = ""
        for key in self.workingAreaDict:
            if(workingStr.find(key)>=0):
                retVal = self.workingAreaDict[key]
        return retVal     

    #抓薪水
    # input  = "月薪 28,000~40,000元"
    # output = 28000
    #bug!
    def __getSalary(self,salaryStr):
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
    # input  = "1至2人"
    # output = 1
    def __getRequiredEmp(self,requiredStr):
        try:
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
        except:
            print(requiredStr)


    #抓學歷要求
    # input  = "專科、大學、碩士", "高中以上"
    # output = "專科" , "高中"
    def __getRequiredDegree(self,requiredDegreeStr):
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
        if(languageStr.find('英文')>=0 and
           languageStr.find('讀 /精通')>=0 and
           languageStr.find('寫 /精通')>=0 ):
            return '英文 讀寫/精通'
        else:
            return 'NA'







class User104:
    def paradef(self):
        return ""
        #### 參數解釋 ####
        # ro:         0(全部),1(全職),2(兼職),3(高階),4(派遣),5(接案),6(家教)
        # order:     11(依日期排序), 4(依學歷排序)
        # asc:       1(ascending=true), 0(ascending=false)
        # mode:      s(摘要),l(列表)
        # page:      <int>(第幾頁)
        # jobsource: 
        # example: 'https://www.104.com.tw/jobs/search/?ro=1&order=11&asc=0&mode=s&jobsource=indexpoc2018&page=1

        #### 額外參數 ####
        # 參數使用範例:  多於一個參數用 % 隔開
        #              url = url + &jobcat=2007001000%2007002000%2007000000
        #              url = url + &area=6001001000%2C6001002000
        #              url = url + '&indcat=1004000000'
        #              url = url + &keyword=國泰人壽
        # ro 工作型態        
        # jobcat 職務類別
        # area 地區
        # indcat 公司產業
        # keyword 額外關鍵字搜尋

    def __init__(self,keywordList,singleRoList,areaList,jobcatList,indcatList):
        self.roDict = self.get_ro_dict()
        self.areaDict = self.get_area_dict()
        self.jobcatDict = self.get_jobcat_dict()
        self.indcatDict = self.get_indcat_dict()
        
        self.query= self.generate_query(
                keywordList,
                [self.roDict[ro] for ro in singleRoList],   
                [self.areaDict[area] for area in areaList],
                [self.jobcatDict[jobcat] for jobcat in jobcatList],
                [self.indcatDict[indcat] for indcat in indcatList],
            )
    def get_ro_dict(self):
        ro_dict = {
            "":"",
            "全部":"0","全職":"1","兼職":"2","高階":"3","派遣":4,"接案":5,"家教":6
        }
        return ro_dict
    def get_area_dict(self):
        area_dict = {
            "":"",
            "台北市" : "6001001000", "新北市" : "2C6001002000" , "桃園市" : "6001005000"
        }
        return area_dict
    def get_jobcat_dict(self):
        jobcat_dict = {
            "":"",
            "資訊軟體系統類" : "2007000000", "軟體／工程類人員" : "2007001000" , "MIS程式設計師" : "2007002000" ,
            "金融專業相關類人員" : "2003002000", 
            "國外業務人員":"2005003005",
        }
        return jobcat_dict
    def get_indcat_dict(self):
        indcat_dict = {
            "":"",
            "金融投顧及保險業" : "1004000000", "投資理財相關業" : "1004002000" , "金融機構及其相關業" : "1004001000" 
        }
        return indcat_dict
    
    
    def get_test_url(self):
        url = self.generate_query( 
            keywordList=["新光銀行","行銷"],
            singleRoList=['0'],
            areaList=["6001001000","2C6001002000"],
            jobcatList=["2007000000","2003002000"],
            indcatList=["1004000000","1004002000"]
        )
        return url

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
    
    def get_filename(self,name):
        filename = "jobs104_"+str(datetime.datetime.now().date()).replace("-","")+"_" + name + ".xlsx"
        return filename

def test_parse104():
    filepath = '../Data/jobs104_20190808_myfile.xlsx'
    sheet = "Sheet1"
    configPath = '../conf/104_config.xlsx'
    workingAreaSheet = '上班地點'
    appliedNumberSheet= '目前應徵人數'
    parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
    parser104.parse104Excel(filepath,sheet)

def test_user104():
    singleRoTestList = ['兼職']
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
    #print(u.get_filename("myfile"))
    print(user.get_query())

if __name__ == '__main__':
    test_user104()
    