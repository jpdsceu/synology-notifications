import json
import os
import requests
import sys

from datetime import datetime
from pytz import timezone
from flask import Flask, request

# from gevent.pywsgi import WSGIServer

app = Flask(__name__)


def timenow():
    now = datetime.now(timezone('Europe/Amsterdam'))
    fmt = "%m/%d/%Y, %H:%M:%S"
    return now.strftime(fmt)


def send(data):
    payload = {
        "embeds": [
            {
                "title": "DSM notification",
                "description": data,
                "color": 36863,
                "footer": {
                    "text": f"{timenow()}",
                    "icon_url": "https://i.imgur.com/EO6Xw2A.jpg"
                }
            }
        ]
    }
    headers = {'Content-Type': 'Application/json; charset=utf-8'}
    print(payload)

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    print(f'response {response.reason}, {response.status_code}')

    return response.reason, response.status_code


@app.route('/', methods=['GET'])
def home_get():
    body = request.args.get('text')
    print(f'text {body}')

    return send(body)


@app.route('/', methods=['POST'])
def home_post():
    body = request.data
    if not body:
        return 'bad request', 400

    print(f'json {body}')

    try:
        synology_message = json.loads(body)['message']
        print(f'synology_message {synology_message}')
    except:
        return 'body not json', 400

    return send(synology_message)


if __name__ == '__main__':
    url = os.getenv('WEBHOOK_URL', None)
    if not url:
        print('No WEBHOOK_URL env var set!')
        sys.exit(1)

    # Debug/Development
    app.run(debug=True, host="0.0.0.0", port="8686")
    # Production
    # http_server = WSGIServer(('', 8686), app)
    # http_server.serve_forever()
