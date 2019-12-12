#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:30:01 2019

@author: shreyarora
"""

import pandas as pd
import threading
import math
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

dist_arr = []

train_label_lists = []

# models
kNN_models = []
for _ in range(12):
    # Create k-NN classifier: k is 3, distance measure is L2 (Euclidean)
    kNN_models.append(KNeighborsClassifier(n_neighbors=7))

# accuracies for each month's model
accuracies = [float]*12

# files
files = []
directory = "../filtered_data"
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        files.append(os.path.join(directory, filename))

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
    # add the training label list
    train_label_lists.append(y_train);
    # train model
    kNN_models[month_num-1].fit(X_train, y_train)
    # get accuracy of model
    test_results = kNN_models[month_num-1].predict(X_test)
    accuracies[month_num-1] = accuracy_score(y_test, test_results)

def kNN_train():
    # initialize threads for each model
    t1 = threading.Thread(target=kNN_train_month, args=(1, pd.read_csv(files[0])))
    t2 = threading.Thread(target=kNN_train_month, args=(2, pd.read_csv(files[1])))
    t3 = threading.Thread(target=kNN_train_month, args=(3, pd.read_csv(files[2])))
    t4 = threading.Thread(target=kNN_train_month, args=(4, pd.read_csv(files[3])))
    t5 = threading.Thread(target=kNN_train_month, args=(5, pd.read_csv(files[4])))
    t6 = threading.Thread(target=kNN_train_month, args=(6, pd.read_csv(files[5])))
    t7 = threading.Thread(target=kNN_train_month, args=(7, pd.read_csv(files[6])))
    t8 = threading.Thread(target=kNN_train_month, args=(8, pd.read_csv(files[7])))
    t9 = threading.Thread(target=kNN_train_month, args=(9, pd.read_csv(files[8])))
    t10 = threading.Thread(target=kNN_train_month, args=(10, pd.read_csv(files[9])))
    t11 = threading.Thread(target=kNN_train_month, args=(11, pd.read_csv(files[10])))
    t12 = threading.Thread(target=kNN_train_month, args=(12, pd.read_csv(files[11])))
    
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
    
def label_to_fare(label):
    return_str = ""
    first_num = label*5
    second_num = first_num+4
    if label < 20:
        return_str = "$" + str(first_num) + ".00-" + str(second_num) + ".99"
    else:
        return_str = ">$100.00"
    return return_str

def index_to_label(index_arr, month):
#    all_labels = pd.read_csv(files[month-1]).filter(['Fare_Label'], axis=1).values.tolist()
    
    all_labels = train_label_lists[month-1]

    labels = []
    for index in index_arr:
        labels.append(all_labels[index])
    
    return labels

def predict(trip_seconds, trip_miles, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, time, month, day):
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
    
    # create test data and label
    X_test = [[int(trip_seconds), trip_miles, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, time, day]]
    # make a prediction
    prediction = kNN_models[month-1].predict(X_test)
    
    # distances of five nearest neighbors
    distances, indices = kNN_models[month-1].kneighbors(X_test, n_neighbors=7, return_distance=True)
    
    labels = index_to_label(indices[0], month)
    
    fares = []
    for label in labels:
        fares.append(label_to_fare(label))
    
    return label_to_fare(prediction[0]), distances[0], fares

def get_accuracy(month):
    return str(math.floor(accuracies[month-1]*100)) + "%"