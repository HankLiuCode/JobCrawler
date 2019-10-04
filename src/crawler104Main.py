from crawler104Modules import Parser104
from crawler104Core import Crawler104Core
import settings
import pandas
from datetime import datetime
import os

def filename_with_header(self, name):
    filename = "jobs104_"+ str(datetime.datetime.now().date()).replace("-","")+"_" + name
    filename = os.path.join(settings.dataDirectory,filename)
    return filename

def parse_unparsed_excel(self,from_filepath,sheet="Sheet1"):
    parser104 = Parser104(configPath,appliedNumberSheet,workingAreaSheet)
    df = pandas.read_excel(io=from_filepath,sheet_name=sheet)
    df = parser104.parse104Dataframe(df)
    
    filename = os.path.basename(from_filepath) + "_parsed" + ".xlsx"
    to_filepath = os.path.join(settings.parsedDirectory,filename)
    df.to_excel(to_filepath,index=False)
    print("finished parsing:  {} -> {}".format(from_filepath,to_filepath))


if __name__ == "__main__":
    # 參數使用範例:  參數 > 1 用 %2C 隔開
    #               url = url + &[Parameter]=[Value]%2C[Value]%2C[Value]
    # 參數:         ro 工作型態, jobcat 職務類別, area 地區, indcat 公司產業, keyword 關鍵字搜尋
    # 額外參數:     order 排序方式, asc 由低到高

    ro_dict = {"全部":"0","全職":"1","兼職":"2","高階":"3","派遣":"4","接案":"5","家教":"6" }
    order_dict = {"符合度排序":"12","日期排序":"11","學歷":"4","經歷":"3","應徵人數":"7","待遇":"13"}
    root_url = 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}'

    name = "whatever.xlsx"
    filename = "jobs104_"+ str(datetime.combine(datetime().date(),datetime().timetz())).replace("-","")+"_" + name
    print(filename)
