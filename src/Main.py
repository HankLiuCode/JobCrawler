from Crawler104Modules import Parser104
from Crawler104 import Crawler104
from User104 import User104
import pandas

if __name__ == "__main__":
    singleRoTestList = ['兼職']
    keywordTestList = ["新光","銀行"]
    areaTestList = ["台北市"]
    jobcatTestList = ["資訊軟體系統類"]
    indcatTestList = ["金融投顧及保險業"]
    u = User104(
        keywordList=keywordTestList,
        singleRoList=singleRoTestList,
        areaList=areaTestList,
        jobcatList=jobcatTestList,
        indcatList=indcatTestList)
    
    c = Crawler104(u.get_url())
    df=pandas.DataFrame(c.getAllJobs())
    df.to_excel("test.xlsx")