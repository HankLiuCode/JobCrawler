from bs4 import BeautifulSoup
import re
import requests
from requests.adapters import HTTPAdapter
import time
import pandas

class Crawler104:
    def __init__(self):
        self.header_info = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Connection':'close'
        }
        self.processedJob = []
        
    # if the element chosen has children
    def getElementsText(self,elements):
        seperate_char = "、"
        result = ''
        for element in elements :
            text = element.text.strip()
            if text != '':
                if result != '':
                    result +=seperate_char
                result += text
        return result

    def cleanText(self,text):
        #replace blank lines
        text = text.replace('\n','').replace('\t','').replace('\r','')
        #replace unwanted chars
        text = text.replace(' ','').replace('：','')
        return text
    
    def getRawJobDetail(self,jobno):
        url = 'https://www.104.com.tw/job/{}'
        res = requests.get( url.format( jobno ),headers=self.header_info, timeout=5)
        soup = BeautifulSoup( res.text, 'html.parser')
        #the dict that will be returned
        rawJobDetailDict={}

        #get view count and job content
        view_count = self.cleanText(soup.select_one('.sub a').text).replace("應徵","")
        job_content = self.cleanText(soup.select_one('.content p').text )
        rawJobDetailDict['應徵人數'] = view_count
        rawJobDetailDict['工作內容'] = job_content

        #gets all the columns for jobdetail
        content_keys = soup.select(".content dt")
        content_vals = soup.select('.content dd')
        index = -1
        for key in content_keys:
            index += 1
            rawJobDetailDict[self.cleanText(key.text)] = self.cleanText(content_vals[index].text)
        
        #print(rawJobDetailDict)
        return rawJobDetailDict
    
        def getJobDetail(rawJobDetailDict):
            chineseToEnglishDict = {
                '職務類別':'JobCategory',
                '工作待遇':'Salary',
                '工作性質':'nature',
                '上班地點':'WorkingAddress',
                '管理責任':'Manage',
                '出差外派':'Travel',
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
                '聯絡人':'Contact',
                '工作編號':'jobno',
                '工作名稱':'jobname', 
                '公司':'company', 
                '工作連結':'joblink'
            }

    def crawlerStart(self):
        url = "https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}&keyword=新光銀行行銷"
        totalPage = 2
        currentPage = 1
        jobList = []
        all_jobs = []

        while(currentPage < totalPage):
            retryRequest = requests.Session()
            retryRequest.mount( 'https://', HTTPAdapter( max_retries = 5 ) )
            res = retryRequest.get( url.format( currentPage ),headers=self.header_info, timeout=5,verify=False)
            soup = BeautifulSoup(res.text,'html.parser')
            if currentPage == 1 :
                totalPage = int( re.search( r'\"totalPage\":(\d*)', soup.text).group(1))
            print( '[{}/{}]'.format(currentPage,totalPage))

            jobList = soup.select('.js-job-item')
            for job in jobList:
                jobname = job.select_one('.js-job-link').text
                joblink = job.select_one('.js-job-link')['href']
                joblink = 'https:' + joblink
                print(joblink)
                jobno = self.getJobNo(joblink)
                if(not self.isProcessed(jobno)):
                    self.processedJob.append(jobno)
                
                company = job.select_one('.b-list-inline a').text
                company = self.cleanText(company)
                
                jobDetail = self.getRawJobDetail(jobno)
                moreJobDetail = { '工作編號':jobno, '工作名稱':jobname, '公司':company, '工作連結':joblink}
                jobDetail.update(moreJobDetail)
                all_jobs.append(jobDetail)
                time.sleep(0.2)
            currentPage += 1
        return all_jobs

    def getJobNo(self,link):
        jobno = re.search( r'job/(.*)\?jobsource', link ).group(1)
        return jobno

    def isProcessed(self,jobno):
        if jobno in self.processedJob:
            print("{} is proccesed".format(jobno))
            return True
        return False

if __name__ == "__main__":
    url = "https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&page={}"
    jobno="4pkh7"
    c = Crawler104()
    print(c.getRawJobDetail(jobno))
    #all_jobs = c.crawlerStart()
    #df = pandas.DataFrame(all_jobs)
    #df.to_excel('test.xlsx')
    print('Finish')