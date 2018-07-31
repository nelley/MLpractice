###########################################
############## SEEDS DATASET ##############
###########################################
import pdb
import numpy as np
from load import load_dataset


pdb.set_trace()
feature_names = [
    'area',
    'perimeter',
    'compactness',
    'length of kernel',
    'width of kernel',
    'asymmetry coefficien',
    'length of kernel groove',
]
features, labels = load_dataset('seeds')
#print features


from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=1)
from sklearn.cross_validation import KFold

# KFold provides train/test indices
kf = KFold(len(features), n_folds=5, shuffle=True)
means = []
for training,testing in kf:
   # We learn a model for this fold with `fit` and then apply it to the
   # testing data with `predict`:
   classifier.fit(features[training], labels[training]) #arg1 as training data, arg2 as training data's label
   prediction = classifier.predict(features[testing])
   #predict_proba = classifier.predict_proba(features[testing])
   
   # np.mean on an array of booleans returns fraction
   # of correct decisions for this fold:
   curmean = np.mean(prediction == labels[testing])
   means.append(curmean)
print('Mean accuracy: {:.1%}'.format(np.mean(means)))


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

classifier = KNeighborsClassifier(n_neighbors=1)
classifier = Pipeline([('norm', StandardScaler()), ('knn', classifier)])

means = []
for training,testing in kf:
    # We learn a model for this fold with `fit` and then apply it to the
    # testing data with `predict`:
    classifier.fit(features[training], labels[training])
    prediction = classifier.predict(features[testing])

    # np.mean on an array of booleans returns fraction
    # of correct decisions for this fold:
    curmean = np.mean(prediction == labels[testing])
    means.append(curmean)
print('Mean accuracy: {:.1%}'.format(np.mean(means)))
