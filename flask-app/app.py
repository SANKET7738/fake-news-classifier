# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 20:13:44 2020

@author: sanket
"""

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# importing lib
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,ngram_range=(1,3))

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

with open('data_pick.pkl','rb') as pickle_data:
    corpus = pickle.load(pickle_data)
def input(final_features):
     

    # preprocessing

    ps = PorterStemmer()
    test_text = []
    input_txt = [final_features]
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


@app.route('/')
def home():
    return render_template('landingpage.html')

@app.route('/predict',methods=['POST'])
def predict():
    
    #for rendering results 
    int_features = [x for x in request.form.values()]
    print('int_features',int_features)
    # final_features = [np.array(int_features)]
    # print('finaal = ', final_features)
    # prediction = input(final_features)
    prediction = input(int_features[0])

    if(prediction==1):
        output = "Unreliable"
    else:
         output = "Reliable"

    return render_template('info.html', pred_output=output)


if __name__ == "__main__":
    app.run(debug=True)