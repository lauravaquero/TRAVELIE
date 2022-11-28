import pandas as pd
import random as rd 

url = "planehotel.csv"

df = pd.read_csv(url, sep=",")
print(df.info())


rd.seed(2022)
hotel_prices = []

number_of_observations = 72
numbers = range(50,400)
hotel_prices.append(rd.sample(numbers,number_of_observations))

ticket_prices = []
ticket_prices.append(rd.sample(numbers,number_of_observations))

df['Hotel price'] = hotel_prices[0]
df['Ticket price'] = ticket_prices[0]

AirPlane_Companies = ['Iberia', 'Air Europa', 'Easy Jet', 'Air France', 'Emirates', 'Poland Airlines']
Train_Companies = ['RENFE', 'AUIGO', 'AUCO']
companies_planes = []
for i in range(number_of_observations):
    companies_planes.append(rd.choice(AirPlane_Companies))

companies_trains = []
for i in range(number_of_observations):
    companies_trains.append(rd.choice(Train_Companies))

mask_train = df['Mode'] == 'Train'
mask_plane = df['Mode'] == 'Plane'

def list_choice(list,n):
    for i in range(n):
        return rd.choices(list,k=n)

df[mask_plane].count() #this will give us the number of travels made by plane
travels_by_plane = 36
travels_by_train = 36

planes_half_dataset = df[mask_plane]
planes_half_dataset['Travel Companies'] = list_choice(AirPlane_Companies,36)
trains_half_dataset = df[mask_train]
trains_half_dataset['Travel Companies'] = list_choice(Train_Companies,36)

travelie_df = pd.concat([planes_half_dataset,trains_half_dataset])

#--------------------------------------------------------------------------------------

routes = travelie_df['Route']
destinations = []
departures = []

for i in routes:
    departures.append(i.split('-')[0])

for i in routes:
    destinations.append(i.split('-')[1])

rd.seed(2022)
travelie_df = travelie_df.rename(columns = {'Route':'Departure'})
travelie_df['Departure'] = departures
travelie_df['Destination'] = list_choice(destinations,72)
travelie_df['Means of transport'] = list_choice(travelie_df['Mode'],72)

travelie_df.drop('Mode', inplace= True, axis = 1)
travelie_df.drop('EcoPassengerCO2', inplace= True, axis = 1)

travelie_df = travelie_df.iloc[:, [0,7,8,6,3,4,5,2,1]]
final_dataset_travelie = travelie_df

final_dataset_travelie