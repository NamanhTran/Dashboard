import threading, concurrent.futures, configparser, datetime
from pymongo import MongoClient

from hackernews.hackernews_api import get_hackernews_stories
from hackernoon.hackernoon_scraper import get_hackernoon_articles
from nytimes.nytimes_api import get_nytimes_articles
from weather.weatherstack_api import get_current_weather

def hackernews_thread():
    print("hackernews")

def hackernoon_thread():
    print("hackernoon")

def nytimes_thread():
    print("nytimes")

def weather_thread():
    print("weather")

def main():
    # Get the config file for the infoscraper
    config = configparser.ConfigParser()
    config.read('./configs/config.cfg')

    # Initalize the results variables
    hackernews_result = None
    hackernoon_result = None
    nytimes_result = None
    weather_result = None

    # Create a thread for each of the api calls 
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        # Create threads to gather information
        hackernews_thread = executor.submit(get_hackernews_stories, 25)
        nytimes_thread = executor.submit(get_nytimes_articles, config['API Key']['nytimes'], 25)
        weather_thread = executor.submit(get_current_weather, config['API Key']['weatherstack'], 'Anaheim, California')
        hackernoon_thread = executor.submit(get_hackernoon_articles, 'hackernoon-top-story', 25)
        
        # Get all the results from the threads results
        hackernoon_result = hackernoon_thread.result()
        hackernews_result = hackernews_thread.result()
        nytimes_result = nytimes_thread.result()
        weather_result = weather_thread.result()

    # Get the database client and conenction
    client = MongoClient('<INSERT URI>') # configparser doesn't work here for some reason so temp fix is to hard code the URI
    db = client['dashboard']

    # Insert collected data into the MongoDB 
    data = {"hackernoon": hackernoon_result,
            "hackernews": hackernews_result,
            "nytimes": nytimes_result,
            "weather": weather_result,
            "lastModifiedDate": datetime.datetime.utcnow()}

    db.data.insert_one(data)

if __name__ == "__main__":
    main()