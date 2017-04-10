__author__ = 'Louis'

import tweepy
from tweepy import OAuthHandler

# my API key and access token
consumer_key = 'jA3znkS38FOVbM8wUXPioUCJ1'
consumer_secret = '8EI4d4UxtkOWlwz4RRuvgt3LsU5w5u8O7vMEUOPkE9O11xdbqa'
access_token = '455330550-UFz10z807V8NRTQ5bwlnVrID2Em8yIy1oTl9cNkR'
access_secret = '29vkaDd4vxglcY88bK8A48YnGJizQqO85rLQAoU3W28f7'

# set up connection using tweepy
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


import json
from tweepy import Stream
from tweepy.streaming import StreamListener

# store data here in JSON format
store_file = 'themasters.json'

# define my stream class
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open(store_file, 'a') as f:
                f.write(data) # save the tweets
                print(json.loads(data)["text"]) # print for debug
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

# start streaming with a filter or a topic
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['themasters'])

