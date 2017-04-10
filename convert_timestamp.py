__author__ = 'Louis'

# make a list of timestamps from a JSON twitter file. Save this list to ASCII file.

import json
import datetime

timestamps = [] # empty list
file_in = 'data.json'
file_out = 'timestamps.txt'

with open(file_in,'r') as f:
    for line in f:
        # Load single line from file
        tweet = json.loads(line)
        # Tag the quantities in Twitter timestamp
        pt = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        # Convert to seconds
        total_seconds = pt.day*3600*24 + pt.second + pt.minute*60 + pt.hour*3600
        with open(file_out, 'a') as output_file:
            # Record the timestamp by appending to file
            output_file.write("%s\n" % total_seconds)
