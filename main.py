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
    return render_template('home.html', title='Our App Name')


@app.route('/step-one', strict_slashes=False)
def step_one():
    state = request.args.get('state')
    cities = meetup_api('/2/cities', params={
        'country': 'US',
        'state': state
    })
    return render_template('step-one.html', title='Searching {} - Bon Voyage'.format(state), state=state,
                           cities=cities.get('results', []))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
