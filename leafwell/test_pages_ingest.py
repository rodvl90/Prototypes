import os
from pprint import pprint
from time import sleep
from urllib.parse import urljoin

import requests
import tldextract
from bs4 import BeautifulSoup

visited = set()

base_url = 'https://leafwell.com/blog/'

def valid_url(url):
    # Implement this function to filter out URLs you don't want to visit
    if "facebook" in url:
        return False
    if "twitter" in url:
        return False
    if "instagram" in url:
        return False
    if "mailto" in url:
        return False

    # if an url has "blog" in it, then it is valid
    if "blog" in url:
        if not url.startswith('https'):
            url = urljoin(base_url, url)
        return url
    return False
    # return "http" in url

def save_content_text(url, content):
    extracted = tldextract.extract(url)
    filename = url.replace('/', '_').replace('https:', '').replace('http:', '') + '.txt'
    # filename = f"{extracted.domain}_{extracted.suffix}.txt"
    path = "data/" + filename
    print("save_content path: ", path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
def save_content_markdown(url, content):
    extracted = tldextract.extract(url)
    filename = url.replace('/', '_').replace('https:', '').replace('http:', '') + '.md'
    # filename = f"{extracted.domain}_{extracted.suffix}.txt"
    path = "data/" + filename
    print("save_content path: ", path)

def scrape(url):
    
    
    if url in visited:
        return
    visited.add(url)
    sleep(2)
    print("scrape Url: ", url,"\n\n")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Modify the CSS selector as per your requirements to extract the right content
    # If soup.select_one('.text-current') returns None, then the content is not found

    # Extract content from elements with the class 'my_class'
    elements = soup.select('.text-current:not(.text-sm)')
    content = url + "\n\n"
    if(len(elements) >= 1):
        print("Found elements: ", len(elements), "\n\n")
        content += '\n\n'.join(element.get_text(separator=' ', strip=True) for element in elements)
        save_content_text(url, content)
        save_content_markdown(url, content)


    links = soup.find_all('a', href=True)
    for link in links:
        new_url = valid_url(link['href'])
        if new_url:
            scrape(new_url)
        


start_url = 'https://leafwell.com/blog/'  # replace with your url
# Call the function with your URL
scrape(start_url)
