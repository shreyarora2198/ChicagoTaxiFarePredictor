#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:30:01 2019

@author: shreyarora
"""

import pandas as pd
import threading
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.neighbors import KNeighborsClassifier

# models
kNN_models = []
for _ in range(12):
    kNN_models.append(KNeighborsClassifier())

# accuracies for each month's model
accuracies = [float]*12

def kNN_train_month(month_num, df):
        
    # target label list
    target = df.filter(['Fare_Label'], axis=1)
    temp_targetlist = target.values.tolist()
    targetlist = []
    for array in temp_targetlist:
        targetlist.append(array[0])
    # data list
    df.drop(['Fare_Label', 'Unnamed: 0'], axis = 1, inplace = True)
    datalist = df.values.tolist()
    # Randomly split data into 66% training and 33% test
    X_train, X_test, y_train, y_test = train_test_split(datalist, targetlist, test_size=.33)    
    # train model
    kNN_models[month_num-1].fit(X_train, y_train)
    # get accuracy of model
    test_results = kNN_models[month_num-1].predict(X_test)
    accuracies[month_num-1] = accuracy_score(y_test, test_results)

def kNN_train():
    # initialize threads for each model
    t1 = threading.Thread(target=kNN_train_month, args=(1, pd.read_csv('../filtered_data/01_January_filtered.csv')))
    t2 = threading.Thread(target=kNN_train_month, args=(2, pd.read_csv('../filtered_data/02_February_filtered.csv')))
    t3 = threading.Thread(target=kNN_train_month, args=(3, pd.read_csv('../filtered_data/03_March_filtered.csv')))
    t4 = threading.Thread(target=kNN_train_month, args=(4, pd.read_csv('../filtered_data/04_April_filtered.csv')))
    t5 = threading.Thread(target=kNN_train_month, args=(5, pd.read_csv('../filtered_data/05_May_filtered.csv')))
    t6 = threading.Thread(target=kNN_train_month, args=(6, pd.read_csv('../filtered_data/06_June_filtered.csv')))
    t7 = threading.Thread(target=kNN_train_month, args=(7, pd.read_csv('../filtered_data/07_July_filtered.csv')))
    t8 = threading.Thread(target=kNN_train_month, args=(8, pd.read_csv('../filtered_data/08_August_filtered.csv')))
    t9 = threading.Thread(target=kNN_train_month, args=(9, pd.read_csv('../filtered_data/09_September_filtered.csv')))
    t10 = threading.Thread(target=kNN_train_month, args=(10, pd.read_csv('../filtered_data/10_October_filtered.csv')))
    t11 = threading.Thread(target=kNN_train_month, args=(11, pd.read_csv('../filtered_data/11_November_filtered.csv')))
    t12 = threading.Thread(target=kNN_train_month, args=(12, pd.read_csv('../filtered_data/12_December_filtered.csv')))
    
    # start each thread
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    
    # join each thread
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()
    t11.join()
    t12.join()

#def predict(trip_seconds, trip_miles, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, time, month, day):
    # example vals
        # trip_seconds: 180
        # trip_miles: 0.4
        # pickup_lat: 599
        # pickup_lon: 346
        # dropoff_lat: 660
        # dropoff_lon: 110
        # time: 375
        # month: 1
        # day: 13
    
     # make a prediction
#     prediction = 
#     return the prediction and the accuracy for that month