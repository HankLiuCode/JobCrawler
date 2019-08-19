from Crawler104Modules import URLMaker104, Parser104
from Crawler104Core import Crawler104
from settings import configPath,workingAreaSheet,appliedNumberSheet,dataDirectory
import pandas
import datetime
import os

def store_file(directory,name,is_parsed):
    filename = "jobs104_"+ str(datetime.datetime.now().date()).replace("-","")+"_" + name 
    if(is_parsed):
        filename += '_parsed'
    filename += ".xlsx"
    filename = os.path.join(directory,filename)
    return filename

def get_url():
    singleRoTestList = ['全部']
    keywordTestList = [""]
    areaTestList = [""]
    jobcatTestList = ["軟體／工程類人員"]
    indcatTestList = ["金融機構及其相關業"]
    url =URLMaker104(
        keywordList=keywordTestList,
        singleRoList=singleRoTestList,
        areaList=areaTestList,
        jobcatList=jobcatTestList,
        indcatList=indcatTestList)
    return url

#outputs excel without furthur parsing
def basic_example():
    url = get_url()
    crawler104=Crawler104(url)
    df=pandas.DataFrame(crawler104.getAllJobs())
    df.to_excel(store_file(dataDirectory,"金融軟體人員",False))

def parsed_example():
    url = get_url()
    crawler104=Crawler104(url)
    parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
    df=pandas.DataFrame(crawler104.getAllJobs())
    parsed_df = parser104.parse104Dataframe(df)
    parsed_df.to_excel(store_file(dataDirectory,"金融軟體人員",True))

def parse_unparsed_excel():
    parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
    parser104.parse104Excel("../Data/jobs104_20190819_金融軟體人員.xlsx")


if __name__ == "__main__":
    parse_unparsed_excel()

    