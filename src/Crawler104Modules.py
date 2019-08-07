import numpy
import pandas
import os

class Parser104:
    
    def __init__(self,configPath,appliedNumberSheet,workingAreaSheet):
        self.appliedNumberDict = self.getAppliedNumberDict(configPath,appliedNumberSheet)
        self.workingAreaDict = self.getWorkingAreaDict(configPath,workingAreaSheet)
        
    def getAppliedNumberDict(self,filepath,sheet):
        appliedNumberDict = {}
        dfAppliedNumber = pandas.read_excel(filepath, sheet)
        for index,row in dfAppliedNumber.iterrows():
            appliedNumberDict[row[0]] = row[1]
        #print(appliedNumberDict)
        return appliedNumberDict
        
    
    def getWorkingAreaDict(self,filepath,sheet):
        workingAreaDict = {}
        dfWorkingArea = pandas.read_excel(filepath,sheet)
        for index,row in dfWorkingArea.iterrows():
            workingAreaDict[row[0]] = row[1]
        #print(workingAreaDict)
        return workingAreaDict
            
    def parse104Excel(self,filepath,sheet):
        df = pandas.read_excel(io=filepath,sheet_name=sheet)
        for i in df.index:
            df.at[i,'目前應徵人數'] = self.getAppliedNumber(df.at[i,'目前應徵人數'])
            df.at[i,'上班地點'] = self.getWorkingArea(df.at[i,'上班地點'])
            df.at[i,'工作待遇'] = self.getSalary(df.at[i,'工作待遇'])
            df.at[i,'需求人數'] = self.getRequiredEmp(df.at[i,'需求人數'])
            df.at[i,'學歷要求'] = self.getRequiredDegree(df.at[i,'學歷要求'])
            df.at[i,'語文條件'] = self.getLanguageData(df.at[i,'語文條件'])
            
        dirname = os.path.dirname(filepath)
        filename = os.path.splitext(filepath)[0] + "_parsed.xlsx"
        df.to_excel(os.path.join(dirname,filename))
        print("finished parsing 104excel at {}...".format(os.path.join(dirname,filename)))
        

    def parse104Dataframe(self,df):
        for i in df.index:
            df.at[i,'view_count'] = self.getAppliedNumber(df.at[i,'view_count'])
            df.at[i,'addr'] = self.getWorkingArea(df.at[i,'addr'])
            df.at[i,'salary'] = self.getSalary(df.at[i,'salary'])
            df.at[i,'required'] = self.getRequiredEmp(df.at[i,'required'])
            df.at[i,'education'] = self.getRequiredDegree(df.at[i,'education'])
            df.at[i,'language'] = self.getLanguageData(df.at[i,'language'])
            #print(df.at[i,'view_count'])
            #print(df.at[i,'address'])
            #print(df.at[i,'salary'])
            #print(df.at[i,'required'])
            #print(df.at[i,'education'])
            #print(df.at[i,'language'])
        return df
    
        
    def getAppliedNumber(self,appliedNumberStr):
        return self.appliedNumberDict.get(appliedNumberStr)

    #bug!
    def getWorkingArea(self,workingStr):
        retVal = ""
        for key in self.workingAreaDict:
            if(workingStr.find(key)>=0):
                retVal = self.workingAreaDict[key]
        return retVal     

    
    #抓薪水
    # input  = "月薪 28,000~40,000元"
    # output = 28000
    #bug!
    def getSalary(self,salaryStr):
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
    def getRequiredEmp(self,requiredStr):
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
    def getRequiredDegree(self,requiredDegreeStr):
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
    def getLanguageData(self,languageStr):
        if(languageStr.find('英文')>=0 and
           languageStr.find('讀 /精通')>=0 and
           languageStr.find('寫 /精通')>=0 ):
            return '英文 讀寫/精通'
        else:
            return 'NA'
        

if __name__ == '__main__':
    filepath = '../Data/jobs104_20190807_myfile.xlsx'
    sheet = "Sheet1"
    
    configPath = '../conf/104_config.xlsx'
    appliedNumberSheet= '目前應徵人數'
    workingAreaSheet = '上班地點'
    parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
    