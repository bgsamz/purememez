import requests
from meme_db import MemeDB

SLACK_FILES_INFO = 'https://slack.com/api/files.info'
DATABASE = MemeDB()


def download_meme(message_event, token):
    path = 'memes/{}.{}'.format(message_event['ts'], message_event['files'][0]['filetype'])

    # meme = tempfile.TemporaryFile()
    with open(path, 'wb') as meme:
        download = requests.get(message_event['files'][0]['url_private'],
                                headers={'Authorization': 'Bearer {}'.format(token)})
        if download.ok:
            meme.write(download.content)
            DATABASE.insert_meme(message_event)
        else:
            raise RuntimeError('Download failed.')

    return path


def delete_meme_file():
    return None
