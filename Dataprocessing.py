import pandas as pandas
import math 

label = []

df =  pandas.read_csv('test.csv')
df.dropna(axis = 1, how ='all', inplace = True)

df.drop(['taxi_id','trip_end_timestamp','dropoff_census_tract','pickup_community_area','dropoff_community_area','tips','tolls','extras','trip_total','payment_type','company'], axis =1, inplace = True)
df.dropna(inplace = True)
print (df)
list = df.loc[: , "fare"]
#print (list)
i = 0 
for fare in list :
    result = fare * 0.2
    label.append(math.floor(result))
    
df['Fare_Label'] = label