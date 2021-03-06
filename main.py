from flask import Flask
from flask import render_template
from flask import request
import json
import os
import datetime
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
    with urllib.request.urlopen(request_url) as response:
        raw_data = response.read()
    data = json.loads(raw_data)
    print(request_url)
    return data


unsplash_base_url ="https://api.unsplash.com"
unsplash_accesskey = "41aabcb9692e8453942ebefec22955f59dd254538a7900341bb7c6f5034eaadf"

def unsplash_api(method, params=None):
    parameters = params if params is not None else {}
    parameters.update({
        'client_id': unsplash_accesskey
    })
    url_params = urllib.parse.urlencode(parameters)
    request_url = '{}{}?{}'.format(unsplash_base_url, method, url_params)
    with urllib.request.urlopen(request_url) as response:
        raw_data = response.read()
    unsplash_data = json.loads(raw_data)
    print(request_url)
    return unsplash_data


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

    city_pics = unsplash_api('/search/photos', params={
        'query': city[0],
        'page': "1",
        'per_page': "10",
        'orientation': "landscape"
    })
    return render_template('results.html', title='Searching {} - Bon Voyage'.format(city), city=city, cityinfo=event.get('city', []),
                          event=sorted(event.get('events', []), key=lambda i: datetime.datetime.strptime('{} {}'.format(i.get('local_date'), i.get('local_time')), '%Y-%m-%d %H:%M')), city_pics=city_pics.get('results', []), startDate=startDate, endDate=endDate)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

