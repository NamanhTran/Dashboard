import requests, json, configparser

def get_current_weather(api_key, location):
    # Read from the config file for nytime api key
    # config = configparser.ConfigParser()
    # config.read('../configs/weatherstack.cfg')

    params = {
        'access_key': api_key,
        'query': location,
        'units': 'f'
    }

    try:
        response = requests.get('http://api.weatherstack.com/current', params)

        weather_info = response.json()

        return weather_info
    
    except:
        return None

# Need to pay $40 per month to use LOL
def get_seven_day_forecast(api_key, location):
    # Read from the config file for nytime api key
    # config = configparser.ConfigParser()
    # config.read('../configs/weatherstack.cfg')

    params = {
        'access_key': api_key,
        'query': location,
        'units': 'f',
        'forecast_days': 14
    }
    
    try:

        response = requests.get('http://api.weatherstack.com/forecast', params)

        weather_info = response.json()

        return weather_info
    
    except:
        return None