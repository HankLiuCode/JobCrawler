from Crawler104Modules import Parser104,User104
from Crawler104 import Crawler104
import pandas
import jieba

def cleanText(uncleanStr):
    return uncleanStr.replace(' ','').replace('\n','').replace('\r','')

if __name__ == "__main__":
    df = pandas.read_excel("../Data/test2.xlsx")
    df['合併欄位'] = ''
    df['斷詞分析'] = ''
    for i in df.index:
        df.at[i,'合併欄位'] = df.at[i,'工作名稱'] + df.at[i,'工作內容'] + df.at[i,'其他條件']
        df.at[i,'合併欄位'] = df.at[i,'合併欄位'].upper()
    
    teststr = """
    新光人壽-資料庫管理師(有相關經驗、證照者從優核敘)1.安裝、建置、維護及管理資料庫物件。2...
    1     新光人壽-軟體設計師(有相關經驗、證照者從優核敘)1.負責撰寫壽險業大型系統程式(領域包含保...
    2     新光人壽-架構專案襄理(投資前台、.NET MVC)(有相關經驗、證照者從優核敘)1.設計應...
    3     新光人壽-行銷企劃專案襄理(電子商務行銷策略規劃)•電子商務行銷策略規劃•行動商務行銷策略規...
    4     新光人壽-數據分析襄理(資料倉儲及大數據分析平台規劃)新光人壽相信資訊科技是企業競爭力的重要...
    5     新光人壽-數據分析襄理(機器學習分析模型)新光人壽相信資訊科技是企業競爭力的重要基石，在資訊...
    6     新光人壽-應用系統工程師(客服)(有相關經驗、證照者從優核敘)本單位成員所負責系統維運工作範...
    7     新光人壽-資料工程師(數據分析、資料倉儲、ETL)(有相關經驗、證照者從優核敘)新光人壽相信...
    19    數位金融部-數位平台規劃專員1.數位平台(網路銀行、行動銀行APP)營運管理。2.數位功能需
    """
    seg_list = []
    with open('../conf/stopword.txt', encoding="utf8") as f:
        stopwords = [cleanText(line) for line in f.readlines()] 
        seg_list = [word for word in jieba.cut(cleanText(teststr), cut_all=False) if word not in stopwords]

    print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

    
    
    