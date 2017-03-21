from flask import Flask, request, render_template
from urllib2 import urlopen
from json import load
from collections import defaultdict
from random import sample

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home_page.html')  

@app.route('/health')
def enter_zip_code():    
    return render_template('landing_page.html')

@app.route('/scores')
def get_health_scores():
    zip_code = request.args.get('zip_code')
    data = get_restaurant_data()
    
    restaurants = {}
    for row in data:
        restaurants[rest_name(row)] = row

    zips = defaultdict(list)
    for rest in restaurants.values():
        zip = rest[13]
        zips[zip].append(rest)

    eateries = {}
    for rest in sample(zips[str(zip_code)], 10):
        name = rest_name(rest).title()
        risk = get_rating(rest)
        eateries[name] = {'name': name, 'risk': risk}

    return render_template('health_score.html', eateries = eateries, zippy = zip_code)


def get_restaurant_data():
    apiUrl = "http://data.sfgov.org/api/views/pyih-qa8i/rows.json?"
    response = urlopen(apiUrl)
    json_obj = load(response)
    data = json_obj['data']
    return data

def rest_name(name): 
    return name[9]

def get_rating(rating):
    return rating[-1]

if __name__ == "__main__":
    app.run(debug=True) 