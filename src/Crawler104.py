from bs4 import BeautifulSoup
import re
import requests
from requests.adapters import HTTPAdapter
import time
import pandas
from Crawler104Modules import User104,Parser104

class Crawler104:
    def __init__(self,rootURL):
        self.header_info = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Connection':'close'
        }
        self.rootURL = rootURL
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
        text = text.replace('\n','').replace('\t','').replace('\r','')
        #replace unwanted chars
        text = text.replace(' ','').replace('：','')
        return text

    def __getJobNo(self,link):
        jobno = re.search( r'job/(.*)\?jobsource', link ).group(1)
        return jobno

    def __isProcessed(self,jobno):
        if jobno in self.processedJob:
            print("{} is proccesed".format(jobno))
            return True
        return False
    
    def __getTotalPage(self):
        res = requests.get( self.rootURL.format(1),headers=self.header_info, timeout=10)
        soup = BeautifulSoup(res.text,'html.parser')
        totalPage = int( re.search( r'\"totalPage\":(\d*)', soup.text).group(1))
        return totalPage

    def __getTotalCount(self):
        res = requests.get( self.rootURL.format(1),headers=self.header_info, timeout=10)
        soup = BeautifulSoup(res.text,'html.parser')
        totalCount = int( re.search( r'\"totalCount\":(\d*)', soup.text).group(1))
        return totalCount

    def getJobDetail(self,jobno):
        url = 'https://www.104.com.tw/job/{}'
        res = requests.get( url.format( jobno ),headers=self.header_info, timeout=5)
        soup = BeautifulSoup( res.text, 'html.parser')
        #dict that has chinese as key
        jobDetailDict={}

        #get view count and job content
        appliedNumber = self.__cleanText(soup.select_one('.sub a').text).replace("應徵","")
        jobContent = self.__cleanText(soup.select_one('.content p').text)
        jobDetailDict['應徵人數'] = appliedNumber
        jobDetailDict['工作內容'] = jobContent

        #gets all other columns for jobdetail
        content_keys = soup.select(".content dt")
        content_vals = soup.select('.content dd')
        index = -1
        for key in content_keys:
            index += 1
            jobDetailDict[self.__cleanText(key.text)] = self.__cleanText(content_vals[index].text)
        
        #print(jobDetailDict)
        return jobDetailDict

    def getAllJobs(self):
        totalPage = self.__getTotalPage()
        totalCount = self.__getTotalCount()
        currentPage = 1
        currentCount = 1
        jobItems = []
        jobList = []

        while(currentPage <= totalPage):
            retryRequest = requests.Session()
            retryRequest.mount( 'https://', HTTPAdapter( max_retries = 5 ) )
            res = retryRequest.get( self.rootURL.format( currentPage ),headers=self.header_info, timeout=5)
            soup = BeautifulSoup(res.text,'html.parser')
            print( 'Page: [{}/{}]'.format(currentPage,totalPage))
            
            jobItems = soup.select('.js-job-item')
            for job in jobItems:
                jobname = job.select_one('.js-job-link').text
                joblink = job.select_one('.js-job-link')['href']
                joblink = 'https:' + joblink
                print( '[{}/{}] {}'.format(currentCount,totalCount,joblink))
                
                jobno = self.__getJobNo(joblink)
                self.processedJob.append(jobno)
            
                company = job.select_one('.b-list-inline a').text
                company = self.__cleanText(company)
                
                jobDetail = self.getJobDetail(jobno)
                moreJobDetail = { '工作編號':jobno, '工作名稱':jobname, '公司':company, '工作連結':joblink}
                jobDetail.update(moreJobDetail)
                jobList.append(jobDetail)
                currentCount += 1 
                time.sleep(0.2)
            currentPage += 1
        return jobList

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
    query = user.get_query()
    c = Crawler104(query)
    allJobs = c.getAllJobs()
    df = pandas.DataFrame(allJobs)
    df.to_excel('test2.xlsx')
    print(len(c.processedJob)==len(set(c.processedJob)))
    print('Finish')