import json
import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title_element = soup.find("h1", class_="article-title")
        if title_element:
            article_title = title_element.text.strip()
        else:
            article_title = "Title not found"

        content_elements = soup.find_all("p", class_="article-content")
        article_content = "\n".join([element.text.strip() for element in content_elements])
        return article_title, article_content
    else:
        return "Failed to retrieve the web page", ""

def process_profiles(profiles):
    profile_output = []
    for profile in profiles:
        name = profile.get("name", "Unknown Name")
        age = profile.get("age", "Unknown Age")
        occupation = profile.get("occupation", "Unknown Occupation")

        profile_output.append(f"Name: {name}\nAge: {age}\nOccupation: {occupation}\n{'-' * 25}")
    return profile_output

def main():

    with open("article_urls.json", "r") as urls_file:
        article_urls = json.load(urls_file)

    
    with open("profiles.json", "r") as profiles_file:
        profiles_data = json.load(profiles_file)

    
    for url in article_urls:
        article_title, article_content = scrape_article(url)
        print("Scraped Article Information:")
        print("Article URL:", url)
        print("Article Title:", article_title)
        print("Article Content:", article_content)
        print("-" * 50)

    
    profile_output = process_profiles(profiles_data)
    print("Processed Profiles:")
    print("\n".join(profile_output))

if __name__ == "__main__":
    main()
