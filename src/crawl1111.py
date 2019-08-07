from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import requests

header_info = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Connection':'close'
}
#ps: 每頁顯示幾筆資料
#
#
#
def get_job_detail(jobno):
    retryRequest = requests.Session()
    retryRequest.mount( 'https://', HTTPAdapter( max_retries = 3 ) )
#     url = 'https://www.104.com.tw/job/?jobsource=joblist_a_date&jobno={}'
    url = 'https://www.1111.com.tw/job/{}?jobsource=hotjob_chr'
    res = retryRequest.get( url.format( jobno ),headers=header_info, timeout=5,verify=False )
    soup = BeautifulSoup( res.text, 'html.parser')
    return soup


s=get_job_detail("86009533")
print(s)