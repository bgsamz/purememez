import sqlite3
import json
import random

MEME_DB_PATH = "memes.db"


class MemeDB:
    def __init__(self):
        self.connection = sqlite3.connect(MEME_DB_PATH, isolation_level=None)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS meme_info (
                ts TEXT NOT NULL PRIMARY KEY,
                file_name TEXT,
                file_type TEXT,
                user TEXT
            );
            
            CREATE TABLE IF NOT EXISTS meme_reactions (
                ts TEXT NOT NULL PRIMARY KEY REFERENCES meme_info(ts),
                reaction TEXT,
                count INTEGER
            );
            
            CREATE TABLE IF NOT EXISTS meme_labels (
                ts TEXT NOT NULL PRIMARY KEY REFERENCES meme_info(ts),
                label TEXT
            );
        """)

    def add_reaction(self, reaction_event):
        self.cursor.execute('SELECT * FROM meme_reactions WHERE ts=? AND reaction=?',
                            (reaction_event['item']['ts'], reaction_event['reaction']))
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute('UPDATE meme_reactions SET count=? WHERE ts=?',
                                (row['count']+1, reaction_event['item']['ts']))
        else:
            self.cursor.execute('INSERT INTO meme_reactions (ts, reaction, count) VALUES (?,?,?)',
                                (reaction_event['item']['ts'], reaction_event['reaction'], 1))

    def remove_reaction(self, reaction_event):
        self.cursor.execute('SELECT * FROM meme_reactions WHERE ts=? AND reaction=?',
                            (reaction_event['item']['ts'], reaction_event['reaction']))
        row = self.cursor.fetchone()
        if row:
            if row['count'] > 1:
                self.cursor.execute('UPDATE meme_reactions SET count=? WHERE ts=?',
                                    (row['count']-1, reaction_event['item']['ts']))
            else:
                self.cursor.execute('DELETE FROM meme_reactions WHERE ts=? AND reaction=?',
                                    (reaction_event['item']['ts'], reaction_event['reaction']))

    def add_label(self, ts, label):
        self.cursor.execute('INSERT INTO meme_labels (ts, label) VALUES (?,?)', (ts, label))

    def remove_label(self, ts, label):
        self.cursor.execute('DELETE FROM meme_labels WHERE ts=? AND label=?', (ts, label))

    def insert_meme(self, message_event):
        self.cursor.execute('INSERT INTO meme_info (ts, file_name, file_type, user) VALUES (?,?,?,?)',
                            (message_event['ts'], message_event['files'][0]['name'],
                             message_event['files'][0]['filetype'], message_event['user']))

    def delete_meme(self, delete_event):
        self.cursor.execute('DELETE FROM meme_info WHERE ts=?', (delete_event['ts'],))

    def get_meme_stats(self):
        self.cursor.execute('SELECT * FROM meme_info')
        rows = self.cursor.fetchall()
        messages = []
        for row in rows:
            reactions = json.loads(row['reactions'])
            key_list = []
            for key in reactions.keys():
                key_list.append(':{}:(x{})'.format(key, reactions[key]))
            formatted_reactions = ','.join(key_list)
            messages.append('Meme {} added by <@{}> with {} reactions: {}'
                            .format(row['file_name'], row['user'], row['reaction_count'], formatted_reactions))
        return messages

    def get_highest_rated_from_user(self, user):
        self.cursor.execute('SELECT meme_info.ts FROM meme_info '
                            'LEFT JOIN meme_reactions ON meme_info.ts = meme_reactions.ts '
                            'WHERE user=? GROUP BY meme_info.ts ORDER BY sum(count) DESC', (user,))
        rows = self.cursor.fetchone()
        return rows['ts']

    def get_random_meme_from_user(self, user):
        self.cursor.execute('SELECT * FROM meme_info WHERE user=?', (user,))
        rows = self.cursor.fetchall()
        return rows[random.randint(0, len(rows)-1)]['ts']

    def get_random_meme(self):
        self.cursor.execute('SELECT * FROM meme_info')
        rows = self.cursor.fetchall()
        return rows[random.randint(0, len(rows)-1)]['ts']

    def get_meme_by_label(self, label):
        self.cursor.execute('SELECT ts FROM meme_labels WHERE label=?', (label,))
        row = self.cursor.fetchone()
        return None if not row else row['ts']
