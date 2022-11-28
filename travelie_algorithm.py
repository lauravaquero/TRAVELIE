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

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#Up to this point, everything was done in the travelie_dataset.py script.

def quicksort(array):
    high = []
    low = []
    if len(array) < 2: 
        return array
    else:
        pivot = rd.choice(array)
        for i in array:
            if i < pivot: 
                low.append(i)
            elif i > pivot:
                high.append(i)
        return quicksort(low) + [pivot] + quicksort(high)


print('Welcome to Travelie!')
account = input('Do you want to sign in or create an account?')
account = account.lower()

if account == 'sign in':
    username = input('Introduce your usernme: ')
    password = input('Introduce your password: ')
            
elif account == 'create an account':
    username = input('Introduce your usernme: ')
    password = input('Introduce your password: ')
        
else:
    print('Please, try again and specify either SIGN IN or CREATE AN ACCOUNT. ')


print(f'Hello, {username}! \nBefore we start your journey, let us ask you some quick questions! ')

departure = input(f'{username}, where are you traveling from? - Beware first capital letters must be used')
destination = input(f'{username}, Where would you like to travel? - Beware first capital letters must be used ')
budget = int(input(f'{username}, what is the budget you had in mind for your trip? '))
means_of_transport = input(f'{username}, are you traveling by Plane or Train? - Beware first capital letters must be used ')
stay_duration = int(input(f'{username}, how many days will you be staying (nights only) '))
sorting_criteria = input(f'{username}, would you rather pay more for the {means_of_transport} ticket and have a worse experience in the hotel?\nPLEASE, JUST ANSWER "YES", "NO" OR "MIDDLE. ')
sorting_criteria = sorting_criteria.lower()

hotel_price = final_dataset_travelie['Hotel price']
ticket_price = final_dataset_travelie['Ticket price']
hotelp_sorted = quicksort(hotel_price)
ticket_price_sorted = quicksort(ticket_price)


hotel_prices_for_hashing = []
hotels_for_hashing = []
hotel_names = final_dataset_travelie['Hotel ']

for i in hotel_names:
    hotels_for_hashing.append(i.split(',')[0])
for i in hotelp_sorted:
    hotel_prices_for_hashing.append(i)

ticket_prices_for_hashing = []
transport_means_for_hashing = []
company_name = final_dataset_travelie['Travel Companies']

for i in company_name:
    transport_means_for_hashing.append(i.split(',')[0])
for i in ticket_price_sorted:
    ticket_prices_for_hashing.append(i)

hotels = dict()

for i in range(len(hotels_for_hashing)):
    hotels[hotels_for_hashing[i]] = hotel_prices_for_hashing[i]

transport = dict()

for i in range(len(transport_means_for_hashing)):
    transport[transport_means_for_hashing[i]] = ticket_prices_for_hashing[i]

#We will lists with the hotels according to a high, low, mid criteria to better understand our data according to user 
#preferences. 

hotels_low = []
hotels_high = []
hotels_mid = []

transport_low = []
transport_mid = []
transport_high = []

for hotel in hotels.items():
    if hotel[1] >= 150 and hotel[1] <= 250:
        hotels_mid.append(hotel)
    elif hotel[1] < 150:
        hotels_low.append(hotel)
    else:
        hotels_high.append(hotel)

for item in transport.items():
    if item[1] < 80:
        transport_low.append(item)
    elif item[1] >= 80 and item[1] <= 150:
        transport_mid.append(item)
    else:
        transport_high.append(item)

#----------------------------------------------------------------

#We are ready to filter our data for later using it to return an optimised trip
final_mask_train = final_dataset_travelie['Means of transport'] == 'Train'
final_mask_plane = final_dataset_travelie['Means of transport'] == 'Plane'

if means_of_transport == 'plane':
    data = final_dataset_travelie[final_mask_plane]
else:
    data = final_dataset_travelie[final_mask_train]

#-------------------------------------------------------------------

sorting_mask = (data['Destination'] == destination) & (data['Departure'] == departure)
sorting_data = data[sorting_mask]

if sorting_criteria == 'yes':
    a = sorted(sorting_data['Ticket price'])
    b = quicksort(a)[0]
    sorting_mask = (data['Destination'] == destination) & (data['Departure'] == departure) & (data['Ticket price'] == b)
elif sorting_criteria == 'no':
    a = sorted(sorting_data['Ticket price'])
    b = quicksort(a)[-1]
    sorting_mask = (data['Destination'] == destination) & (data['Departure'] == departure) & (data['Ticket price'] == b)
elif sorting_criteria == 'middle':
    a = sorted(sorting_data['Ticket price'])
    b = quicksort(a)[(len(a)//2)]
    sorting_mask = (data['Destination'] == destination) & (data['Departure'] == departure) & (data['Ticket price'] == b)

final_set = data[sorting_mask]
#We use int so that only one integer will be displayed, as well as strings, which will be splitted and indexed to only show
#the desired info, instead of info on our variable too. 

final_company = str(final_set['Travel Companies']).split()[1]
final_ticket_price = int(final_set['Ticket price'])
final_hotel = str(final_set['Hotel ']).split()[1]
final_hotel_price = int(final_set['Hotel price'])
final_travel_time = int(final_set['Raw travel time'])
final_weeks_ahead = int(final_set['WeeksAhead'])

total_price_stay = stay_duration*final_hotel_price
total_trip_price = (total_price_stay + (final_ticket_price))

if total_trip_price <= budget:
       print(f"""Hello, {username}. The Travelie team hopes you're having an amazing day.
We received your preferences summary, and computed what we consider to be the best trip accoridng to your criteria.

You will depart from {departure} with destination {destination}, to where you will travel with {final_company}. The duration of your trip will be of {final_travel_time} minutes.
During your stay of {stay_duration} nights, you will be accommodated at {final_hotel} hotel.
The final price for your stay at {final_hotel} hotel will be of {total_price_stay}€, and the two-way ticket will cost {final_ticket_price}€.

FOR A GRAND TOTAL OF {total_trip_price} OUT OF YOUR {budget}€ BUDGET.

NOTE: To achieve the best price, we highly recommend that you contract your trip with {int(final_weeks_ahead)} weeks anticipation.

We hope you have a wonderful time visiting {destination} and bid you farewell.
For any inquiries about your trip, please contact us at 

+91 788 901 678
help.travelie@travelie.com
Paseo de la Castellana 297, Madrid
Spain""")

else: 
    print(f"""Hello, {username}.The Travelie team hopes you're having an amazing day.
We received your preferences summary, and are very sorry to inform you that we couldn't compute a trip to {destination} according to your preferences.

For any inquiries about your trip, please contact us at 

+91 788 901 678
help.travelie@travelie.com
Paseo de la Castellana 297, Madrid
Spain""")
 