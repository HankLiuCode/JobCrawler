import datetime


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
    
    def get_filename(self,name):
        filename = "jobs104_"+str(datetime.datetime.now().date())+"_" + name + ".xlsx"
        return filename

if __name__ == "__main__":

    keywordList = ["新光","銀行"]
    areaTestList = ["台北市"]
    jobcatTestList = ["資訊軟體系統類"]
    indcatTestlist = ["金融投顧及保險業"]
    u = User104(keywordList,areaTestList,jobcatTestList,indcatTestlist)
    
    #print(u.get_filename("myfile"))
    #print(u.get_url())
    #print(u.generate_url(keywordList=["keyword1","keyword2"],areaList=["aaaaaaaa","baaaaaaaaaa"],jobcatList=["jjjjjjjjjjjj","JJJJJJJJJJJ"],indcatList=["iiiiiiiiiiiiii","iiiiiiiiiiii"]))
    #print(u.generate_url_segment("area",["aaaaaaaa","bbbbbbbb","cccccccc"],True))
