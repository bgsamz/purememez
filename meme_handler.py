import requests
import os
import s3
from meme_db import MemeDB
from config import MEME_BUCKET

SLACK_FILES_INFO = 'https://slack.com/api/files.info'
DATABASE = MemeDB()
SUPPORTED_FILE_EXTENSIONS = (
    'tif',
    'tiff',
    'gif',
    'jpeg',
    'jpg',
    'png',
    'pdf'
)


def download_meme(message_event, token):
    extension = message_event['files'][0]['filetype']
    if extension not in SUPPORTED_FILE_EXTENSIONS:
        return None

    download = requests.get(message_event['files'][0]['url_private'],
                            headers={'Authorization': 'Bearer {}'.format(token)})
    if download.ok:
        print('Attempting to put file in bucket...')
        s3.put_stream(MEME_BUCKET, message_event['ts'], download.content)
        DATABASE.insert_meme(message_event)
    else:
        raise RuntimeError('Download failed.')

    return message_event['ts']


def readback_meme(ts):
    return s3.get(MEME_BUCKET, ts)


def delete_meme_file(path):
    if os.path.exists(path):
        os.remove(path)
