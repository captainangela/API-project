from urllib2 import urlopen
from json import load
from collections import defaultdict
from random import sample

#sf open data source: live health scores
apiUrl = "http://data.sfgov.org/api/views/pyih-qa8i/rows.json?"

#open the apiUrl and assign data to variable
response = urlopen(apiUrl)
json_obj = load(response)
data = json_obj['data']

def rest_name(r): 
	return r[9]

#get rid of duplicate rows
restaurants = {}
for row in data:
    # the last row has the latest health inspection
    restaurants[rest_name(row)] = row

#organize by zip code
zips = defaultdict(list)
for rest in restaurants.values():
	zip = rest[13]
	zips[zip].append(rest)

zip_code = raw_input("What San Francisco zip code will you be dining in today? ")

print "Here are 10 restaurants in your area: "
for rest in sample(zips[str(zip_code)], 10):
	print rest_name(rest)

