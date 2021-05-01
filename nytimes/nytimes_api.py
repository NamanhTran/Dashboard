import requests, json, configparser

def get_nytimes_articles(api_key, max_articles):
    # Read from the config file for nytime api key
    # config = configparser.ConfigParser()
    # config.read('../configs/config.cfg')
    
    # Get the articles from the front page
    try:
        response = requests.get(f"https://api.nytimes.com/svc/topstories/v2/home.json?api-key={api_key}")

        # Only get the first n articles
        articles_json = response.json()['results'][:max_articles]
        return articles_json

    except:
        return None