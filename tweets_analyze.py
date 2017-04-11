
import json
import re
from collections import Counter
from nltk.corpus import stopwords
import string
import vincent
from nltk import bigrams
from collections import defaultdict
from operator import itemgetter
import math


file_name = 'accident_unique.json'
s = 'accident'    # the word we are interested in a freq/time plot



def my_print(message, arr):
    print(message)
    print(arr)
    print('\n')


### build regular expression search patterns
# mostly taken from http://marcobonzanini.com/2015/03/17/mining-twitter-data-with-python-part-3-term-frequencies/
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)', # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


### get most frequent itmes (words, bigrams, co-occurrences)
# stopwords are taken from nltk, plus punctuation and some custom character strings.
punctuation = list(string.punctuation)
stop_words = stopwords.words('english') + punctuation + ['rt','via', '…']

# tokenize the tweets
com = defaultdict(lambda : defaultdict(int)) # co-occurrence matrix
timestamps = [] # store the timestamp of interested word
with open(file_name, 'r') as f:
    counts_words = Counter() # plain words, not hashtag, no @ sign
    counts_bigram = Counter() # bigram based on words
    counts_hash = Counter() # all hashtags
    for line in f:
        tweet = json.loads(line)
        tokens = preprocess(tweet['text'], lowercase=True)
        # Create a list with all the words
        words = [word for word in tokens
                 if word not in stop_words and
                 not word.startswith(('@'))]  # ignore @users
        words_bigram = bigrams(words)
        words_hash = [word for word in tokens if word not in stop_words and word.startswith('#')]
        # Update the counter
        counts_words.update(words)
        counts_bigram.update(words_bigram)
        counts_hash.update(words_hash)
        if s in words:
            timestamps.append(tweet['created_at']) # count frequencies of interested word

        # build co-occurrence matrix
        for i in range(len(words)-1):
            for j in range(i+1, len(words)):
                w1, w2 = sorted([words[i], words[j]])
                if w1 != w2:
                    com[w1][w2] += 1

# extract top k frequent co-occurrent words
k = 10
com_max = []
# look for the most common co-exist words for each word
for t1 in com:
    t1_max_words = sorted(com[t1].items(), key=itemgetter(1), reverse=True)[:k]
    for t2, t2_count in t1_max_words:
        com_max.append(((t1, t2), t2_count)) # append as a tuple
# get the most frequent co-occurrences
words_max = sorted(com_max, key=itemgetter(1), reverse=True)
my_print('top co-existed words: ', words_max[:k])

# Print the first n most frequent words
my_print('most frequent words:', counts_words.most_common(20))
my_print('most frequent hashtags:', counts_hash.most_common(20))
my_print('most frequent bigrams:', counts_bigram.most_common(20))



### freq visualization of interested item using vincent
# save bar plot in json, then render it in html
word_freq = counts_words.most_common(20)[1:]
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('word_freq.json')



### time series visualization using Pandas
import pandas
ones = [1]*len(timestamps)
idx = pandas.DatetimeIndex(timestamps)
keyword = pandas.Series(ones, index=idx)

# put all tweets into one bucket within x interval
resamp = keyword.resample('30s').sum().fillna(0)
freq_plot = vincent.Line(resamp)
freq_plot.legend(title=s)
freq_plot.axis_titles(x='Time', y='Freq')
freq_plot.to_json('freq_plot.json')
