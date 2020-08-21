from django.shortcuts import render
from .forms import InputForm

from newspaper import Article
import nltk
import re
import requests
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
from classifier.forms import InputForm


# Create your views here.
def index(request):
    print(request.POST)
    
   
    return render(request, 'classifier/landingpage.html')

def form(request):
    form = InputForm()


    return render(request, 'classifier/form.html', {'form':form})

def output(request):
    print("1")
    form = InputForm(request.POST)
    if form.is_valid():
        print("2")
        url = form.cleaned_data['input_url']
        print(url)
        return render(request, 'classifier/output.html', {'url':url})
    else:
        print("error")
        error = "Oops"

    return render(request, 'classifier/output.html',{'url':error})
    



    


def classify(url):
    print("step-3")
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



