#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:30:01 2019

@author: shreyarora
"""

import pandas as pd
import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.neighbors import KNeighborsClassifier

# models
kNN_01 = KNeighborsClassifier()
kNN_02 = KNeighborsClassifier()
kNN_03 = KNeighborsClassifier()
kNN_04 = KNeighborsClassifier()
kNN_05 = KNeighborsClassifier()
kNN_06 = KNeighborsClassifier()
kNN_07 = KNeighborsClassifier()
kNN_08 = KNeighborsClassifier()
kNN_09 = KNeighborsClassifier()
kNN_10 = KNeighborsClassifier()
kNN_11 = KNeighborsClassifier()
kNN_12 = KNeighborsClassifier()

accuracies = [float]*12

def kNN_train_month(month_num, df, model):
    
    ## REMOVE START
    df.head(int(len(df)*(.15)))
    ## REMOVE END
    
    # target label list
    target = df.filter(['Fare_Label'], axis=1)
    temp_targetlist = target.values.tolist()
    targetlist = []
    for array in temp_targetlist:
        targetlist.append(array[0])
    # data list
    df.drop(['Fare_Label', 'Unnamed: 0'], axis = 1, inplace = True)
    datalist = df.values.tolist()
    # Randomly split data into 90% training and 10% test
    
    ## EDIT START
    X_train, X_test, y_train, y_test = train_test_split(datalist, targetlist, test_size=.33)
    ## EDIT END
    
    # train model
    model.fit(X_train, y_train)
    # get accuracy of model
    test_results = model.predict(X_test)
    accuracies[month_num-1] = accuracy_score(y_test, test_results)

def kNN_train():
    # train a model for each month
    
    # January
    df = pd.read_csv('../filtered_data/01_January_filtered.csv')
    kNN_train_month(1,df,kNN_01)
    
    # February
    df = pd.read_csv('../filtered_data/02_February_filtered.csv')
    kNN_train_month(2,df,kNN_02)
    
    # March
    df = pd.read_csv('../filtered_data/03_March_filtered.csv')
    kNN_train_month(3,df,kNN_03)
    
    
st = datetime.datetime.now()
kNN_train()
et = datetime.datetime.now()
print("Total time: " + str(et-st))
print("Jan Accuracy: " + str(accuracies[0]))
print("Feb Accuracy: " + str(accuracies[1]))
print("Mar Accuracy: " + str(accuracies[2]))