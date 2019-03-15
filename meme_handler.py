import requests
from meme_db import MemeDB

SLACK_FILES_INFO = 'https://slack.com/api/files.info'
DATABASE = MemeDB()
SUPPORTED_FILE_EXTENSIONS = (
    '.tif',
    '.tiff',
    '.gif',
    '.jpeg',
    '.jpg',
    '.png',
    '.pdf'
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

    return path


def delete_meme_file():
    return None
