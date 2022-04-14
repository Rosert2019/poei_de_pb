# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 08:36:21 2022

@author: Djonga
"""

import os
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes  import MultinomialNB, BernoulliNB
import pickle

os.chdir('D:/POEI-Data ENGINEER/Autres')

nltk.download('averaged_perceptron_tagger')

#reading positive and negative tweetq from files on disk
positiveTweets = open('./data/positive.txt','r').read()
negativeTweets = open('./data/negative.txt','r').read()

allWords = []
documents = []
allowedWordTypes = ['JJ']
wordFeatures = []


for tweet in positiveTweets.split('\n'):
   documents.append((tweet, 'pos'))
   words = word_tokenize(tweet)
   couples = nltk.pos_tag(words)
   for w in couples:
      if w[1] in allowedWordTypes:
          allWords.append(w[0].lower())
		  
		  
for tweet in negativeTweets.split('\n'):
   documents.append((tweet, 'neg'))
   words = word_tokenize(tweet)
   couples = nltk.pos_tag(words)
   for w in couples:
      if w[1] in allowedWordTypes:
          allWords.append(w[0].lower())	

allWords = nltk.FreqDist(allWords)
wordFeatures = list(allWords.keys())[:5000]		

#allWords.plot(cumulative=True) 

def findFeatures(document):
    words = word_tokenize(document)
    features = {}
    for w in wordFeatures:
       features[w] = (w in words)
    return features
	
featureSets = [(findFeatures(tweet), category) for (tweet, category) in documents]

random.shuffle(featureSets)
testingSet = featureSets[10000:]
trainingSet = featureSets[:10000]

classifier = nltk.NaiveBayesClassifier.train(trainingSet)

#We can check the model prediction accuracy with test_x data.
#https://www.datatechnotes.com/2019/05/sentiment-classification-with-nltk.html
#https://github.com/carlosarcila/autocop_en_distributed

acc=nltk.classify.accuracy(classifier, testingSet)
print("Accuracy:", acc)

#export modele to pickle
pickle.dump(classifier, open('bayesTweets.pkl', 'wb'))

		  

		