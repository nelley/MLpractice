# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import MeCab
import pdb
from collections import defaultdict
from gensim import corpora, models
import matplotlib.pyplot as plt
import numpy as np

stoplist = set('的 ， 。 ！ 『 』 「 」 、'.split())
documents = ["你很難想像，這一名年僅24歲的年輕控衛，他超齡的成熟穩定，幾乎主宰整個場上節奏， 他流暢的快攻、處理球的視野、關鍵時刻的發揮，實在讓人很難把他跟他的年紀相連結。 隨著黃金世代淡出台灣籃壇，陳盈駿用樸實球風，虔誠倚靠上帝加給他的力量，問鼎新世 代、華麗登場。",
                "許多球迷十分納悶，陳盈駿明明擁有國家一隊控衛的實力，今年為什麼被分配到世大運培 訓隊？作為世大運培訓隊領導者，陳盈駿沒沒有想這麼多，他很樂意、也很高興能為世大 運效力，也盼用實際行動影響隊友，積極用心作好場上工作，一路把士氣帶到世大運。「 少說多作，身體力行影響隊友，大家這段時間集訓也都表現很好，團隊凝聚力很強。」",
                "陳盈駿說，不管是在中華藍還是中華白，兩邊都有不同的收穫學習。在藍隊，他是學弟， 多觀察、多聽多看、虛心討教；在白隊，他是Leader，以身作則、作團隊的榜樣、帶領年 輕世代一步一步成長。「這兩年能打國家隊都是一種榮譽，所以不管在哪裡，心理層面都 有很大成長。」",
                "瓊斯盃首戰後，陳盈駿用26分7籃板8助攻揭開年輕世代新篇章，今年陳盈駿卸下國家隊一 線主控的光環，投身世大運培訓隊，用另一種姿態扮演球隊佼佼者，為年輕世代挹注全新 能量。",
                "馬林魚隊43歲日籍野手鈴木一朗是目前大聯盟現役最資深球員，16日他代打出擊，並且敲出適時內野安打建功",
                "波士頓塞爾提克今天與『真理』Paul Pierce簽下一日合約，讓這位綠衫軍的代表性人物能夠回到東區老家光榮退役",
                "已故藝人高凌風的兒子「寶弟」，近年積極投入演藝圈的工作",
                "對於子女都在外地打拚的長輩們來說，如果能夠養隻小貓、小狗來互動的話，不但感情上有所慰藉，對身心健康也很有幫助吧！",
                "登上大聯盟後，林子偉不到1個月時間3度演出猛打賞，頓時成了「台灣之光」",
                "其實，林子偉在小聯盟也曾經歷多年低潮，直到他從釣魚中悟出一番哲學"]
#mt = MeCab.Tagger('mecabrc')
mt = MeCab.Tagger('-Owakati')

if __name__ == '__main__':
    pdb.set_trace()
    word_list = []
    #for doc in documents:
        #print type(mt.parse(doc))
        #x.append(list(mt.parse(doc).split()))
    #word_list.append([w for w in list(mt.parse(doc).split()) if w not in stoplist] for doc in documents)
    # 形態素解析
    word_list = [[w for w in list(mt.parse(doc).split()) if w not in stoplist] for doc in documents]
    print word_list
    # remove word and tokenize
    frequency = defaultdict(int) 
    for word in word_list:
        for ele in word:
            frequency[str(ele)] += 1

    #for k, value in frequency.iteritems():
    #    print '%s, %s' % (str(k).decode('string_escape'), value)

    word_list = [[ele for ele in word if frequency[str(ele)] > 1] for word in word_list]

    #for word in word_list:
    #    print str(word).decode('string_escape')
   
    # store dict for future use(unique token) 
    dictionary = corpora.Dictionary(word_list)
    dictionary.save('/home/nelley/MLpractice/test.dict')
    #for k, v in dictionary.iteritems():
    #    print '%s, %s' % (k, v)

    # count the num of occurence of each word. corpus is the set of vectors
    corpus = [dictionary.doc2bow(word) for word in word_list]
    corpora.MmCorpus.serialize('/home/nelley/MLpractice/test_corpus.mm', corpus)
    
    corpus_loaded = corpora.MmCorpus('/home/nelley/MLpractice/test_corpus.mm')
    #print (corpus_loaded)

    # keep the topic consistent
    np.random.seed(15)
    model = models.ldamodel.LdaModel(corpus_loaded, num_topics = 2, id2word=dictionary)
    check_topic_elements = model.print_topics(num_topics=2, num_words=5)
    for ele in check_topic_elements:
        print str(ele[1]).decode('string_escape')

    topics = [model[c] for c in corpus_loaded]
    print topics[0]
    # Iterate over all the topics in the model
    for ti in range(model.num_topics):  # 5 topics
        words = model.show_topic(ti, 100)   #get words contain in dictionary for each topics
        tf = sum(f for _, f in words)
        with open('topics_test.txt', 'w') as output:
            output.write('\n'.join('{}:{}'.format(w, int(1000. * f / tf)) for w, f in words))
            output.write("\n\n\n")


