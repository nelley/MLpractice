import random
from sklearn import neighbors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


x1 = np.random.normal(50, 6, 200)   #(center of the distribution, deviation, array size)
y1 = np.random.normal(5, 0.5, 200)

x2 = np.random.normal(30,6,200)
y2 = np.random.normal(4,0.5,200)

x3 = np.random.normal(45,6,200)
y3 = np.random.normal(2.5, 0.5, 200)


#plt.scatter(x1,y1,c='b',marker='s',s=50,alpha=0.8)
#plt.scatter(x2,y2,c='r', marker='^', s=50, alpha=0.8)
#plt.scatter(x3,y3, c='g', s=50, alpha=0.8)

x_val = np.concatenate((x1,x2,x3))
y_val = np.concatenate((y1,y2,y3))


x_diff = max(x_val)-min(x_val)
y_diff = max(y_val)-min(y_val)

x_normalized = [x/(x_diff) for x in x_val]
y_normalized = [y/(y_diff) for y in y_val]
xy_normalized = zip(x_normalized,y_normalized)


labels = [1]*200+[2]*200+[3]*200
clf = neighbors.KNeighborsClassifier(1)

# calculate model
clf.fit(xy_normalized, labels)

#plt.show()
nearests = clf.kneighbors([(50/x_diff, 5/y_diff),(30/x_diff, 3/y_diff)], 10, False)
print nearests

prediction = clf.predict([(50/x_diff, 5/y_diff),(30/x_diff, 3/y_diff)])
print prediction    #output represents the category 1 or 2 or 3 with (50,5) (30,3)

prediction_proba = clf.predict_proba([(50/x_diff, 5/y_diff),(30/x_diff, 3/y_diff)])
print prediction_proba

#=============================
#test data generation
#=============================
x1_test = np.random.normal(50, 6, 100)
y1_test = np.random.normal(5, 0.5, 100)

x2_test = np.random.normal(30,6,100)
y2_test = np.random.normal(4,0.5,100)

x3_test = np.random.normal(45,6,100)
y3_test = np.random.normal(2.5, 0.5, 100)

xy_test_normalized = zip(np.concatenate((x1_test,x2_test,x3_test))/x_diff,\
                        np.concatenate((y1_test,y2_test,y3_test))/y_diff)

labels_test = [1]*100+[2]*100+[3]*100

score = clf.score(xy_test_normalized, labels_test)
print score

#====================
#generate graph
#====================
xx,yy = np.meshgrid(np.arange(1,70.1,0.1), np.arange(1,7.01,0.01))


xx_normalized = xx/x_diff
yy_normalized = yy/y_diff

coords = np.c_[xx_normalized.ravel(), yy_normalized.ravel()]


Z = clf.predict(coords)
Z = Z.reshape(xx.shape)


light_rgb = ListedColormap([ '#AAAAFF', '#FFAAAA','#AAFFAA'])
plt.pcolormesh(xx, yy, Z, cmap=light_rgb)
plt.scatter(x1,y1,c='b',marker='s',s=50,alpha=0.8)
plt.scatter(x2,y2,c='r', marker='^', s=50, alpha=0.8)
plt.scatter(x3,y3, c='g', s=50, alpha=0.8)
plt.axis((10, 70,1,7))


plt.show()
