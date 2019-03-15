import sqlite3
import json

MEME_DB_PATH = "memes.db"


class MemeDB:
    def __init__(self):
        self.connection = sqlite3.connect(MEME_DB_PATH, isolation_level=None)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS meme_info (
                meme_id TEXT,
                created INTEGER,
                meme_name TEXT,
                uploaded_by TEXT,
                reactions TEXT
            );
        """)

    def add_reaction(self, reaction_event):
        self.cursor.execute('SELECT reactions FROM meme_info WHERE meme_id=?', reaction_event['item']['file'])
        row = self.cursor.fetchone()
        if row:
            reactions = json.loads(row['reactions'])
            if reaction_event['reaction'] in reactions:
                reactions[reaction_event['reaction']] += 1
            else:
                reactions[reaction_event['reaction']] = 1
            new_reactions = json.dump(reactions)
            self.cursor.execute('UPDATE meme_info SET reactions=? WHERE meme_id=?', (new_reactions, reaction_event['item']['file']))

    def remove_reaction(self, reaction_event):
        self.cursor.execute('SELECT reactions FROM meme_info WHERE meme_id=?', reaction_event['item']['file'])
        row = self.cursor.fetchone()
        if row:
            reactions = json.loads(row['reactions'])
            if reaction_event['reaction'] in reactions:
                if reactions[reaction_event['reaction']] > 1:
                    reactions[reaction_event['reaction']] -= 1
                else:
                    del reactions[reaction_event['reaction']]
            else:
                return
            new_reactions = json.dump(reactions)
            self.cursor.execute('UPDATE meme_info SET reactions=? WHERE meme_id=?', (new_reactions, reaction_event['item']['file']))

    def insert_meme(self, file):
        self.cursor.execute('INSERT INTO meme_info (meme_id, created, meme_name, uploaded_by, reactions) VALUES (?,?,?,?,?)',
                            (file['id'], file['created'], file['name'], file['user'], '{}'))

    def delete_meme(self, file):
        self.cursor.execute('DELETE FROM meme_info WHERE meme_id=?', file['id'])

    def get_memes(self):
        self.cursor.execute('SELECT * FROM meme_info')
        rows = self.cursor.fetchall()
        messages = []
        for row in rows:
            reactions = json.loads(row['reactions'])
            key_list = []
            for key in reactions.keys():
                key_list.append(':{}:'.format(key))
            formatted_reactions = ','.join(key_list)
            messages.append('Meme {} added by {} with the following reactions: {}'.format(row['meme_name'], row['uploaded_by'], formatted_reactions))
        return messages
