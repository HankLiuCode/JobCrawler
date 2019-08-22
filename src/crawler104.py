from crawler104Modules import URLMaker104, Parser104
from crawler104Core import Crawler104Core
from settings import configPath,workingAreaSheet,appliedNumberSheet,dataDirectory
import pandas
import datetime
import os

class Crawler104:
    def __init__(self):
        self.url = self.get_url()
        self.df_unparsed = None

    def get_filename(self, name, parsed):
        filename = "jobs104_"+ str(datetime.datetime.now().date()).replace("-","")+"_" + name
        if(parsed):
            filename += '_parsed'
        filename += ".xlsx"
        filename = os.path.join(dataDirectory,filename)
        return filename

    def start_crawl(self):
        crawler104Core = Crawler104Core(self.url)
        self.df_unparsed = pandas.DataFrame(crawler104Core.getAllJobs())

    def generate_excel(self,filename):
        self.df_unparsed.to_excel(self.get_filename(filename,parsed=False),index=False)

    def generate_excel_parsed(self,filename):
        parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
        df_parsed = parser104.parse104Dataframe(self.df_unparsed)
        df_parsed.to_excel(self.get_filename(filename,parsed=True),index=False)

    def parse_unparsed_excel(self,filename):
        parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
        filename = os.path.join(dataDirectory,filename)
        parser104.parse104Excel(filename)

    def get_url(self):
        url = URLMaker104(
            keywordList     =   [""], # 關鍵字
            singleRoList    =   ['全職'], # 全職 兼職
            areaList        =   ["台北"], # 縣市
            jobcatList      =   ["軟體／工程類人員"],  # 工作類別
            indcatList      =   ["金融機構及其相關業"] # 產業類別
            ).get_query()
        return url

if __name__ == "__main__":
    myCrawler = Crawler104()
    #myCrawler.start_crawl()
    #myCrawler.generate_excel("金融")
    #myCrawler.generate_excel_parsed("Test")
    myCrawler.parse_unparsed_excel("jobs104_20190822_金融IT.xlsx")
