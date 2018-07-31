# -*- coding= utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

text = [
    ["the", "dog", "run", ],
    ["a", "cat", "run", ],
    ["a", "dog", "sleep", ],
    ["the", "cat", "sleep", ],
    ["a", "dog", "bark", ],
    ["the", "cat", "meows", ],
    ["the", "bird", "fly", ],
    ["a", "bird", "sleep", ],
    ["the", "Winston", "run", "fast", "and", "handsome"],
    ["the", "Winston", "sleep"]
]

def build_word_vector(text):
    #reduce(lambda a,b : a+b, text)會依序拆開array, 並將其中的string接起來
    #set()去掉相同的元素
    #w:i for i,w in enumerate()是直接產出一個dict的意思
    word2id = {w: i for i, w in enumerate(sorted(list(set(reduce(lambda a, b: a + b, text)))))}
    #dict.items()return a copy of dict
    id2word = {x[1]: x[0] for x in word2id.items()}
    #create narray with 0
    wvectors = np.zeros((len(word2id), len(word2id)))
    for sentence in text:
        print 'sentence=%s' % sentence
        #sentence[:-1] means get rid of last element
        #sentence[1:] means get rid of first element
        for word1, word2 in zip(sentence[:-1], sentence[1:]):
            id1, id2 = word2id[word1], word2id[word2]
            wvectors[id1, id2] += 1
            wvectors[id2, id1] += 1
    return wvectors, word2id, id2word


def cosine_sim(v1, v2):
    return np.dot(v1, v2) / (np.sqrt(np.sum(np.power(v1, 2))) * np.sqrt(np.sum(np.power(v1, 2))))


def visualize(wvectors, id2word):
    np.random.seed(10)
    fig = plt.figure()
    U, sigma, Vh = np.linalg.svd(wvectors)
    ax = fig.add_subplot(111)
    ax.axis([-1, 1, -1, 1])
    for i in id2word:
        ax.text(U[i, 0], U[i, 1], id2word[i], alpha=0.3, fontsize=20)
    plt.show()

wvectors, word2id, id2word = build_word_vector(text)
print wvectors
#visualize(wvectors, id2word)

#print cosine_sim(wvectors[word2id["dog"]], wvectors[word2id["Winston"]])
#print word2id
#print wvectors[word2id["Winston"]]
