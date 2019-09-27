from bs4 import BeautifulSoup
import re
import requests
from requests.adapters import HTTPAdapter
import time
import pandas

class Crawler104Core:
    def __init__(self):
        self.header_info = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Connection':'close'
        }
        self.processedJob = []
    
    # if the element chosen has children
    def __getElementsText(self,elements):
        seperate_char = "、"
        result = ''
        for element in elements :
            text = element.text.strip()
            if text != '':
                if result != '':
                    result +=seperate_char
                result += text
        return result

    def __cleanText(self,text):
        #replace blank lines
        text = text.strip().replace('\n','').replace('\t','').replace('\r','')
        #replace unwanted chars
        text = text.replace('：','')
        return text

    def getJobDetail(self,joblink):
        jobDetailDict = {}
        if (not re.search( r'job/(.*)\?jobsource', joblink ) == None):
            jobno = re.search( r'job/(.*)\?jobsource', joblink ).group(1)
            if not jobno in self.processedJob:
                jobDetailDict = self.getStandardJobDetail(jobno)
            else:
                print("{} is proccesed".format(jobno))
        else:
            print("joblink invalid : {}".format(joblink))
        return jobDetailDict
    
    #抓取104一般的網頁格式(全職,兼職) 派遣,接案,家教等不包括在此
    def getStandardJobDetail(self,jobno):
        url = 'https://www.104.com.tw/job/{}'
        retryRequest = requests.Session()
        retryRequest.mount( 'https://', HTTPAdapter( max_retries = 5 ) )
        res = retryRequest.get( url.format(jobno),headers=self.header_info, timeout=5,verify=False)
        soup = BeautifulSoup( res.text, 'html.parser')

        appliedNumber = self.__cleanText(soup.select_one('.sub a').text).replace("應徵","")
        jobContent = self.__cleanText(soup.select_one('.content p').text)
        #dict that has chinese as key
        jobDetailDict = {
            '工作編號': jobno,
            '工作名稱':'', 
            '公司':'', 
            '應徵人數': appliedNumber,
            '需求人數':'',
            '工作待遇':'',
            '職務類別':'',
            '上班地點':'',
            '工作性質':'',
            '管理責任':'',
            '出差外派':'',
            '工作經歷':'',
            '學歷要求':'',
            '科系要求':'',
            '語文條件':'',
            '擅長工具':'',
            '具備證照':'',
            '工作技能':'',
            '其他條件':'',
            '工作內容': jobContent,
            '合併欄位':'',
            '斷詞分析':'',
            '工作連結':'',
        }
        #gets all other columns for jobdetail
        content_keys = soup.select(".content dt")
        content_vals = soup.select('.content dd')
        index = -1
        for key in content_keys:
            index += 1
            if self.__cleanText(key.text) in jobDetailDict:
                jobDetailDict[self.__cleanText(key.text)] = self.__cleanText(content_vals[index].text)
        
        jobDetailDict["職務類別"] = jobDetailDict["職務類別"].replace(" ",'').replace("認識「」職務詳細職類分析(工作內容、薪資分布..)更多相關工作","")
        jobDetailDict['上班地點'] = jobDetailDict['上班地點'].replace(" ",'').replace("地圖找工作","")
        
        self.processedJob.append(jobno)
        #print(jobDetailDict)
        return jobDetailDict

    def getTotal(self,url):
        retryRequest = requests.Session()
        retryRequest.mount( 'https://', HTTPAdapter( max_retries = 5 ) )
        res = retryRequest.get( url.format(1),headers=self.header_info, timeout=5, verify=False)
        soup = BeautifulSoup(res.text,'html.parser')

        totalCount = int( re.search( r'\"{}\":(\d*)'.format("totalCount"), soup.text).group(1))
        totalPage = int( re.search( r'\"{}\":(\d*)'.format("totalPage"), soup.text).group(1))
        return [totalCount,totalPage]

    def start_crawl(self, root_url):
        totalCount, totalPage = self.getTotal(root_url)
        currentPage = 1
        currentCount = 1

        jobList = []
        try:
            while(currentPage <= totalPage):
                retryRequest = requests.Session()
                retryRequest.mount( 'https://', HTTPAdapter( max_retries = 5 ) )
                
                res = retryRequest.get( root_url.format( currentPage ),headers=self.header_info, timeout=5, verify=False)
                soup = BeautifulSoup(res.text,'html.parser')
                print( 'Page: [{}/{}]'.format(currentPage,totalPage))
                
                jobItems = []
                jobItems = soup.select('.js-job-item')
                for job in jobItems:
                    jobname = job.select_one('.js-job-link').text
                    joblink = job.select_one('.js-job-link')['href']
                    joblink = 'https:' + joblink

                    company = job.select_one('.b-list-inline a').text
                    company = self.__cleanText(company)

                    jobDetail = self.getJobDetail(joblink)
                    #not tested yet
                    if jobDetail:
                        moreJobDetail = {'工作名稱':jobname, '公司':company, '工作連結':joblink}
                        jobDetail.update(moreJobDetail)
                        jobList.append(jobDetail)
                    print( '[{}/{}] {}'.format(currentCount,totalCount,joblink))
                    currentCount += 1
                currentPage += 1
        except KeyboardInterrupt:
            return jobList
        return jobList

    # 以下還在測試 為了解決104中只能爬到150頁(約3000個工作)的問題
    # 利用 104_config.xml 中
    def url_siever(urls):
    jobcat_urls = sieve_urls_with_param(urls, 'jobcat')
    area_urls = sieve_urls_with_param([url[0] for url in jobcat_urls if not url[1]], 'area')
    
    print(area_urls)


    def sieve_urls_with_param(urls, sieve_with_param):
        url_list = []
        for url in urls:
            param_list = []
            param_name = sieve_with_param
            traverse_param_tree(param_list, url, param_name)
            for param in param_list:
                param_url = url + "&{}=".format(param_name) + param[0]
                url_list.append((param_url, param[1]))
        return url_list


    def traverse_param_tree(param_list, base_url, param_name, param_val = None):
        url = base_url + "&{}=".format(param_name)
        if not param_val:
            for param in param_child(param_name):
                traverse_param_tree(param_list, base_url, param_name, param)

        elif getTotal(url+param_val)[0] < 3000:
            param_list.append((param_val, True))

        elif getTotal(url+param_val)[0] >= 3000 and len(param_child(param_name, param_val)) == 0:
            param_list.append((param_val, False))

        else:
            for param in param_child(param_name, param_val):
                traverse_param_tree(param_list, base_url, param_name, param)

    def param_child(param_name, param_val = None):
        param_children_value = []
        xml_path = os.path.join(settings.configDirectory,'104_config.xml')
        tree = xml_etree_ElementTree.parse(xml_path)
        try:
            parent = tree.find('{}'.format(param_name))
            if param_val:
                parent = parent.find('.//*[@value="{}"]'.format(param_val))
            for child in parent:
                param_children_value.append(child.attrib['value'])
        except TypeError:
            print("{} param_name {} does not exist".format(TypeError, param_name))
            raise
        return param_children_value

    def url_param_dict(url):
        params = re.findall(r"[^&?]*?=[^&?]*",url)
        param_dict = {}
        for param in params:
            p_name,p_val = param.split("=")
            param_dict[p_name] = p_val.split("%2C")
        return param_dict 