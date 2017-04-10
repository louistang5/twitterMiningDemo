__author__ = 'Louis'


# Finds the most commonly retweeted tweets?
# Taken from https://github.com/pablobarbera/pytwools/blob/master/top-tweets.py

import json

k = 5  # Number of top tweets to find
n = 1  # Minimum number of retweets allowed for list
file_in = 'themasters.json'


tweets = {}
fh = open(file_in, 'r')
for line in fh:
    try:
        tweet = json.loads(line) # Loads a line from the file
    except:
        continue # handle read-in error
    if 'retweeted_status' not in tweet:
        continue
    rt = tweet['retweeted_status']
    if rt['retweet_count'] < n: # Check that the number of retweets is above threshold
        continue
    tweets[rt['id_str']] = rt # store the tweets in dict, key is original user id

# convert to list
tweets = [tweets[w] for w in tweets.keys()]
# sort by retweet count
tweets.sort(key=lambda x: -x['retweet_count'])
# display top k retweets
for t in tweets[:k]:
    print('[' + t['user']['screen_name'] + ']: ' + t['text'] + ' [' + str(t['retweet_count']) + ' retweets]')

