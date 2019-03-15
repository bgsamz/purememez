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

    path = 'memes/{}.{}'.format(message_event['ts'], extension)

    # meme = tempfile.TemporaryFile()
    with open(path, 'wb') as meme:
        download = requests.get(message_event['files'][0]['url_private'],
                                headers={'Authorization': 'Bearer {}'.format(token)})
        if download.ok:
            meme.write(download.content)
            DATABASE.insert_meme(message_event)
        else:
            raise RuntimeError('Download failed.')

    print('Attempting to put file in bucket...')
    s3.put_file(MEME_BUCKET, path.split('/')[1], path)

    return path


def delete_meme_file(path):
    if os.path.exists(path):
        os.remove(path)
