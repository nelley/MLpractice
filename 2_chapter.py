# -*- coding: utf-8 -*-
import pdb
from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
import numpy as np

pdb.set_trace()
#load the data from scikit-learn
data = load_iris()
features = data['data']
feature_names = data['feature_names']

#definition of target
#0:setosa
#1:versicolor
#2:virginica
target = data['target']

#print features
#print feature_names
#print "target=%s" % target
#print features[True]
#print features[target == 3, 0] #return a dict contains a list

#zip= iterate two objects in parallel
'''
for t, marker, c in zip(xrange(3), ">ox", "rgb"):
    #print "t=%s, marker=%s, c=%s" % (t, marker, c)
    plt.scatter(features[target == t,2], #x axis
                features[target == t,3], #y axis
                marker = marker,        #marker style show on the graph
                c=c
                )
    #print features[target == t,2]

plt.xlabel("sepal length(cm)")
plt.ylabel("sepal width(cm)")
plt.show()
'''
#: means all element in the 2D array
#2 means element 2 in the 1D array
plength = features[:, 2]

#numpy operation below
tmp = (data['target_names'][value] for value in data ['target'])
labels = np.array(list(tmp))

#create an array with True which elements equal to 'setosa', and others as False
is_setosa = (labels == 'setosa')

max_setosa = plength[is_setosa].max()
min_non_setosa = plength[~is_setosa].min()
print format(max_setosa)
print format(min_non_setosa)


#if features[:,2] < 2: print 'iris setosa'
#else: print 'iris versicolor or iris virginica'

features = features[~is_setosa]
labels = labels[~is_setosa]
virginica = (labels == 'virginica')

# seperate virginica & versicolor
best_acc = -1.0
#generate all possible threshold for this feature
#shape[1][0]=sepal_length
#shape[1][1]=sepal_width
#shape[1][2]=petal_length
#shape[1][3]=petal_width
best_acc = -1
for fi in xrange(features.shape[1]):
    thresh = features[:,fi].copy()
    thresh.sort()   # each thresh represents for sepal/petal's length/width in 4 array
    # now test all thresh
    for t in thresh:
        #找出virginica佔比例最高的thresh值
        pred = (features[:,fi] > t)
        acc = (pred==virginica).mean()
        rev_acc = (pred == ~virginica).mean()
        if rev_acc > acc:
            reverse = True
            acc = rev_acc
        else:
            reverse = False

        #print acc
        if acc > best_acc:
            best_acc = acc
            best_fi = fi
            best_t = t
            best_reverse = reverse
print(best_fi, best_t, best_reverse, best_acc)

def is_virginica_test(fi, t, reverse, example):
    'Apply threshold model to a new example'
    test = example[fi] > t
    if reverse:
        test = not test
    return test

#---------------------------------------
# leave one out cross validation
#---------------------------------------
from threshold import fit_model, predict

# ning accuracy was 96.0%.
# ing accuracy was 90.0% (N = 50).
correct = 0.0

for ei in range(len(features)):
    # select all but the one at position `ei`:
    training = np.ones(len(features), bool) #create a all True array
    training[ei] = False
    # create a reverse array of training array
    testing = ~training
    model = fit_model(features[training], virginica[training])
    predictions = predict(model, features[testing])
    correct += np.sum(predictions == virginica[testing]) 

acc = correct/float(len(features))
print('Accuracy: {0:.1%}'.format(acc))



