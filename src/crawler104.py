from crawler104Modules import Parser104
from crawler104Core import Crawler104Core
from settings import configPath,workingAreaSheet,appliedNumberSheet,dataDirectory,parsedDirectory
import pandas
import datetime
import os

class Crawler104:
    def __init__(self):
        self.crawlerCore = Crawler104Core()
        self.df_unparsed = pandas.DataFrame({})

    def get_filepath(self, name):
        filename = "jobs104_"+ str(datetime.datetime.now().date()).replace("-","")+"_" + name
        filename += ".xlsx"
        filename = os.path.join(dataDirectory,filename)
        return filename

    def start_crawl(self, url):
        df = pandas.DataFrame(self.crawlerCore.start_crawl(url))
        self.df_unparsed = self.df_unparsed.append(df)

    def generate_excel(self,filename):
        self.df_unparsed.to_excel(self.get_filepath(filename),index=False)

    def parse_unparsed_excel(self,from_filepath,sheet="Sheet1"):
        parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
        df = pandas.read_excel(io=from_filepath,sheet_name=sheet)
        df = parser104.parse104Dataframe(df)
        
        filename = os.path.basename(from_filepath) + "_parsed" + ".xlsx"
        to_filepath = os.path.join(parsedDirectory,filename)
        df.to_excel(to_filepath,index=False)
        print("finished parsing:  {} -> {}".format(from_filepath,to_filepath))
    
    
if __name__ == "__main__":
    # 參數使用範例:  多於一個參數用 % 隔開
    #               url = url + &[Parameter]=[Value]%[Value]%[Value]
    # ro 工作型態        
    # jobcat 職務類別
    # area 地區
    # indcat 公司產業
    # keyword 關鍵字搜尋

    # 額外參數
    # order 排序方式
    # asc 由低到高
    ro_dict = {"全部":"0","全職":"1","兼職":"2","高階":"3","派遣":"4","接案":"5","家教":"6" }
    area_dict = {
            "基隆" : "6001004000", "台北" : "6001001000", "新北" : "2C6001002000",
            "桃園" : "6001005000", "新竹" : "6001006000", "苗栗" : "6001007000",
            "台中" : "6001008000", "彰化" : "6001010000", "南投" : "6001011000",
            
            "雲林" : "6001012000", "嘉義" : "6001013000", "台南" : "6001014000",
            "高雄" : "6001016000", "屏東" : "6001018000",
            
            "宜蘭" : "6001003000", "花蓮" : "6001020000", "台東" : "6001019000",
            "金門" : "6001022000", "馬祖" : "6001023000", "連江" : "6001023000",
        }
    jobcat_dict = {
            "資訊軟體系統類":"2007000000", 
                "軟體／工程類人員":"2007001000" , 
                    "軟體專案主管":"2007001001",
                    "電子商務技術主管":"2007001002",
                    "通訊軟體工程師":"2007001003",
                    "軟體設計工程師":"2007001004",
                    "韌體設計工程師":"2007001005",
                    "Internet程式設計師":"2007001006",
                    "電腦系統分析師":"2007001007",
                    "電玩程式設計師":"2007001008",
                    "其他資訊專業人員":"2007001009",
                    "資訊助理人員":"2007001010",
                    "BIOS工程師":"2007001011",
                    "演算法開發工程師":"2007001012",
                "MIS程式設計師":"2007002000" ,
                    "MIS/網管主管":"2007002001",
                    "資料庫管理人員":"2007002002",
                    "MIS程式設計師":"2007002003",
                    "MES工程師":"2007002004",
                    "網路管理工程師":"2007002005",
                    "系統維護/操作人員":"2007002006",
                    "資訊設備管制人員":"2007002007",
                    "網路安全分析師":"2007002008",

            "財會/金融專業類":"2003000000", 
                "金融專業相關類人員" : "2003002000" , 
                "財務/會計/稅務類" : "2003001000", 
            
            "國外業務人員":"2005003005",
            "工讀生":"2002001011",
        }
    indcat_dict = {
            "金融投顧及保險業" : "1004000000", "投資理財相關業" : "1004002000" , "金融機構及其相關業" : "1004001000", 
        }
    order_dict = { 
            "符合度排序":"12","日期排序":"11","學歷":"4","經歷":"3","應徵人數":"7","待遇":"13"
        }
    
    myCrawler = Crawler104()
    root_url = 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}'
    urls = []
    for i in range(12):
        jobcat_url = root_url + "&jobcat=20070010{:02}".format(i+1)
        urlTotal = myCrawler.crawlerCore.getTotal('totalCount',jobcat_url)
        if urlTotal > 3000:
            area_jobcat_url_taipei = jobcat_url + "&area=6001001000"
            area_jobcat_url_xinbei = jobcat_url + "&area=2C6001002000"
            area_jobcat_url_taoyuan = jobcat_url + "&area=6001005000"
            area_jobcat_url_xinzhu = jobcat_url + "&area=6001006000"
            area_jobcat_url_taichung = jobcat_url + "&area=6001008000"
            area_jobcat_url_kaohsiung = jobcat_url + "&area=6001016000"
            area_jobcat_url_others_1 = jobcat_url + "&area=6001003000%6001020000%6001019000%6001022000%6001023000%6001023000"
            area_jobcat_url_others_2 = jobcat_url + "&area=6001004000%6001007000%6001010000%6001011000%6001012000%6001013000%6001014000%6001018000"
        else:
            urls.append(jobcat_url)
    for i in range(8):
        jobcat_url = root_url + "&jobcat=20070020{:02}".format(i+1)
        urlTotal = myCrawler.crawlerCore.getTotal('totalCount',jobcat_url)
        urls.append(jobcat_url)
    
    for url in urls:
        urlTotal = myCrawler.crawlerCore.getTotal('totalCount',url)
        #print("{} totalCount:{}".format(url,urlTotal))

    myCrawler.start_crawl("https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}&jobcat=2007001006&indcat=1004002000")
    myCrawler.generate_excel("Testing")

    #myCrawler.parse_unparsed_excel("../data/jobs104_20190912_IT產業.xlsx")
