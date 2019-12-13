import pandas as pandas
import math 

label = []
#mystring = []
date_and_time = []
complete_date = []
day = []
time = []
totaltime = []
#read in csv file 
df =  pandas.read_csv('../unfiltered_data/chicago_taxi_trips_2016_12.csv')
#takes the first 15% of the csv
df = df.head(int(len(df)*(.15)))
df.dropna(axis = 1, how ='all', inplace = True)
#drop columns not being fed into the model as features 
df.drop(['taxi_id','trip_end_timestamp','dropoff_census_tract','pickup_community_area','dropoff_community_area','tips','tolls','extras','trip_total','payment_type','company'], axis =1, inplace = True)
df.dropna(inplace = True)
#load fares and dates into a list
fare_list = df.loc[: , "fare"]
datetime_list = df.loc[:,"trip_start_timestamp"]
#convert fare into a label between 1-20 
for fare in fare_list :
    result = fare * 0.2
    if (result > 20):
        result = 20
    label.append(math.floor(result))
i = 0
#convert time into a minute in the day 
for row in datetime_list :
    date_and_time.append(row.split(" ",1))
    time.append(date_and_time[i][1].split(":",))
    complete_date.append(date_and_time[i][0].split("-",))
    day.append(complete_date[i][2])
    
    totaltime.append(int(time[i][0])*60 + int(time[i][1]))
    i += 1
#drop the pre-processed fare and trip start time stamp 
df.drop(['trip_start_timestamp', 'fare'], axis =1, inplace = True)

#add new columns to the dataframe containing the processed data 
df['Time'] = totaltime
df['Date'] = day
df['Fare_Label'] = label

#convert the filtered dataframe into a csv for training 
df.to_csv(r'../filtered_data/12_December_filtered.csv')