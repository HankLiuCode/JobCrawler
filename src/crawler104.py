from crawler104Modules import Parser104
from crawler104Core import Crawler104Core
import settings
import pandas
import datetime
import os
import re
from xml.etree import ElementTree as xml_etree_ElementTree

import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

class Crawler104:
    def __init__(self):
        self.crawlerCore = Crawler104Core()
        self.df_unparsed = pandas.DataFrame()

    def get_filepath(self, name):
        filename = "jobs104_"+ str(datetime.datetime.now().date()).replace("-","")+"_" + name
        filename += ".xlsx"
        filename = os.path.join(settings.dataDirectory,filename)
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
        to_filepath = os.path.join(settings.parsedDirectory,filename)
        df.to_excel(to_filepath,index=False)
        print("finished parsing:  {} -> {}".format(from_filepath,to_filepath))

def getTotal(url):
    header_info = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection':'close'
    }
    retryRequest = requests.Session()
    retryRequest.mount( 'https://', HTTPAdapter( max_retries = 5 ) )
    res = retryRequest.get( url.format(1),headers=header_info, timeout=5, verify=False)
    soup = BeautifulSoup(res.text,'html.parser')

    totalCount = int( re.search( r'\"{}\":(\d*)'.format("totalCount"), soup.text).group(1))
    totalPage = int( re.search( r'\"{}\":(\d*)'.format("totalPage"), soup.text).group(1))
    return [totalCount,totalPage]

def url_seiver(urls):
    root_url = 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}'
    passed_urls = []
    unpassed_urls = urls
        
    print(passed_urls)
    print(unpassed_urls)

def traverse_param_tree(param_list, param_name, param_val = None):
    url = 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}&jobcat='
    for param in param_child("jobcat", param_val):
        traverse_param_tree(param_list, param_name, param)
    param_list.append(param_val)

def param_child(param_name, param_val = None):
    param_children_value = []
    xml_path = os.path.join(settings.configDirectory,'104_config.xml')
    tree = xml_etree_ElementTree.parse(xml_path)
    parent = tree.find('{}'.format(param_name))
    if param_val:
        parent = parent.find('.//*[@value="{}"]'.format(param_val))
    for child in parent:
        param_children_value.append(child.attrib['value'])
    return param_children_value

def url_param_dict(url):
    params = re.findall(r"[^&?]*?=[^&?]*",url)
    param_dict = {}
    for param in params:
        p_name,p_val = param.split("=")
        param_dict[p_name] = p_val.split("%2C")
    return param_dict 


if __name__ == "__main__":
    # 參數使用範例:  參數 > 1 用 %2C 隔開
    #               url = url + &[Parameter]=[Value]%2C[Value]%2C[Value]
    # 參數:         ro 工作型態, jobcat 職務類別, area 地區, indcat 公司產業, keyword 關鍵字搜尋
    # 額外參數:     order 排序方式, asc 由低到高
    ro_dict = {"全部":"0","全職":"1","兼職":"2","高階":"3","派遣":"4","接案":"5","家教":"6" }
    order_dict = {"符合度排序":"12","日期排序":"11","學歷":"4","經歷":"3","應徵人數":"7","待遇":"13"}
    root_url = 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}'
    
    param_list = []
    traverse_param_tree(param_list,"jobcat")
    print(param_list)
    #myCrawler = Crawler104()
    #myCrawler.start_crawl(root_url)
    #myCrawler.generate_excel("test")
    #myCrawler.parse_unparsed_excel("../data/jobs104_20190912_IT產業.xlsx")

