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
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,ngram_range=(1,3))
model = pickle.load(open('models/model.pkl', 'rb'))

with open('models/data_pick.pkl','rb') as pickle_data:
    corpus = pickle.load(pickle_data)

from classifier.scrapper import scrape, simalirity, google_search, predict
from classifier.models import NewsInfo


# Create your views here.
def index(request):
    if request.GET.get('news_link', None) is not None:
        try:
            url = request.GET['news_link']
            NewsInfo.objects.create(news_link=url)
            output = classify(url)
        except Exception as e:
            print(e)
   
    return render(request, 'classifier/landingpage.html')

def output(request, output):
    try:
        output = NewsInfo.objects.get(pk=output)
    except NewsInfo.DoesNotExist:
        raise Http404("Question does not exist")

    #output = classify(news_link)

    return render(request,'classifier/info.html', {'pred_output':output})


def classify(url):
    news_model = NewsInfo.objects.create()
    test_text, test_title, test_link, test_article = scrape(url)
    news_model.news_title = test_title
    news_model.news_link = test_link
    news_model.news_text = test_text
    search_urls, source_sites = google_search(test_link, test_title)
    #sim_score = simalirity(search_urls, test_text)
    pred_output = predict(test_text)
    if(pred_output==1):
        output = "Unreliable"
    else:
        output = "Reliable"
    print(output)
    news_model.output = output
    news_model.save()

    return output



