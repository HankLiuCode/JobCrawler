from Crawler104Modules import User104, Parser104
from Crawler104 import Crawler104
import pandas
import datetime

def get_filename(name,is_parsed):
    filename = "jobs104_"+str(datetime.datetime.now().date()).replace("-","")+"_" + name 
    if(is_parsed):
        filename += '_parsed'
    filename += ".xlsx"
    return filename

def get_user():
    singleRoTestList = ['全職']
    keywordTestList = [""]
    areaTestList = [""]
    jobcatTestList = ["軟體／工程類人員"]
    indcatTestList = ["金融機構及其相關業"]
    user = User104(
        keywordList=keywordTestList,
        singleRoList=singleRoTestList,
        areaList=areaTestList,
        jobcatList=jobcatTestList,
        indcatList=indcatTestList)
    return user

#outputs excel without furthur parsing
def basic_example():
    user = get_user()
    crawler104=Crawler104(user)
    df=pandas.DataFrame(crawler104.getAllJobs())
    df.to_excel("../Data/"+get_filename("金融相關IT",False))

def parsed_example():
    user = get_user()
    crawler104=Crawler104(user)
    configPath = '../conf/104_config.xlsx'
    workingAreaSheet = '上班地點'
    appliedNumberSheet= '目前應徵人數'
    parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
    df=pandas.DataFrame(crawler104.getAllJobs())
    parsed_df = parser104.parse104Dataframe(df)
    parsed_df.to_excel("../Data/"+get_filename("金融相關IT",True))

def parse_unparsed_excel():
    configPath = '../conf/104_config.xlsx'
    workingAreaSheet = '上班地點'
    appliedNumberSheet= '目前應徵人數'
    parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
    parser104.parse104Excel("../Data/jobs104_20190814_金融相關IT.xlsx")

if __name__ == "__main__":
    parse_unparsed_excel()

    