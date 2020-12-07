# -*- coding: utf-8 -*-
"""sentiment_detection_from_book_reviews.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i0uzdBKh4reV_JY361ZyXlxWIzEDi8M0
"""

import random
class Sentiment:
  negative= "NEGATIVE"
  positive= "POSITIVE"
  neutral= "NEUTRAL"
class Review:
  def __init__(self,text,rate):
    self.text=text;
    self.rate=rate;
    self.sentiment= self.get_sentiment()
  def get_sentiment(self):
    if self.rate <=2:
      return Sentiment.negative
    elif self.rate == 3:
      return Sentiment.neutral
    else:
      return Sentiment.positive 

class Reviewsfilter:
  def __init__(self,reviews):
    self.reviews= reviews
  def get_text(self):
    return [x.text for x in self.reviews]
  def get_sentiment(self):
    return [x.text for x in self.reviews]
  def evenly_distribute(self):
    negative = list(filter(lambda x: x.sentiment== Sentiment.negative,self.reviews))
    positive = list(filter(lambda x: x.sentiment== Sentiment.positive,self.reviews))
 #shrinking positive examples
    positive_shrunk= positive[:len(negative)] # from 0 to as many elemnts that negative has
    self.reviews= positive_shrunk + negative
    
    random.shuffle(self.reviews)

import json
reviews=[]
with open('Books_small_10000.json') as f:
  for line in f:
    r= json.loads(line)
    reviews.append(Review(r['reviewText'],r['overall']))
reviews[2].sentiment

from sklearn.model_selection import train_test_split
#two types of splits, one with passing X and y separately
train, test = train_test_split(reviews,test_size=0.33,random_state=42)
train_container=Reviewsfilter(train)
test_container=Reviewsfilter(test)


#len(test_container.reviews)

train_container.evenly_distribute()
X_train= train_container.get_text()
Y_train= train_container.get_sentiment()
X_test= test_container.get_text()
Y_test= test_container.get_sentiment()

#len(train)
#print(train[77].text)
#splitting data
#X_train= [temp.text for temp in train]
#Y_train= [temp.sentiment for temp in train]
#X_test=  [temp.text for temp in test]
#Y_test=  [temp.sentiment for temp in test]
#X_train[0]
#Y_train[0]

from sklearn.feature_extraction.text import CountVectorizer
vectorizer= CountVectorizer()
BOW_X_train=vectorizer.fit_transform(X_train) #bag of words for X training. Creates an array of words
#print(BOW_X_train.vocabulary_) #fit just creates a vocabulary
#use transform to to encode/tokenize a document(has to be a raw document_)
BOW_X_test= vectorizer.transform(X_test)


#BOW_X_test= vectorizer.fit_transform(X_test)
#print(BOW_X_train[0].toarray())
#print(X[0])

"""Predicting using different models"""

#SVM CLASSIFIER

from sklearn.svm import SVC
svm_model= SVC(kernel='linear') #classifier
svm_model.fit(BOW_X_train, Y_train)
print(X_test[1])
print(Y_test[1])
svm_model.predict(BOW_X_test[1])

#DECISION TREE

from sklearn.tree import DecisionTreeClassifier

tree_model= DecisionTreeClassifier()
tree_model.fit(BOW_X_train, Y_train)
print(X_test[15])
tree_model.predict(BOW_X_test)

#NAIVE BAYES

from sklearn.naive_bayes import GaussianNB

nb_model= GaussianNB()
nb_model.fit(BOW_X_train.toarray(),Y_train)
print(X_test[15])
nb_model.predict(BOW_X_test.toarray())

#LOGISTIC REGRESSION

from sklearn.linear_model import LogisticRegression
lr_model= LogisticRegression()
lr_model.fit(BOW_X_train.toarray(),Y_train)
print(X_test[15])
lr_model.predict(BOW_X_test.toarray())

"""Evaluating!"""

# passing data to use for testing and Y_test for comparing
 #JUST THE ACCURACY
# print(type(BOW_X_train))
 #BOW_X_test.shape
 print(svm_model.score(BOW_X_test, Y_test))
 print(tree_model.score(BOW_X_test, Y_test))
 print(nb_model.score(BOW_X_test.toarray(), Y_test))
 #print(lr_model.score(BOW_X_test, Y_test))

#F1 SCORES; scores from 0-1, 1 being best
from sklearn.metrics import f1_score
print(f1_score(Y_test,svm_model.predict(BOW_X_test), average= None, labels=[Sentiment.positive,Sentiment.neutral,Sentiment.negative] ))
print(f1_score(Y_test,tree_model.predict(BOW_X_test), average= None, labels=[Sentiment.positive,Sentiment.neutral,Sentiment.negative] ))
# works good on positive but not negative and neutral data



