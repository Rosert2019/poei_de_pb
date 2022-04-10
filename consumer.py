from kafka import KafkaConsumer
from json import loads
import json
import pandas as pd
import streamlit as st
import requests
import industrialisation #l'importation du classifier contenu dans le fichier pickle

st.title("Lecture des tweets en streaming et analyse sentimentale") 


consumer = KafkaConsumer(
    'numtest',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

end_point_pb = 'https://api.powerbi.com/beta/5dd8a2bb-ec68-4001-8b40-8d12dc51acd8/datasets/f41ee568-712a-4d18-9832-ccaab2f242d0/rows?key=khPrXZk1PeQ%2BQ46eSpru69y4fEwZd3P%2FQlxfJ5L6LuF0sdzzCu3UzsuEqtPKJUbCAlxqxGbjERQjscfCWXv%2BLQ%3D%3D'

flag_pos = 0
flag_neg = 0

for tweet in consumer:
    tweet = tweet.value

    #extract tweet features
    tweetFeature = industrialisation.findFeatures(tweet['text'])

    #review prediction
    review = industrialisation.loadBayes.classify(tweetFeature)
    
    if review == 'pos':
        st.success('Positif review')
        flag_pos = 1
    else:
        st.warning('Negatif review')
        flag_neg  = 1 
     
    tweet['review'] = review 
    tweet['flag_pos'] = flag_pos
    tweet['flag_neg'] = flag_neg

    #get minute and hours
    tweet['minutes'] = tweet['created_at'].split(':')[1]
    tweet['hours'] = tweet['created_at'].split(':')[0]

    #get country from location if exist
    if tweet['location_user'] is not None:
       tweet['location_user'] = (tweet['location_user']).split(',')[-1]
    else:
        tweet['location_user'] = tweet['location_user']

    #envoie dans power bi service 
    res = requests.post(end_point_pb, data=json.dumps([tweet])) 
    tweet['status_bi'] = res.status_code

    #print dans streamlit
    tweetDataFrame = pd.DataFrame([tweet])
    st.table(tweetDataFrame)

    flag_pos = 0
    flag_neg = 0
