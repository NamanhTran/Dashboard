import os, json
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import NoSuchElementException

def get_hackernoon_articles(tag, max_results):
    url = f"https://hackernoon.com/tagged/{tag}"

    # Launch Firefox in headless
    opts = FirefoxOptions()
    opts.add_argument("--headless")

    driver = webdriver.Firefox(options=opts)
    driver.implicitly_wait(2)

    # Get the url
    driver.get(url)

    # List to hold all articles infomation
    articles_info = []

    while len(articles_info) != max_results:
        try:
            # Get the articles and images for the articles
            articles = driver.find_elements_by_xpath("//article/div[@class='title-wrapper']/h2/a")
            images = driver.find_elements_by_xpath("//article/div[@class='image-wrapper']/a/div/img")\
            
            # To remove the first article which is always an ad
            #images = images[1:]
        
        except NoSuchElementException:
            print("The hackernoon page has changed. This scraper needs to be updated! 1")
            return None

        try:
            # Ensure that there are equal numbers of articles and images
            assert len(articles) == len(images)

            # Loop through all the articles
            for i in range(len(articles)):
                # If we have enough articles we can stop scraping for more articles
                if len(articles_info) == max_results:
                    break

                # Get and set the article's title, url, and image
                article_title = articles[i].text
                article_url = articles[i].get_attribute("href")
                image_url = images[i].get_attribute("src")

                article_info = {"title": article_title, "url": article_url, "image_url": image_url}
                articles_info.append(article_info)
        
        except:
            print("The hackernoon page has changed. This scraper needs to be updated! 2")
            return None

        # Click next page
        try:
            driver.find_element_by_xpath("//a[@aria-label='Next page']").click()

        except NoSuchElementException:
            print("The hackernoon page has changed. This scraper needs to be updated! 3")
            return None

    # Replaces broken images and 
    for article in articles_info:
        # Get the length of the title
        article_title_length = len(article["title"])

        # Get the length of the image url
        image_url_length = len(article["image_url"])

        # Get the last three character of the title
        last_three_char_title = article["title"][article_title_length - 3: article_title_length]

        # Get the last three character of the image url
        last_three_char_image_url = article["image_url"][image_url_length - 4: image_url_length]

        # If the last three character is '...' then the title is truncated
        if last_three_char_title == "...":
            try:
                # Go to the webpage
                driver.get(article["url"])

                # Scrap the full title
                full_title = driver.find_element_by_xpath("//main/div/h1").text

                # Replace article.title with correct title
                article["title"] = full_title
            
            except NoSuchElementException:
                print(f"Cannot get full title for {article['title']}")
                return None
        
        # If the last three character is 'gif' then it is a broken image
        if last_three_char_image_url != "jpeg":
            try:
                # Go to the webpage
                driver.get(article["url"])

            except NoSuchElementException:
                print("The hackernoon page has changed. This scraper needs to be updated! 4")
                return None

            # Get the image
            try:
                new_image_url = driver.find_element_by_xpath("//div[@class='fullscreen']/img").get_attribute("src")

                # Set the new image url
                article["image_url"] = new_image_url

            except NoSuchElementException:
                print(f"No image found for {article['title']}")

    driver.close()

    return articles_info