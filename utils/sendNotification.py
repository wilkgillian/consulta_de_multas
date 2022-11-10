import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def post_message_to_teams(message: str):

    url = os.environ['URL']

    headers = {

        'Content-Type': 'application/json'
    }

    payload = {
        "text": message
    }

    requests.post(url, headers=headers, data=json.dumps(payload))
