import pandas as pandas
import math 

label = []
#mystring = []
time = []
time2 = []
totaltime = []

df =  pandas.read_csv('test.csv')
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
for row in datetime_list :
    time.append(row.split(" ",1))
    time2.append(time[i][1].split(":",))
    totaltime.append(int(time2[i][0])*60 + int(time2[i][1]))
    i += 1
 
df['Fare_Label'] = label
df['Time_Label'] = totaltime 