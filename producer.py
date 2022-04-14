from time import sleep
from json import dumps
from kafka import KafkaProducer
from tweepy import OAuthHandler, Stream
import tweepy
import json

#connexion to kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

#connexion to tweeter API
class StdOutListener(tweepy.Stream):
    def on_status(self, status):
        data = {'id_tweet' : status.id, 'created_at' : str(status.created_at).split(" ")[1], 'text':status.text, 'location_user':status.user.location, 'flag_geo':status.user._json['geo_enabled'], 'number of likes': status.favorite_count,
'number of retweets':status.retweet_count, 'user_numner_followers':status.user.followers_count}
      

        print(data)
        #sending tweet by kafka producer 
        producer.send('numtest', value=data)
        return True

#reading tweeter api credentials
with open('myKeys.json') as json_file:
    data = json.load(json_file)

API_key = data['API_key']  
API_secret_key = data['API_secret_key']  
Access_token = data['Access_token']
Access_token_secret = data['Access_token_secret']



#listening tweeter in streaming
listener = StdOutListener(API_key, API_secret_key, Access_token, Access_token_secret)
listener.filter(languages=['en'], track=['film',  'movie'])
listener.sample()


 
