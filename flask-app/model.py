import pandas as pd

df=pd.read_csv('datasets/train.csv')

#df.head()

#get the independent features
x=df.drop('label',axis=1)

#x.head()

#get the dependent features
y=df['label']

#y.head()

df.shape

from sklearn.feature_extraction.text import CountVectorizer

df=df.dropna()

messages=df.copy()

messages.reset_index(inplace=True)

import nltk
#nltk.download('stopwords')

from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer
import re 
ps = PorterStemmer()
corpus = []

    
import pickle

with open('data_pick.pkl', 'rb') as pickle_data:
    corpus = pickle.load(pickle_data)
    

## Applying Countvectorizer
# creating the bag of words model 
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 5000, ngram_range=(1,3))
X = cv.fit_transform(corpus).toarray()    

y=messages['label']

# Divide the dataset into train and test 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.33, random_state=0)

count_df = pd.DataFrame(X_train, columns=cv.get_feature_names())

#cv.get_feature_names()

#count_df.head()

# passive agressive classifier algorithm 

from sklearn.linear_model import PassiveAggressiveClassifier
import itertools
linear_clf = PassiveAggressiveClassifier(n_iter_no_change=50)
linear_clf.fit(X_train, y_train)
pred = linear_clf.predict(X_test)
#score = metrics.accuracy_score(y_test, pred)
#print("accuracy: %0.3f" % score)    

#saving model
pickle.dump(linear_clf, open('model.pkl', 'wb'))

#loading model
model = pickle.load(open('model.pkl','rb'))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    





























