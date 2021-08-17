import requests
from prettytable import PrettyTable


# API for requests
api_url = 'http://api.openweathermap.org/data/2.5/weather'
api_url_for_cities = 'http://api.openweathermap.org/data/2.5/find'

# Enter the city and number of cities around
print('Enter the city:')
while True:
    city = input()
    if not city:
        print('Enter the city:')
    else:
        break

print('Enter the number of cities(up to 50):')
while True:
    amount_city = input()
    if amount_city.isdigit():
        break
    else:
        print('Enter the number of cities(up to 50):')

# Create dict with params for request to determine the coordinates of the city
params_for_coord = {
    'q': city,
    'appid': '404d2a101510d5c590a0358a0b3d47c9',
    'units': 'metric'

}

# Params for request to determine the coordinates of the city
res_for_coord = requests.get(api_url, params=params_for_coord)
city_data = res_for_coord.json()

# Create dict with params for main request
params_for_cities = {
    'appid': '404d2a101510d5c590a0358a0b3d47c9',
    'units': 'metric',
    'cnt': amount_city,
}

# Add coordinates to the dict with params for main request
params_for_cities.update(city_data['coord'])

# Main request
res_for_cities = requests.get(api_url_for_cities, params=params_for_cities)
city_circle_data = res_for_cities.json()

# Create list for information about weather
weather_list = [[el['name'], str(el['main']['temp']), str(el['main']['feels_like']), str(el['main']['pressure']),
                 str(el['main']['humidity']), str(el['wind']['speed'])] for el in city_circle_data['list']]


# Create pretty output
x = PrettyTable()
x.field_names = ['City', 'Temperature', 'Feels like', 'Pressure', 'Humidity', 'Wind speed', ]
[x.add_row(el) for el in weather_list]
print(x)











