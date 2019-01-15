import sqlite3

class SQLInit:
    def __init__(self):
        self.conn = sqlite3.connect("main.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''
                CREATE TABLE IF NOT EXISTS `saves` (
                        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                        `name`	TEXT NOT NULL UNIQUE,
                        `content`	INTEGER NOT NULL,
                        `uses`	INTEGER NOT NULL,
                        `last_used`	NUMERIC,
                        `saved_by`	TEXT NOT NULL,
                        `time_added`	NUMERIC NOT NULL,
                        `approved_by`	TEXT NOT NULL
                );
                ''')
        self.conn.commit()