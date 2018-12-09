from flask import Flask
from flask import render_template
from flask import request
import json
import os
import urllib.parse
import urllib.request

base_url = 'https://api.meetup.com'
api_key = '55422e26d4d4459537924533f116b25'

def meetup_api(method, params=None):
    parameters = params if params is not None else {}
    parameters.update({
        'key': api_key,
        'sign': 'true'
    })
    url_params = urllib.parse.urlencode(parameters)
    request_url = '{}{}?{}'.format(base_url, method, url_params)
    print(request_url)
    with urllib.request.urlopen(request_url) as response:
        raw_data = response.read()
    data = json.loads(raw_data)
    return data


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html', title='Bon Voyage')

# get request to the python server (Flask)
@app.route('/step-one', strict_slashes=False)
def step_one():
    state = request.args.get('state')
    cities = meetup_api('/2/cities', params={
        'country': 'US',
        'state': state
    })
    return render_template('step-one.html', title='Searching {} - Bon Voyage'.format(state), state=state,
                           cities=cities.get('results', []))

@app.route('/results', strict_slashes=False)
# YYYY-MM-DDTHH:MM:SS.
# 01/09/2018
def results():
    city = request.args.get('city').split('+')
    date = request.args.get('daterange').split(" - ")
    startDate = date[0]
    startDate = ("{}-{}-{}{}").format(startDate[6:10], startDate[0:2], startDate[3:5], "T00:00:00")
    endDate = date[1]
    endDate = ("{}-{}-{}{}").format(endDate[6:10], endDate[0:2], endDate[3:5], "T00:00:00")
    event = meetup_api('/find/upcoming_events', params={
       'end_date_range': endDate,
       'start_date_range': startDate,
       'lat': city[1],
       'lon': city[2],
       'radius': '100',
       'page': "10"
    })
    return render_template('results.html', title='Searching {} - Bon Voyage'.format(city), city=city,
                          event=event.get('results', []))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

