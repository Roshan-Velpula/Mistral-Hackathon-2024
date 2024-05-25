import requests
from bs4 import BeautifulSoup
import html2text
import os
import json

# Constants
BASE_URL = 'https://ernest.essec.edu'
URL_SCRAPE = "https://ernest.essec.edu/support/solutions/7000001043"

# Directory to save downloads
os.makedirs('downloads', exist_ok=True)

# Function to scrape articles and metadata from a parent URL
def scrape_articles_from_parent(parent_url, parent_title):
    articles = []
    page_number = 1

    while True:
        page_url = f"{parent_url}/page/{page_number}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        divs_1 = soup.find_all('div', class_="ellipsis article-title")
        if not divs_1:
            break
        
        for div in divs_1:
            a_tag = div.find('a')
            title = a_tag.get_text(strip=True)
            url_article = BASE_URL + a_tag['href']
            article_content = scrape_article(url_article)
            if article_content:
                markdown_content = html2text.html2text(article_content)
                article_data = {
                    "page_content": markdown_content,
                    "metadata": {
                        "Title": title,
                        "Parent": parent_title,
                        "URL": url_article
                    }
                }
                articles.append(article_data)
        
        page_number += 1
    
    return articles

# Function to scrape the content of an article
def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract article content
    article_body = soup.find('article', class_='article-body')
    if article_body:
        return str(article_body)
    return None

# Scrape the main URL to get parent sections
res_temp = requests.get(URL_SCRAPE)
soup_temp = BeautifulSoup(res_temp.content, 'html.parser')
divs = soup_temp.find_all('div', class_="list-lead")

# Dictionaries to store parent URLs and item counts
sections_url = {}
section_item_count = {}

for div in divs:
    a_tag = div.find('a')
    section_url = BASE_URL + a_tag['href']
    section_title = a_tag['title']
    span_tag = a_tag.find('span', class_='item-count')
    item_count = span_tag.get_text() if span_tag else '0'
    
    sections_url[section_title] = section_url
    section_item_count[section_title] = item_count

# Dictionary to store the final JSON data
final_data = {}

# Loop through each parent section and scrape articles
for parent_title, parent_url in sections_url.items():
    print(f"Scraping articles for parent section: {parent_title}")
    articles = scrape_articles_from_parent(parent_url, parent_title)
    if articles:
        final_data[parent_title] = articles

# Save the final data to a JSON file
json_filename = os.path.join('downloads', 'articles_data.json')
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print(f"Data saved to {json_filename}")
