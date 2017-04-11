__author__ = 'Louis'

import tweepy
from tweepy import OAuthHandler
import csv

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
from datetime import datetime

# store data in JSON format
json_file = 'test.json'

set_time = 1*60*60   # set time limit (in seconds)
start_time = datetime.now()

### define my stream class and save tweets into json file
class MyListener(StreamListener):
    def on_data(self, data):
        end_time = datetime.now()
        runtime = (end_time - start_time).total_seconds()
        if runtime > set_time:
            return False
        try:
            with open(json_file, 'a', newline='') as f:
                f.write(data)  # save the tweets
                print(json.loads(data)["text"]) # print for debug
                return True
        except BaseException as e:
            # print(datetime.now())
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        # print(datetime.now())
        print(status)
        return True


# ### or save it to a csv file
# csv_file = 'accident.csv'
# class MyListener(StreamListener):
#     def on_status(self, status):
#         end_time = datetime.now()
#         runtime = (end_time - start_time).total_seconds()
#         if runtime > set_time:
#             return False
#         try:
#             with open(csv_file, 'a', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow([status.author.screen_name, status.created_at, status.coordinates, status.text])
#                 print(status.author.screen_name, status.created_at, status.text)
#                 return True
#         except BaseException as e:
#             # print(datetime.now())
#             print("Error on_data: %s" % str(e))
#         return True
#
#     def on_error(self, status):
#         # print(datetime.now())
#         print(status)
#         return True


# start streaming with a filter or a topic
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(languages=['en'], track=['accident'])
