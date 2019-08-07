from Crawler104Modules import Parser104
import random
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import numpy
import pandas
import re
import time
import datetime

# add this line to pip install to prevent ssl error
# --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org 
#
header_info = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Connection':'close'
}


# 移除空白行
def clean_blank_lines( text ) :
    lines = (line.strip() for line in text.splitlines())
    chunks = ( line.strip() for line in lines )
    result = '\n'.join(chunk for chunk in chunks if chunk)
    return result

def clean_text( text ) :
    return text.replace('\t','').replace('\r','').replace('\n','')

def merge_list( dom, sep_char ) :
    result = ''
    for dt in dom :
        text = dt.text.strip()
        if text != '' :
            if result != '' :
                result += sep_char
            result += dt.text
    return result

def parse_job_content( meta_list ) :
    result = ''
    for meta in meta_list :
        if meta.has_attr('property') and meta['property'] == 'og:description' and meta.has_attr('content')  :
            result = meta['content'].strip()
            break
    return result

def get_job_detail( jobno ) :
    retryRequest = requests.Session()
    retryRequest.mount( 'https://', HTTPAdapter( max_retries = 3 ) )
#     url = 'https://www.104.com.tw/job/?jobsource=joblist_a_date&jobno={}'
    url = 'https://www.104.com.tw/job/{}'
    res = retryRequest.get( url.format( jobno ),headers=header_info, timeout=5,verify=False )
    soup = BeautifulSoup( res.text, 'html.parser')

#     html_src = res.text
#     info_list = soup.select('.info')
#     print( html_src )
#     print( html_src[html_src.index('<h2>公司福利</h2>'):html_src.index('<h2>聯絡方式</h2>')] )
#     print( re.search( r'<h2>公司福利</h2>(.*)<h2>聯絡方式</h2>', html_src, re.S ).group( 1 ) )
#     print( soup.select('.info')[2] )

    view_count=''
    job_content=''
    cate=''
    salary=''
    nature=''
    manage=''
    travel=''
    working=''
    vacation=''
    available=''
    required=''
    identity=''
    experience=''
    education=''
    department=''
    language=''
    skill=''
    other=''
    contact=''
    addr=''
    tool=''
    update=''

    try :
        view_count = soup.select_one('.sub a').text.strip().replace('應徵','') #目前應徵人數
    except Exception as e:
        view_count = ''

#     job_content = clean_blank_lines( parse_job_content( soup.select('meta') ) )
    job_content = clean_blank_lines( soup.select_one('.content p').text )

    content_key = soup.select('.content dt')
    content_val = soup.select('.content dd')

    idx = -1
    for key in content_key :
        idx = idx + 1
        if key.text == '工作性質：' :
            nature = clean_blank_lines( content_val[idx].text )   
        elif key.text == '管理責任：' :
            manage = clean_blank_lines( content_val[idx].text )
        elif key.text == '出差外派：' :
            travel = clean_blank_lines( content_val[idx].text )
        elif key.text == '上班時段：' :
            working = clean_blank_lines( content_val[idx].text )
        elif key.text == '休假制度：' :
            vacation = clean_blank_lines( content_val[idx].text )
        elif key.text == '可上班日：' :
            available = clean_blank_lines( content_val[idx].text )
        elif key.text == '需求人數：' :
            required = clean_blank_lines( content_val[idx].text )
        elif key.text == '接受身份：' :
            identity = clean_blank_lines( content_val[idx].text )
        elif key.text == '工作經歷：' :
            experience = clean_blank_lines( content_val[idx].text )
        elif key.text == '學歷要求：' :
            education = clean_blank_lines( content_val[idx].text )
        elif key.text == '科系要求：' :
            department = clean_blank_lines( content_val[idx].text )
        elif key.text == '語文條件：' :
            language = clean_blank_lines( content_val[idx].text )
        elif key.text == '工作技能：' :
            skill = clean_blank_lines( content_val[idx].text )
        elif key.text == '其他條件：' :
            other = clean_blank_lines( content_val[idx].text )
        elif key.text == '聯絡人：' :
            contact = clean_blank_lines( content_val[idx].text )

    try :
        salary = clean_text( soup.select_one('.salary').text ) #工作待遇
        if( salary != None and salary.find('面議') >= 0 ):
            salary = '面議'
    except Exception as e:
        salary = ''
    try :
        cate =  merge_list( soup.select('.cate span'), '、' ) #職務類別
    except Exception as e:
        cate = ''
    try :
        addr = clean_text( soup.select_one('.addr').text ).replace('地圖找工作','').strip() #上班地點
    except Exception as e:
        addr = ''
    try :
        tool =  merge_list( soup.select('.tool a'), '、' ) #擅長工具
    except Exception as e:
        tool = ''
    try :
        update = soup.select_one('.update').text.replace('更新日期：','') #更新日期
    except Exception as e:
        update = ''

    job_detail = {
        'view_count':view_count,
        'job_content':job_content,
        'cate':cate,
        'salary':salary,
        'nature':nature,
        'manage':manage,
        'travel':travel,
        'working':working,
        'vacation':vacation,
        'available':available,
        'required':required,
        'identity':identity,
        'experience':experience,
        'education':education,
        'department':department,
        'language':language,
        'skill':skill,
        'other':other,
        'contact':contact,
        'addr':addr,
        'tool':tool,
        'update':update
    }
    return job_detail

def start_crawl( url ):
    all_jobs = []
    total_page = 999
    curr_page = 1
    total_row = 0
    processed = []
    while curr_page <= total_page :
        retryRequest = requests.Session()
        retryRequest.mount( 'https://', HTTPAdapter( max_retries = 5 ) )

        res = retryRequest.get( url.format( curr_page ), headers=header_info, timeout=10 ,verify=False)

        soup = BeautifulSoup( res.text, 'html.parser')

        # 取搜尋結果總頁數
        if curr_page == 1 :
            total_page = int( re.search( r'\"totalPage\":(\d*)', soup.text ).group( 1 ) )
        print( '[' + str(curr_page) + '/' + str(total_page)+ ']' )

        job_list = soup.select('.js-job-item')
        for job in job_list :
            jobname = job.select_one('.js-job-link').text
            link = job.select_one('.js-job-link')['href']
            link = 'https:' + link
            #排除獵人頭
            if( link.find('hunter.104.com.tw') >= 0 ) :
                print( 'ignore : ' + link)
                continue

            #取 Job No.
            jobno = re.search( r'job/(.*)\?jobsource', link ).group(1)
            if jobno in processed :
                print( 'Processed : ' + jobno )
                continue
            else :
                total_row = total_row + 1
                processed.append( jobno )

            #取公司名稱
            company = job.select_one('.b-list-inline a').text
            company = clean_blank_lines( company.strip() )

            #取職務
            kind = job.select('.b-clearfix li')[2].text

            job_data = { 'jobno':jobno, 'jobname':jobname, 'company':company, 'url':link }

            print( str(total_row) + '.' + link)

            job_detail = get_job_detail( jobno )
            job_data.update( job_detail )
            all_jobs.append( job_data )
            time.sleep( random.uniform( 1.0, 2.0 ) )

            # for test only
    #         break

        curr_page = curr_page + 1

        # for test only
    #     if( curr_page > 2 ) :
    #         break
    return all_jobs

class User104:
    def paradef(self):
        return ""
        #### 參數解釋 ####
        # ro:         0(全部),1(全職),2(兼職),3(高階),4(派遣),5(接案),6(家教)
        # order:     11(依日期排序), 4(依學歷排序)
        # asc:       1(ascending=true), 0(ascending=false)
        # mode:      s(摘要),l(列表)
        # page:      <int>(第幾頁)
        # jobsource: ??? (打甚麼好像沒差)
        # example: 'https://www.104.com.tw/jobs/search/?ro=1&order=11&asc=0&mode=s&jobsource=indexpoc2018&page=1

        #### 額外參數 ####
        # 參數使用範例:  多於一個參數用 % 隔開
        #              url = url + &jobcat=2007001000%2007002000%2007000000
        #              url = url + &area=6001001000%2C6001002000
        #              url = url + '&indcat=1004000000'
        #              url = url + &keyword=國泰人壽
        #
        # ro 工作型態        
        #      0(全部),1(全職),2(兼職),3(高階),4(派遣),5(接案),6(家教)
        #
        # jobcat 職務類別
        #     2007000000(資訊軟體系統類) { 2007001000(軟體／工程類人員), 2007002000(MIS程式設計師) }
        #     2003002000(金融專業相關類人員)
        #
        # area 地區
        #     6001001000(台北市), 2C6001002000(新北市), 6001005000(桃園市)
        #
        # indcat 公司產業
        #     1004000000(金融投顧及保險業) { 1004002000(投資理財相關業), 1004001000(金融機構及其相關業) }
        # 
        # keyword
        # 額外關鍵字搜尋
        #   
    def __init__(self,keywordList,areaList,jobcatList,indcatList):
        self.areaDict = self.get_area_dict()
        self.jobcatDict = self.get_jobcat_dict()
        self.indcatDict = self.get_indcat_dict()
        self.url= self.generate_url(
                keywordList,
                [self.areaDict[area] for area in areaList],
                [self.jobcatDict[jobcat] for jobcat in jobcatList],
                [self.indcatDict[indcat] for indcat in indcatList],
            )
        
    def get_area_dict(self):
        area_dict = {
            "台北市" : "6001001000", "新北市" : "2C6001002000" , "桃園市" : "6001005000"
        }
        return area_dict
    def get_jobcat_dict(self):
        jobcat_dict = {
            "資訊軟體系統類" : "2007000000", "軟體／工程類人員" : "2007001000" , "MIS程式設計師" : "2007002000" ,
            "金融專業相關類人員" : "2003002000"
        }
        return jobcat_dict
    def get_indcat_dict(self):
        indcat_dict = {
            "金融投顧及保險業" : "1004000000", "投資理財相關業" : "1004002000" , "金融機構及其相關業" : "1004001000" 
        }
        return indcat_dict


    def get_test_url(self):
        url = u.generate_url( 
                keywordList=["新光銀行","行銷"],
                areaList=["6001001000","2C6001002000"],
                jobcatList=["2007000000","2003002000"],
                indcatList=["1004000000","1004002000"]
            )
        return url

    def generate_url(self,keywordList,areaList,jobcatList,indcatList):
        fullurl = 'https://www.104.com.tw/jobs/search/?jobsource=2018indexpoc&ro=1&page={}'
        fullurl += self.generate_url_segment("keyword",keywordList,False)
        fullurl += self.generate_url_segment("area",areaList,False)
        fullurl += self.generate_url_segment("jobcat",jobcatList,False)
        fullurl += self.generate_url_segment("indcat",indcatList,False)
        return fullurl
    def generate_url_segment(self,parameterName,parameterList,isFirstParameter):
        url_segment = ""
        if(not isFirstParameter):
            url_segment += "&" 
        url_segment += parameterName + "="
        
        for i in range(len(parameterList)):
            url_segment = url_segment + parameterList[i]
            if i < len(parameterList) - 1:
                url_segment = url_segment + "%"

        return url_segment
    def get_url(self):
        return self.url
    def get_filename(self,sitename,keyword):
        filename = sitename+"_"+str(datetime.datetime.now().date()).replace("-","_") +"_" + keyword + ".xlsx"
        return filename

keywordList = ["新光","銀行"]
areaTestList = ["台北市"]
jobcatTestList = ["資訊軟體系統類"]
indcatTestlist = ["金融投顧及保險業"]
u = User104(keywordList,areaTestList,jobcatTestList,indcatTestlist)
print(u.get_url())
#print(u.generate_url(keywordList=["keyword1","keyword2"],areaList=["aaaaaaaa","baaaaaaaaaa"],jobcatList=["jjjjjjjjjjjj","JJJJJJJJJJJ"],indcatList=["iiiiiiiiiiiiii","iiiiiiiiiiii"]))
#print(u.generate_url_segment("area",["aaaaaaaa","bbbbbbbb","cccccccc"],True))
