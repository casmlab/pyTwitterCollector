import tweepy
import threading
import logging
from tweepy.models import Status
from tweepy.utils import import_simplejson, urlencode_noplus
import json
import re

json = import_simplejson()

class Stream:
    
    def __init__(self, consumer_key, consumer_secret, 
                       key, secret, filter, name):
        
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(key, secret)
        self.filter = filter
        self.tweetsBuffer = TweetsBuffer()
        self.name = name
        self.logger = logging.getLogger('TwitterCollector')
        #check credentials
        if not tweepy.API(self.auth).verify_credentials():
            print "Invalid credentials for user: ",self.name,".\nExiting..."
            logging.error("Invalid credentials for user: "+self.name+".\nExiting...")
            exit(0)

    def run(self):
        
        sl = StreamListener()
        sl.init(self.tweetsBuffer)
        try:
            streamer = tweepy.Stream(auth=self.auth, 
                                     listener=sl, 
                                     timeout=3000000000, 
                                     include_entities=1, 
                                     include_rts=1)
            
            #load friends, if there is no ids file
            if not self.filter:
                self.filter = tweepy.API(self.auth).friends_ids()
            sThread = threading.Thread(target=streamer.filter, args=(self.filter,))
            #sThread = threading.Thread(target=streamer.filter, args=(None, ['hello']))
            sThread.start()
            return sThread
        except Exception, e:
            print e
    
    def getTweetsBuffer(self):
        return self.tweetsBuffer

class StreamListener(tweepy.StreamListener):
    
    def init(self, tweetsBuffer):
        #set buffer
        self.tweetsBuffer = tweetsBuffer
            
    def parse_status(self, status, retweet = False):
        
        tweet = {
                 'tweet_id':status.id, 
                     'tweet_text':status.text,
                     'created_at':status.created_at,
                     'geo_lat':status.coordinates['coordinates'][0] 
                               if not status.coordinates is None 
                               else 0,
                     'geo_long': status.coordinates['coordinates'][1] 
                                 if not status.coordinates is None 
                                 else 0,
                     'user_id':status.user.id,
                     'tweet_url':"http://twitter.com/"+status.user.id_str+"/status/"+status.id_str,
                     'retweet_count':status.retweet_count,
                     'original_tweet_id':status.retweeted_status.id 
                                        if not retweet and (status.retweet_count > 0)
                                        else 0,
		             'urls': status.entities['urls'],
                     'hashtags':status.entities['hashtags'],
                     'mentions': status.entities['user_mentions']
                     }
        
        #parse user object
        user = {
                'user_id':status.user.id,
                    'screen_name': status.user.screen_name,
                    'name': status.user.name,
                    'followers_count': status.user.followers_count,
                    'friends_count': status.user.friends_count,
                    'description': status.user.description 
                                   if not status.user.description is None
                                   else "N/A",
                    'image_url': status.user.profile_image_url,
                    'location': status.user.location
                                if not status.user.location is None
                                   else "N/A",
                    'created_at': status.user.created_at
                    }
        
        return {'tweet':tweet, 'user':user}
    
    def on_data(self, data):
        
        if 'in_reply_to_status_id' in data:
            status = Status.parse(self.api, json.loads(data))
            if self.on_status(status, data) is False:
                return False
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                 return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        
    def on_status(self, status, rawJsonData):
        try:
            #parse tweet
            tweet = self.parse_status(status)
            tweet['raw_json'] = rawJsonData
            self.tweetsBuffer.insert(tweet)
            
            #parse retweet
            if tweet['tweet']['retweet_count'] > 0:
                retweet = self.parse_status(status.retweeted_status, True)
                retweet['raw_json'] = None
                self.tweetsBuffer.insert(retweet)
                
        except Exception:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

class TweetsBuffer():
    tweetsBuffer = []
    
    def __init__(self):
        self.lock = threading.Lock()
        
    def insert(self, tweet):
        self.lock.acquire()
        self.tweetsBuffer.append(tweet)
        self.lock.release()
    
    def pop(self):
        self.lock.acquire()
        tweet = self.tweetsBuffer.pop() if len(self.tweetsBuffer) > 0 else None
        self.lock.release()
        return tweet
    
