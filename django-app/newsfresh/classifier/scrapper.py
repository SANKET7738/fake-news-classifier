from newspaper import Article
import nltk
import re
import numpy as np
from googlesearch import search
from urllib.parse import urlparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from classifier.models import NewsInfo



def scrape(user_input):
    url = user_input
    article = Article(url)
    article.download()
    article.parse()
    #nltk.download('punkt')
    article.nlp()
    text = article.text
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub("(\\r|\r|\n)\\n$", " ", text)
    text = [text]
    
    input_text = text
    input_link = user_input
    input_title = article.title

    return input_text, input_title, input_link, article

def google_search(input_link, input_title):
    title = input_title
    domain = urlparse(input_link).hostname
    search_urls = []
    source_sites = []
    for i in search(title, tld = "com", num = 10, start = 1, stop = 6):
        if "youtube" not in i and domain not in i:
            source_sites.append(urlparse(i).hostname)
            search_urls.append(i)

    return search_urls, source_sites

def simalirity(search_urls, input_text):
    #cv = CountVectorizer(max_features = 5000, ngram_range=(1,3))
    count = 0
    input_text = input_text
    # print('INPUT_TEXT = ', input_text)
    sim_tfv = TfidfVectorizer(stop_words ="english")
    #obj1 =  cv.fit_transform(input_text)
    obj1 = sim_tfv.fit_transform(input_text)
    
    
    for i in search_urls:
        print('count = ', count)
        test_text, test_title, test_link, test_article = scrape(i)
        # print('TEST_TEXT = ', test_text)
        # print('length ', len(test_text[0]))
        test_text = [test_text]
        #obj2 = cv.fit_transform(test_text)
        sim_tfv2 = TfidfVectorizer(stop_words ="english")
        
        obj2 = sim_tfv2.fit_transform(test_text[0])
        score = cosine_similarity(obj1,obj2)
        score.append(score*100)
        count += 1
    avg_score = score/count


    return avg_score

def mentor_similarity(url_list, article):
    article = article
    sim_tfv = TfidfVectorizer(stop_words ="english")
    #article needs to be vectorized first
    sim_transform1 = sim_tfv.fit_transform(article)
    cosine = []
    cosineCleaned = []
    cosineAverage = 0
    count = 0
    print('sim_transform1 = ',sim_transform1)
    #loop to calculate each article from the google search
    #against the original article
    for i in url_list:
        test_text, test_title, test_link, test_article = scrape(i)
        
        test_text = [test_text]
        sim_transform2 = sim_tfv.transform(test_text[0])
        print('sim_transform2 = ', sim_transform2)
        score = cosine_similarity(sim_transform1, sim_transform2)
        cosine.append(score*100)
        print("Article " + str(count) + " similarity calculated")
        count+=1
    for i in cosine:
        x = str(i).replace('[','').replace(']','')
        cosineCleaned.append(x)

    for i in cosine:
        if i !=0:
            cosineAverage = cosineAverage + i
        else:
            count-=1

    #averages the similarity score
    averageScore = cosineAverage/count
    averageScore = str(averageScore).replace('[','').replace(']','')
    averageScore = float(averageScore)
    print(averageScore)
    return cosineCleaned, averageScore


if __name__ == "__main__":
    url = 'https://www.indiatoday.in/india/story/indian-national-among-killed-landslides-nepal-1707450-2020-08-03'
    test_text, test_title, test_link, test_article = scrape(url)
    #print(test_text, test_link,test_title, test_article)
    search_urls, source_sites = google_search(test_link, test_title)
    #print(search_urls)
    #print(source_sites)
    sim_score = simalirity(search_urls, test_text)
    # sim_score = mentor_similarity(search_urls, test_text)
    print(sim_score)
     


        
    




