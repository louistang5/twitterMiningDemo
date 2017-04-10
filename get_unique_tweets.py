# now we have collected the tweets, let's do some basic
# statictics on them

import json

file_name = 'themasters.json'
output_file = 'themasters_unique.json'

# coding = 'utf-8'
# x = u'😘😘xyz😊😊'
# print([c for c in x])

# first, take a look at the structure of a tweet
with open(file_name, 'r') as f:
    line = f.readline()
    tweet = json.loads(line)
    print(json.dumps(tweet, indent=4))

# we are only interested in:
# content of tweet: 'text'
# whether it is a retweet: 'text' starts with RT
# whether it is retweeted: 'retweeted'
# post time of tweet: 'timestamp_ms'
#   or raw datetime format: 'created_at'

# first of all, we can count number of unique tweets and retweets
retweets = 0
unique = 0
with open(file_name, 'r') as f:
    for line in f:
        tweet = json.loads(line)
        # print tweet # for debug
        if tweet['text'][0:2] == 'RT':
            retweets += 1
        else:
            with open(output_file, 'a') as out_file:
                out_file.write(line)
            unique += 1

print('Unique tweets: %s' %unique)
print('Retweets: %s' %retweets)


