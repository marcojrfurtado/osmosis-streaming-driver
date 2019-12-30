from collections import OrderedDict
from random import randint
from hashlib import md5
from datetime import datetime


class TokenStore:

    def __init__(self):
        self._tokens = dict()
        self._expiration_map = OrderedDict()

    def register(self, stream_url, expiration_date):
        self._purge()
        token_input = str(stream_url + str(expiration_date) + str(randint(0, 100000))).encode()
        token = md5(token_input).hexdigest()
        self._insert(stream_url, token, expiration_date)
        return token

    def validate(self, token):
        self._purge()
        return token in self._tokens

    def get_stream_url(self, token):
        if not(self.validate(token)):
            return None
        return self._tokens[token]

    def dump(self):
        details_str = ""
        for expiration, token in self._expiration_map.items():
            details_str += "Token '%s' valid for stream '%s' expires at '%s';\n" % \
                           (token, self._tokens[token], expiration)
        return details_str

    def _insert(self, stream_url, token, expiration_date):
        self._tokens[token] = stream_url
        self._expiration_map[expiration_date] = token

    def _purge(self):
        now = datetime.now()
        to_delete = []
        for expiration, _ in self._expiration_map.items():
            if expiration > now:
                break
            to_delete.append(expiration)
        for expired_timestamp in to_delete:
            expired_token = self._expiration_map[expired_timestamp]
            del self._expiration_map[expired_timestamp]
            del self._tokens[expired_token]
