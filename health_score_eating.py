from flask import Flask, request, render_template
from urllib2 import urlopen
from json import load
from collections import defaultdict
from random import sample

app = Flask(__name__)

apiUrl = "http://data.sfgov.org/api/views/pyih-qa8i/rows.json?"
response = urlopen(apiUrl)
json_obj = load(response)
data = json_obj['data']

@app.route("/")
def index():
    return """
    <html>
      <body>
        <h1>Welcome!</h1>
        Click here to check for restaurants!
      </body>
    </html>
    """    

@app.route('/health')
def enter_zip_code():    
    return """
    <html>
    <head>
    <title>Health Scores</title>
    </head>
    <body>
        <form action='scores'>
            What zip code will you be dining in? 
            <input type ='text' name ='zip_code'>
            <input type ='submit'>
        </form>
    </body>
    </html> 
    """

@app.route('/scores')
def get_health_scores():
    zip_code = request.args.get('zip_code')
    
    restaurants = {}
    for row in data:
        restaurants[rest_name(row)] = row

    zips = defaultdict(list)
    for rest in restaurants.values():
        zip = rest[13]
        zips[zip].append(rest)

    rest_list = []
    for rest in sample(zips[str(zip_code)], 10):
        rest_list.append(rest_name(rest).title())
        risk = get_rating(rest)

    return render_template('health_score.html', restaurants = rest_list, zippy = zip_code)
    
def rest_name(name): 
    return name[9]

def get_rating(r):
    return r[-1]

#get rid of duplicate rows


#get the health rating
ratings = {}

#organize by zip code


if __name__ == "__main__":
    app.run(debug=True) 