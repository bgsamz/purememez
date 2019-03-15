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
                ts TEXT,
                file_name TEXT,
                user TEXT,
                reactions TEXT
            );
        """)

    def add_reaction(self, reaction_event):
        self.cursor.execute('SELECT reactions FROM meme_info WHERE ts=?', (reaction_event['item']['ts'],))
        row = self.cursor.fetchone()
        if row:
            reactions = json.loads(row['reactions'])
            if reaction_event['reaction'] in reactions:
                reactions[reaction_event['reaction']] += 1
            else:
                reactions[reaction_event['reaction']] = 1
            new_reactions = json.dumps(reactions)
            self.cursor.execute('UPDATE meme_info SET reactions=? WHERE ts=?', (new_reactions, reaction_event['item']['ts']))

    def remove_reaction(self, reaction_event):
        self.cursor.execute('SELECT reactions FROM meme_info WHERE ts=?', (reaction_event['item']['ts'],))
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
            new_reactions = json.dumps(reactions)
            self.cursor.execute('UPDATE meme_info SET reactions=? WHERE ts=?', (new_reactions, reaction_event['item']['ts']))

    def insert_meme(self, message_event):
        self.cursor.execute('INSERT INTO meme_info (ts, file_name, user, reactions) VALUES (?,?,?,?)',
                            (message_event['ts'], message_event['files'][0]['name'], message_event['user'], '{}'))

    def delete_meme(self, delete_event):
        self.cursor.execute('DELETE FROM meme_info WHERE ts=?', (delete_event['ts'],))

    def get_memes(self):
        self.cursor.execute('SELECT * FROM meme_info')
        rows = self.cursor.fetchall()
        messages = []
        for row in rows:
            reactions = json.loads(row['reactions'])
            key_list = []
            for key in reactions.keys():
                key_list.append(':{}:(x{})'.format(key, reactions[key]))
            formatted_reactions = ','.join(key_list)
            messages.append('Meme {} added by {} with the following reactions: {}'.format(row['file_name'], row['user'], formatted_reactions))
        return messages
