#!/usr/bin/env python

import pickle
import json
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

#lecture du fichier contenant le classifier bayesien
loadBayes = pickle.load(open('bayesTweets.pkl', 'rb'))

#import all words features
with open('wordFeatures.json') as json_file:
    allWords = json.load(json_file)
	
wordFeatures = allWords['wordFeatures']


#extract tweet features
def findFeatures(document):
    words = word_tokenize(document)
    features = {}
    for w in wordFeatures:
       features[w] = (w in words)
    return features
	

#tweetText = "Oh my goodness Jersey Boys is the best thing I have seen @BradfordTheatre in a long time. @LukeSuri was amazing as Frankie Valli, what a voice! But my fave was @TheGriffmiester as Nick Massi. Five star review from me. Don't forget the accessible performances 16th and 17th."	
#tweetFeatures= findFeatures(tweetText)	
#example of pred
#prediction = loadBayes.classify(tweetFeatures)
#print(prediction)
