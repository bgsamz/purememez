import requests
import tempfile

SLACK_FILES_INFO = 'https://slack.com/api/files.info'


def download_meme(file_id, token, bot):
    file = requests.get(SLACK_FILES_INFO, {'token': token, 'file': file_id}).json()['file']
    path = 'memes/{}'.format(file['name'])

    if file['user'] == bot:
        return None

    # meme = tempfile.TemporaryFile()
    with open(path, 'wb') as meme:
        download = requests.get(file['url_private'], headers={'Authorization': 'Bearer {}'.format(token)})
        if download.ok:
            meme.write(download.content)
        else:
            raise RuntimeError('Download failed.')

    return path
