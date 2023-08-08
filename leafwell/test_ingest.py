import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def replace_links_with_content(soup, base_url):
    # find all link elements
    for a in soup.find_all('a', href=True):
        url = a['href']

        # handle internal relative URLs
        if not url.startswith('http'):
            url = urljoin(base_url, url)

        # fetch content of the linked page
        linked_soup = fetch_content(url)

        # find the element with class "text-current" and get its text content
        text_current = linked_soup.find(class_='text-current')
        if text_current is not None:
            text_current = text_current.get_text(separator=' ', strip=True)

        # replace link with the content of the "text-current" element
        a.replace_with(text_current if text_current else '')

    return soup

def compile_website(url):
    soup = fetch_content(url)
    soup = replace_links_with_content(soup, url)

    # extract and clean text
    text = ' '.join(re.sub(r'\{.*?\}', '', tag.get_text()) for tag in soup.find_all(True))

    # replace '/' with '_' in filename to avoid errors
    filename = url.replace('/', '_') + '.txt'
    path = 'data/' + filename
    # save the cleaned text to a file
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

# define the initial URL
start_url = 'https://leafwell.com/blog'  # replace with your url

# start the compilation
compile_website(start_url)
