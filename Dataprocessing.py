import pandas as pandas
import math 

label = []
#mystring = []
date_and_time = []
complete_date = []
day = []
time = []
totaltime = []

df =  pandas.read_csv('../unfiltered_data/chicago_taxi_trips_2016_01.csv')
df.dropna(axis = 1, how ='all', inplace = True)

df.drop(['taxi_id','trip_end_timestamp','dropoff_census_tract','pickup_community_area','dropoff_community_area','tips','tolls','extras','trip_total','payment_type','company'], axis =1, inplace = True)
df.dropna(inplace = True)

fare_list = df.loc[: , "fare"]
datetime_list = df.loc[:,"trip_start_timestamp"]

for fare in fare_list :
    result = fare * 0.2
    if (result > 20):
        result = 20
    label.append(math.floor(result))
i = 0
#print(datetime_list[0])
for row in datetime_list :
    date_and_time.append(row.split(" ",1))
    time.append(date_and_time[i][1].split(":",))
    complete_date.append(date_and_time[i][0].split("-",))
    day.append(complete_date[i][2])
    
    totaltime.append(int(time[i][0])*60 + int(time[i][1]))
    i += 1

df.drop(['trip_start_timestamp', 'fare'], axis =1, inplace = True)

df['Time'] = totaltime
df['Date'] = day
df['Fare_Label'] = label

df.to_csv(r'../filtered_data/01_January_filtered.csv')