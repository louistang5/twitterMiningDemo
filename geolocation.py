import json

file_name = 'tweets.json'
geo_file = 'geo_data.json'

with open(file_name, 'r')  as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for line in f:
        tweet = json.loads(line)
        if tweet['coordinates']:
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                    "text": tweet['text'],
                    "created_at": tweet['created_at']
                }
            }
            geo_data['features'].append(geo_json_feature)

# save geo data
with open(geo_file, 'a') as fout:
    fout.write(json.dumps(geo_data, indent=4))
