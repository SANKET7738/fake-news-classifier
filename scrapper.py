from newspaper import Article
import nltk
import re
from googlesearch import search
from urllib.parse import urlparse

def scrape(user_input):
    url = user_input
    article = Article(url)
    article.download()
    article.parse()
    nltk.download('punkt')
    article.nlp()
    text = article.text
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub("(\\r|\r|\n)\\n$", " ", text)
    text = [text]
    
    input_text = text
    input_link = user_input
    input_title = article.title

    return input_text, input_title, input_link

def search(input_link, input_title):
    title = input_title
    domain = urlparse(input_link).hostname
    search_urls = []
    source_sites = []
    for i in search(title, tld = "com", num = 10, start = 1, stop = 6):
        if "youtube" not in i and domain not in i:
            source_sites.append(urlparse(i).hostname)
            search_urls.append(i)

    return search_urls, source_sites



