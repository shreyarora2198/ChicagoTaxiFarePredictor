#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:30:01 2019

@author: shreyarora
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def kNN_prediction():
        
    # Randomly split data into 70% training and 30% test
    X_train, X_test, y_train, y_test = train_test_split(datalist, targetlist, test_size=.20)
    
    # Train a kNN model using the training set
    clf_KNN = KNeighborsClassifier()
    clf_KNN.fit(X_train, y_train)
    
    # Predictions using the kNN model on the test set
    print("Predicting labels of the test data set - %i random samples" % (len(X_test)))
    result = clf_KNN.predict(X_test)
    
    return str(accuracy_score(y_test, result))

df =  pd.read_csv('../filtered_data/01_January_filtered.csv')

target = df.filter(['Fare_Label'], axis=1)
df.drop(['Fare_Label'], axis = 1, inplace = True)

datalist = df.values.tolist()
targetlist = target.values.tolist()

print("kNN accuracy: " + kNN_prediction())