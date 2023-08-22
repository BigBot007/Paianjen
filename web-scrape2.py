import json
import requests
from bs4 import BeautifulSoup
import csv

def scrape_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title_element = soup.find("h1", class_="article-title")
        author_element = soup.find("p", class_="author")
        content_elements = soup.find_all("p", class_="article-content")

        if title_element:
            article_title = title_element.text.strip()
        else:
            article_title = "Title not found"

        if author_element:
            article_author = author_element.text.strip()
        else:
            article_author = "Author not found"

        article_content = "\n".join([element.text.strip() for element in content_elements])
        
        return article_title, article_author, article_content
    else:
        return "Failed to retrieve the web page", "", ""

def process_profiles(profiles):
    profile_output = []
    for profile in profiles:
        title_path = profile.get("title", "Unknown title")
        teaser_path = profile.get("teaser", "Unknown teaser")
        content_path = profile.get("content", "Unknown content")

        profile_output.append(f"title: {title_path}\nteaser: {teaser_path}\nOccupation: {content_path}\n{'-' * 25}")
    return profile_output

def main():
    
    with open("links1.json", "r") as urls_file:
        article_urls = json.load(urls_file)

    
    with open("profiles.json", "r") as profiles_file:
        profiles_data = json.load(profiles_file)

    article_urls = article_urls ['links']
    profiles_info = process_profiles(profiles_data)

    
    for url in article_urls:
        article_title, article_author, article_content = scrape_article(url)
    article_urls.append({"URL": url, "Title": article_title, "Author": article_author, "Content": article_content})

    
    with open("output.csv", "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["URL", "Title", "Author", "Content"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(article_urls)

        
        csv_file.write("\n")
        csv_file.write("Profiles:\n")
        csv_file.write("\n".join(profiles_info))

if __name__ == "__main__":
    main()


