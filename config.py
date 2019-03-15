import os
import json

FILEPATH = 'config.json'

data = None
if os.path.exists(FILEPATH):
    with open(FILEPATH) as config:
        data = json.load(config)


def reader(field):
    global data
    return data[field] if data is not None else os.getenv(field)


INSECURE_S3_ENABLED = reader('INSECURE_S3_ENABLED')
ACCESS_KEY = reader('S3_ACCESS_KEY')
SECRET_KEY = reader('S3_SECRET_KEY')
S3_ENDPOINT = reader('S3_ENDPOINT')
MEME_BUCKET = reader('BUCKET')
BOT_TOKEN = reader('SLACK_BOT_TOKEN')
