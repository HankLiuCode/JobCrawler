# coding= utf-8
from Crawler104Modules import Parser104,URLMaker104
from Crawler104Core import Crawler104
import pandas
import jieba
import re

def cleanText(uncleanStr):
    uncleanStr = re.sub(r"\d+"," ",uncleanStr)
    return uncleanStr.replace(' ','').replace('\n','').replace('\r','')

if __name__ == "__main__":
    df = pandas.read_excel("../Data/jobs104_20190816_金融軟體人員_parsed.xlsx")
    df['合併欄位'] = ''
    df['斷詞分析'] = ''
    for i in df.index:
        df.at[i,'合併欄位'] = df.at[i,'工作名稱'] + df.at[i,'工作內容'] + df.at[i,'其他條件']
        df.at[i,'合併欄位'] = df.at[i,'合併欄位'].upper()

        with open('../conf/stopword.txt', encoding="utf8") as f:
            stopwords = [cleanText(line) for line in f.readlines()]
            df.at[i,'斷詞分析'] = ";".join( [word for word in jieba.cut(cleanText(df.at[0,'合併欄位']), cut_all=False) if word not in stopwords] )
    
    print(df.at[0,'斷詞分析'])
    
    teststr = """

    
    """
    seg_list = []
    with open('../conf/stopword.txt', encoding="utf8") as f:
        stopwords = [cleanText(line) for line in f.readlines()]
        seg_list = [word for word in jieba.cut(cleanText(df.at[0,'合併欄位']), cut_all=False) if word not in stopwords]

    print("Default Mode: " + ";".join(seg_list))  # 精确模式
        
    
    
    