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

# list to hold distances
dist_arr = []

# list to hold training labels for data visualization
train_label_lists = [[] for x in range(12)]

# accuracies for each month's model
accuracies = [float]*12

# list of models in month order
kNN_models = []
for _ in range(12):
    # Create k-NN classifier: k is 7, distance measure is L2 (Euclidean)
    kNN_models.append(KNeighborsClassifier(n_neighbors=7))

# list of csv filenames in month order
files = []
directory = "../filtered_data"
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        files.append(os.path.join(directory, filename))

# train a single model
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
    train_label_lists[month_num-1] = y_train;
    # train model
    kNN_models[month_num-1].fit(X_train, y_train)
    # get accuracy of model
    test_results = kNN_models[month_num-1].predict(X_test)
    accuracies[month_num-1] = accuracy_score(y_test, test_results)

# train all models, one per month
def kNN_train():
    threads = []
    
    # create one thread per model
    for i in range(12):
        threads.append(threading.Thread(target=kNN_train_month, args=((i+1), pd.read_csv(files[i]))))
    
    # start each thread
    for thread in threads:
        thread.start()
    
    # join each thread
    for thread in threads:
        thread.join()

# convert a label(0-20) to matching fare string
def label_to_fare(label):
    return_str = ""
    first_num = label*5
    second_num = first_num+4
    if label < 20:
        return_str = "$" + str(first_num) + ".00-" + str(second_num) + ".99"
    else:
        return_str = ">$100.00"
    return return_str

# convert an index to label(0-20)
def index_to_label(index_arr, month):    
    all_labels = train_label_lists[month-1]

    labels = []
    for index in index_arr:
        labels.append(all_labels[index])
    
    return labels

# make a prediction, given values and the month (model)
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
    X_test = [[int(trip_seconds), trip_miles, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, time, day]]\
    
    # make a prediction
    prediction = kNN_models[month-1].predict(X_test)
    
    # distances of 7 nearest neighbors
    distances, indices = kNN_models[month-1].kneighbors(X_test, n_neighbors=7, return_distance=True)
    
    # get labels of the 7 nearest neighbors
    labels = index_to_label(indices[0], month)
    
    # convert labels of the 7 nearest neighbors to fares
    fares = []
    for label in labels:
        fares.append(label_to_fare(label))
    
    return label_to_fare(prediction[0]), distances[0], fares

# get the accuracy for a given month and convert it to a string
def get_accuracy(month):
    return str(math.floor(accuracies[month-1]*100)) + "%"