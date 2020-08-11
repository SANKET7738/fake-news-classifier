from django.shortcuts import render
from .forms import InputForm

from newspaper import Article
import nltk
import re
from googlesearch import search
from urllib.parse import urlparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,ngram_range=(1,3))
model = pickle.load(open('models/model.pkl', 'rb'))

with open('models/data_pick.pkl','rb') as pickle_data:
    corpus = pickle.load(pickle_data)

from classifier.scrapper import scrape, simalirity, google_search
from classifier.models import NewsInfo


# Create your views here.
def index(request):
    output = ''
    
    if request.GET.get('news_link', None) is not None:
        try:
            url = request.GET['news_link']
            NewsInfo.objects.create(news_link=url)
            pred_output = classify(url)
            if(pred_output==1):
                output = "Unreliable"
            else:
                output = "Reliable"
            print(output)
            NewsInfo.objects.create(output=output)
            NewsInfo.save()
        except Exception as e:
            print(e)
   
    return render(request, 'classifier/landingpage.html')

def output(request):
    return render(request,'classifier/info.html', {'pred_output':output})

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

def classify(url):
     test_text, test_title, test_link, test_article = scrape(url)
     search_urls, source_sites = google_search(test_link, test_title)
     #sim_score = simalirity(search_urls, test_text)
     pred_result = predict(test_text)
     print(pred_result)
     return pred_result


