import requests, json, configparser

def get_current_weather(location):
    # Read from the config file for nytime api key
    config = configparser.ConfigParser()
    config.read('../config.cfg')

    params = {
        'access_key': config['API Key']['weatherstack'],
        'query': location,
        'units': 'f'
    }

    response = requests.get('http://api.weatherstack.com/current', params)

    weather_info = response.json()

    print(weather_info)

    print(u'Current temperature in %s is %dF' % (weather_info['location']['name'], weather_info['current']['temperature']))

    return weather_info

def get_seven_day_forecast(location):
    # Read from the config file for nytime api key
    config = configparser.ConfigParser()
    config.read('../config.cfg')

    params = {
        'access_key': config['API Key']['weatherstack'],
        'query': location,
        'units': 'f',
        'forecast_days': 14
    }

    response = requests.get('http://api.weatherstack.com/forecast', params)

    weather_info = response.json()

    return weather_info

get_current_weather("Anaheim, United States of America")
get_seven_day_forecast("Anaheim, United States of America")