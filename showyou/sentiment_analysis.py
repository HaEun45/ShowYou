import matplotlib.pyplot as plt
import numpy as np
import matplotlib

from . import mongo_connection

#window경우 한글폰트설정
#matplotlib.rc('font', family='HYsanB')

#mac의 경우 한글폰트설정
matplotlib.rc('font', family='AppleGothic')

def __init__():
    return True

def __path():
    return True
#리스트 전부 가져오기
def Sentiment_Analysis():
    sentiment_list = mongo_connection.sentiment_analysis_result_find()
    textmining_list = mongo_connection.textmining_result_find()


    #post_id /긍정(+1),부정(-1),중립(0) 받아오기
    sentiment_data =[]
    for i in sentiment_list:
        sentiment_data.append(i['sentiment'])

    # post_id / keyword받아오기
    keyword_list =[]
    post_id = []
    for i in textmining_list:
        post_id.append(i['post_id'])
        keyword_list.append(i['keyword'])

    #for i in post_id:
    #    print(i, '/', keyword_list[i], '/', sentiment_data[i])


    # 합친 딕션너리
    post_id_to_keywords = dict(zip(post_id,keyword_list))
    post_id_to_sentiment = dict(zip(post_id,sentiment_data))
#    print(post_id_to_keywords)
#    print(post_id_to_sentiment)

    #키워드에 따른 빈도수 구하기
    keywords = [] #모든 키워드들의 집합
    count={} #{키워드: 빈도}의 순서쌍
    positive={}#{키워드: 긍정의 빈도}의 순서쌍
    neutral = {} #{키워드: 중립의 빈도}의 순서쌍
    negative = {}#{키워드: 부정의 빈도}의 순서쌍

    for post_id in post_id:
        for keyword in post_id_to_keywords[post_id]:
            if(keyword not in keywords):
                keywords.append(keyword)
                count[keyword] = 0
                negative[keyword] = 0
                neutral[keyword] = 0
                positive[keyword] = 0

            count[keyword] += 1
            senti = post_id_to_sentiment[post_id]

            if(senti == 1):
                positive[keyword] += 1
            elif(senti == 0):
                neutral[keyword] += 1
            else:
                negative[keyword] += 1

    sentiment = {}

    for k in list(keywords):
        if(positive[k] > negative[k] and positive[k]>neutral[k]):
            sentiment[k] = 1
        elif(negative[k]>positive[k] and negative[k]>neutral[k]):
            sentiment[k] = -1
        else:
            sentiment[k] = 0



    input_keywords = keywords[59:73]
    input_count = dict(list(count.items())[59:73])
    input_sentiment = dict(list(sentiment.items())[59:73])

    print(input_keywords)
    print(input_count)
    print(input_sentiment)

    #원그래프 만들기!!
    #r = np.random.randiant(5,15,size=10)
    r = list(count.values())


    class C():
        def __init__(self,r):
            self.N = len(r)
            self.x = np.ones((self.N,3))
            self.x[:,2] = r
            maxstep = 2*self.x[:,2].max()
            length = np.ceil(np.sqrt(self.N))
            grid = np.arange(0,length*maxstep,maxstep)
            gx,gy = np.meshgrid(grid,grid)
            self.x[:,0] = gx.flatten()[:self.N]
            self.x[:,1] = gy.flatten()[:self.N]
            self.x[:,:2] = self.x[:,:2] - np.mean(self.x[:,:2], axis=0)

            self.step = self.x[:,2].min()
            self.p = lambda x,y: np.sum((x**2+y**2)**2)
            self.E = self.energy()
            self.iter = 1.

        def minimize(self):
            while self.iter < 1000*self.N:
                for i in range(self.N):
                    rand = np.random.randn(2)*self.step/self.iter
                    self.x[i,:2] += rand
                    e = self.energy()
                    if (e < self.E and self.isvalid(i)):
                        self.E = e
                        self.iter = 1.
                    else:
                        self.x[i,:2] -= rand
                        self.iter += 1.

        def energy(self):
            return self.p(self.x[:,0], self.x[:,1])

        def distance(self,x1,x2):
            return np.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)-x1[2]-x2[2]

        def isvalid(self, i):
            for j in range(self.N):
                if i!=j:
                    if self.distance(self.x[i,:], self.x[j,:]) < 0:
                        return False
            return True

        def plot(self, ax):
            index=0
            for i in range(self.N):
                keyword=input_keywords[index]
                if(input_sentiment[keyword]==1):
                    color='orange'
                elif(input_sentiment[keyword]==0):
                    color='salmon'
                else:
                    color='skyblue'

                circ = plt.Circle(self.x[i,:2],self.x[i,2], color = color)
                ax.add_patch(circ)
                ax.annotate(keyword, xy=(self.x[i,:2]), fontsize=10, ha="center")
                index += 1

    c = C(r)

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    ax.axis("off")

    c.minimize()

    c.plot(ax)
    ax.relim()
    ax.autoscale_view()
    plt.savefig('sentiment1_plt.png')
    pylab.savefig('sentiment2_pylab.png')
    fig.savefig('sentiment3_fig.png')
    #print("이미지 저장해줭제바루")
    #fig.savefig('sentiment1.png')
    #plt.show()

    #fig.close()
