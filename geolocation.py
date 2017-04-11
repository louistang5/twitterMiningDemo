import json

file_name = 'accident.json'
geo_file = 'geo_data.json'

count = 0
with open(file_name, 'r')  as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for line in f:
        tweet = json.loads(line)
        if tweet['coordinates']:
            print(tweet['text'])
            count += 1
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                    "text": tweet['text'],
                    "created_at": tweet['created_at']
                }
            }
            geo_data['features'].append(geo_json_feature)

print('Number of tweets that has geo location: ' + str(count))

# save geo data
with open(geo_file, 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))
