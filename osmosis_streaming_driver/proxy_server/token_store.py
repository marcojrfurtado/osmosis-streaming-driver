from random import randint
from hashlib import md5
from datetime import datetime
from dateutil.parser import parse as dateparse
import sqlite3
import contextlib

DEFAULT_TOKEN_STORE_DB = './token_store.db'


class TokenStore:
    def __init__(self, store_db_location=DEFAULT_TOKEN_STORE_DB):
        self._store_db = store_db_location
        self._create_table()

    def register(self, stream_url, expiration_date):
        self._purge()
        token_input = str(stream_url + str(expiration_date) + str(randint(0, 100000))).encode()
        token = md5(token_input).hexdigest()
        self._insert(stream_url, token, expiration_date)
        return token

    def get_token_attributes(self, token):
        self._purge()
        stream_url, expiration = None, None
        with sqlite3.connect(self._store_db) as con:
            with contextlib.closing(con.cursor()) as cursor:
                row = cursor.execute('SELECT stream_url, expiration from tokens '
                                     'WHERE token=?', (token,)).fetchone()
                if row:
                    stream_url, expiration = row[0], dateparse(row[1])

        return stream_url, expiration

    def dump(self):
        details_str = ""
        with sqlite3.connect(self._store_db) as con:
            with contextlib.closing(con.cursor()) as cursor:
                details_str += str(cursor.execute('SELECT * from tokens '
                                                  'ORDER BY expiration').fetchall())
        return details_str

    def _insert(self, stream_url, token, expiration_date):
        with sqlite3.connect(self._store_db) as con:
            with contextlib.closing(con.cursor()) as cursor:
                cursor.execute('INSERT INTO tokens(token,stream_url,expiration)'
                               'VALUES(?,?,?)', (token, stream_url, expiration_date))
        con.commit()

    def _create_table(self):
        with sqlite3.connect(self._store_db) as con:
            with contextlib.closing(con.cursor()) as cursor:
                cursor.execute('''CREATE TABLE IF NOT EXISTS tokens (
                                        id integer PRIMARY KEY,
                                        token text NOT NULL,
                                        stream_url text NOT NULL,
                                        expiration timestamp NOT NULL
                                    ); ''')
            con.commit()

    def _purge(self):
        # TODO: Should be stored in a ordered map
        # Using this because it works in a multi-process deployment
        with sqlite3.connect(self._store_db) as con:
            with contextlib.closing(con.cursor()) as cursor:
                cursor.execute('DELETE FROM tokens '
                               'WHERE expiration < ?', (datetime.now(),))
            con.commit()

