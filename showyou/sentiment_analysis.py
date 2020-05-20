#from . import mongo_connection

import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from . import mongo_connection

#리스트 전부 가져오기
def Sentiment_Analysis():
    sentiment_list = mongo_connection.sentiment_analysis_result_find()
    textmining_list = mongo_connection.textmining_result_find()


    #post_id /긍정(+1),부정(-1),중립(0) 받아오기
    sentiment_data =[]
    sentiment_post_id = []
    for i in sentiment_list:
        sentiment_post_id.append(i['post_id'])
        sentiment_data.append(i['sentiment'])

    # post_id / keyword받아오기
    keyword_list =[]
    post_id = []
    for i in textmining_list:
        post_id.append(i['post_id'])
        keyword_list.append(i['keyword'])

    #keyword가 key이고 post_id가 value인 딕셔너리

    # 합친 딕션너리
    d1 = {}
    d1 = dict(zip(post_id,keyword_list))

    d2 = {}
    d2 = dict(zip(sentiment_post_id,sentiment_data))


    #키워드에 따른 빈도수 구하기
    all={} #{키워드: 빈도}의 순서쌍
    positive={}#{키워드: 긍정의 빈도}의 순서쌍
    neutral = {} #{키워드: 중립의 빈도}의 순서쌍
    negative = {}#{키워드: 부정의 빈도}의 순서쌍

    for i in post_id: #i는 배열의 한 item
        keywords = d1[i]
        sentiment = d2[i]
        for j in keywords:
            keyword=j


            #키워드가 한 딕셔너리에 없다면 다른 딕셔너리들에도 없음
            if(keyword not in all.keys()):
                all[keyword]=0
                negative[keyword]=0
                neutral[keyword]=0
                positive[keyword]=0

            all[keyword]+=1

            if(sentiment==-1):
                negative[keyword]+=1

            if(sentiment==0):
                neutral[keyword]+=1

            if(sentiment==1):
                positive[keyword]+=1

    print("all")
    print(all)
    print("positive")
    print(positive)
    print("negative")
    print(negative)
    print("neutral")
    print(neutral)
