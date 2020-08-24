from newspaper import Article
import nltk
import re
import numpy as np
import pickle
from googlesearch import search
from urllib.parse import urlparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,ngram_range=(1,3))
model = pickle.load(open('models/model.pkl', 'rb'))

with open('models/data_pick.pkl','rb') as pickle_data:
    corpus = pickle.load(pickle_data)




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


def similarity(url_list, article):
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
    averageScore = round(averageScore, 2)
    return averageScore


def predict(input):
     # preprocessing
    ps = PorterStemmer()
    test_text = []
    input_txt = input
    test = re.sub('[^a-zA-Z]',' ',input_txt[0])
    test = test.lower()
    test = test.split()
    test = [ps.stem(word) for word in test if not word in stopwords.words('english')]
    test = ' '.join(test)
    test_text.append(test)

    #countvectorization

    corpus.append(test_text[0])

   # from sklearn.feature_extraction.text import CountVectorizer
    #cv = CountVectorizer(max_features=5000,ngram_range=(1,3))
    X = cv.fit_transform(corpus).toarray()

    prediction = model.predict(np.array([X[-1]]))

    return prediction


if __name__ == "__main__":
    url = 'https://www.indiatoday.in/india/story/indian-national-among-killed-landslides-nepal-1707450-2020-08-03'
    test_text, test_title, test_link, test_article = scrape(url)
    print(test_article)
    #print(test_text, test_link,test_title, test_article)
    search_urls, source_sites = google_search(test_link, test_title)
    #print(search_urls)
    #print(source_sites)
    #sim_score = simalirity(search_urls, test_text)
    #sim_score, avg_score = similarity(search_urls, test_text)
    #print(avg_score)
     


        
    




