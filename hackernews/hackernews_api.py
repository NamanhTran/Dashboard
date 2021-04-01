import requests, json

def get_hackernews_stories(max_stories):

    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")

    stories_id = response.json()[:max_stories]

    stories_info = []

    for story_id in stories_id:
        response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
        story_info = response.json()
        stories_info.append(story_info)

    return stories_info

print(get_hackernews_stories(20))