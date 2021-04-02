import requests, json, configparser

def get_nytimes_articles(max_articles):
    # Read from the config file for nytime api key
    config = configparser.ConfigParser()
    config.read('../config.cfg')
    
    # Get the articles from the front page
    response = requests.get(f"https://api.nytimes.com/svc/topstories/v2/home.json?api-key={config['API Key']['nytimes']}")

    # Only get the first n articles
    articles_json = response.json()['results'][:max_articles]
    print(json.dumps(articles_json, indent=4))
    return articles_json