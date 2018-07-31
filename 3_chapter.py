# -*- coding=utf-8 -*-
import os
import sys
from sklearn.feature_extraction.text import CountVectorizer
import scipy as sp
import pdb

pdb.set_trace()

def dist_raw(v1, v2):
    delta = v1 - v2
    return sp.linalg.norm(delta.toarray())

def dist_norm(v1, v2):
    #sp.linalg.norm() is calculated for Euclidean distance
    #實際的操作是把矩陣中所有的元素平方加總後開更號
    v1_normalized = v1 / sp.linalg.norm(v1.toarray())
    v2_normalized = v2 / sp.linalg.norm(v2.toarray())

    delta = v1_normalized - v2_normalized

    return sp.linalg.norm(delta.toarray())

dist = dist_norm


#content = ['how to format my hard disk', ' hard disk format problems format format', 'format format winston']
#vectorizer = CountVectorizer(min_df=2, max_df=0.7)
#X = vectorizer.fit_transform(content)
#print vectorizer.get_feature_names()

#vectorizer = CountVectorizer(min_df=1, stop_words='english')
print vectorizer.get_stop_words()

TOY_DIR ="/home/nelley/MLpractice/data/toy" 
posts = [open(os.path.join(TOY_DIR, f)).read() for f in os.listdir(TOY_DIR)]

import nltk.stem
english_stemmer = nltk.stem.SnowballStemmer('english')

class StemmedCountVectorizer(CountVectorizer):

    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedCountVectorizer(min_df=1, stop_words='english')

#print english_stemmer.stem('talking')


from sklearn.feature_extraction.text import TfidfVectorizer


class StemmedTfidfVectorizer(TfidfVectorizer):

    def build_analyzer(self):
        analyzer = super(StemmedTfidfVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedTfidfVectorizer(
    min_df=1, stop_words='english', decode_error='ignore')


X_train = vectorizer.fit_transform(posts)

number_samples, number_features = X_train.shape
print vectorizer.get_feature_names()

new_post = "imaging databases"
new_post_vec = vectorizer.transform([new_post])
print (new_post_vec)    #可以得出new_post跟X_train的單字重複的部份



best_doc = None
best_dist = sys.maxint
best_i = None
for i in range(0, number_samples):
    post = posts[i]
    if post == new_post:
        continue
    post_vec = X_train.getrow(i)
    d = dist(post_vec, new_post_vec)

    print("=== Post %i with dist=%.2f: %s" % (i, d, post))

    if d < best_dist:
        best_dist = d
        best_i = i

print("Best post is %i with dist=%.2f" % (best_i, best_dist))


print X_train.getrow(3).toarray()
print X_train.getrow(4).toarray()
'''
print (X.toarray())
print (X.toarray().transpose())
'''

