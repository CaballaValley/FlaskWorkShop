from random import sample, randint

from flask import Flask, abort, jsonify
import requests

app = Flask(__name__)


ANIMALS = ['cat', 'dog', 'fish', 'monkey']


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500


@app.route('/random/animals')
def random_animals():
    return {
        'animals': sample(ANIMALS, randint(1, len(ANIMALS)-1))
    }


@app.route('/random/<animals>')
def random_remote_animals(animals):
    try:
        remote_request = requests.get(
            f'http://127.0.0.1:5002/{animals}'
        )
        data = remote_request.json()
    except Exception as e:
        abort(500, description=e)

    data = {}

    if remote_request.status_code == 200:
        data['animals'] = remote_request.json()
    else:
        abort(500, description="Resource not found in remote API")

    return data
