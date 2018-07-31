#-*- coding:utf-8 -*-
import re
import MeCab
from bson.code import Code
from pymongo import MongoClient
from subprocess import Popen, PIPE
import sys
import pdb
from zhon.hanzi import punctuation
import unicodedata

reload(sys)
sys.setdefaultencoding("utf-8")

pdb.set_trace()
mt = MeCab.Tagger("-Owakati")
#mt = MeCab.Tagger("mecabrc -d /home/nelley/MLpractice/mecab/final/")
#mt = MeCab.Tagger("mecabrc")

#SPLIT_DELEMITER = ' |-|,|\n|，|。|：|、'
REG_IPADDR = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
REG_URL = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
REG_DT1 = '((0[1-9]|10|11|12)\/([0-2][0-9]|30|31)\/\d{4}\s([0-1][0-9]|20|21|22|23)\:[0-5][0-9]\:[0-5][0-9])'
#REG_DT2 = '((Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*([1-2]?[0-9]|30|31)\s*([0-1][0-9]|20|21|22|23)\:[0-5][0-9]\:[0-5][0-9]\s\d{4})'
          #((Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s([0-2][0-9]|30|31)\s([0-1][0-9]|20|21|22|23)\:[0-5][0-9]\:[0-5][0-9]\s\d{4})
REG_DT2 = '\D{3}\s\D{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s\d{4}'
REG_DT_NO_WEEKDAY = '\d{1,2}/\d{1,2}/\d{4}\s+\d{2}:\d{2}:\d{2}'
REG_PUSH = u'\u63a8'

#FINAL_REG = '(' + REG_IPADDR + '|' + REG_URL + '|' + REG_TS1 + '|' + ')'
#FINAL_REG = '(' + REG_IPADDR + '|' + REG_URL + ')'
FINAL_REG = '(' + REG_DT2 + '|' + REG_DT_NO_WEEKDAY + '|' + REG_IPADDR + '|' + REG_URL + ')'


def get_db():
    client = MongoClient('192.168.8.129:27017')
    db = client.PTT
    db.authenticate("root", "notsniw0405", source="admin")
    return db

def fullToHalfWidth(str_origin):
    #print unicodedata.normalize('NFKC', str_origin)
    return unicodedata.normalize('NFKC', str_origin)


def regex_date(str_rex):
    #compi = re.compile(REG_DT2).split(str_rex)
    #print compi
    #target = re.findall(compi, str_rex)
    # empty list check needed
    #print target
    #print re.split('(' + REG_DT_NO_WEEKDAY + ')', TEST_STR)
    print re.split('(' + REG_PUSH + ')', str_rex)


    #tmp =  fullToHalfWidth(str_rex)
    #print re.compile(u'\u63a8', re.UNICODE).split(tmp)


if __name__ == '__main__':

    conn = get_db()
    posts = conn.Posts
    posts_salary = posts.find({"category":"salary"}).sort("post_time",-1).limit(5)
    #posts_salary = posts.find({"category":"tech_job"}).sort("post_time",-1).limit(5)
    #posts_salary = posts.find({"category":"gossip"}).sort("post_time",-1).limit(5)

    post_ele_list = []

    for idx, post in enumerate(posts_salary):
        tmp = re.split(FINAL_REG, str(post['content']))
        print 'len=%s, type=%s' % (len(tmp), type(tmp))
        print '-----------------------------------'
        post_ele_list.append(tmp)
        #post_ele_list.append(list(mt.parse(str(post['content'])).split(' ')))

    print 'list len=%s' % len(post_ele_list)
    #print ','.join(str(ele) for ele in post_ele_list)
    for ele in post_ele_list:
        for e in ele:
            print e
        print '--------------------------' 
    TEST_STR = 'asdf推→噓sdfakiuyasghlhttpi10/21/2017 23:44:40kkjhrtkjkiukgyu766754１２３４５６７８９０ss。。Ｈ５Ｎ２'
    #TEST_STR = 'sdfakiuyasghlhttpiiSun Sep  9 23:44:40 2007kkjhrtkjkiukgyu766754Sun Jan 19 23:43:41 2017dfgarga'
    #fullToHalfWidth(unicode(TEST_STR))
    regex_date(unicode(TEST_STR, 'utf-8'))


