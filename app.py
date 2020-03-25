#! .env/bin/python

import json
import os.path as op

import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template


app = Flask('gg',
            template_folder='.',
            static_folder='static')


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/css/<path:path>')
def css(path):
    return app.send_static_file(op.join('css', path))


@app.route('/img/<path:path>')
def img(path):
    return app.send_static_file(op.join('img', path))


@app.route('/favicon.ico')
def fav():
    return app.send_static_file('favicon.ico')


@app.route('/data')
def data():
    url = "https://covid-19-data.p.rapidapi.com/totals"

    query = {"format":"json"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "b95d40efd0mshbd3d0586047cbabp156a05jsn3409b12c49c9"
    }

    data = requests.request('GET', url, headers=headers, params=query).json()[0]

    return json.dumps({
        'total': data['confirmed'],
        'deaths': data['deaths'],
        'recovered': data['recovered']
    })


@app.route('/countries')
def countries():
    result = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(result.content, 'html.parser')
    container = soup.find(id='countries').parent

    tabs = container.find(style='position:relative;')
    table = container.find(id='nav-tabContent')

    return {'html': ''.join(map(str, [tabs, table]))}


if __name__ == '__main__':
    app.run()
