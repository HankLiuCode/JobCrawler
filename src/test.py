import jieba
import jieba.analyse



test=jieba.analyse.extract_tags(mystr,topK=10)
print(test)