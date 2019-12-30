#  SPDX-License-Identifier: Apache-2.0
import pytest
from datetime import datetime, timedelta

from osmosis_streaming_driver.proxy_server import TokenStore


def test_validate_token():
    store = TokenStore()
    token = store.register('wss://some-url', expiration_date=datetime.now()+timedelta(hours=2))
    assert store.validate(token)
    assert store.get_stream_url(token) == 'wss://some-url'


def test_validate_expired_token():
    store = TokenStore()
    token = store.register('wss://some-url', expiration_date=datetime.now()-timedelta(hours=2))
    assert store.validate(token) is False
    assert store.get_stream_url(token) is None
    assert store.dump() == ""


def test_get_two_tokens_same_url():
    store = TokenStore()
    expiration = datetime.now() + timedelta(hours=2)
    token1 = store.register('wss://some-url', expiration_date=expiration)
    token2 = store.register('wss://some-url', expiration_date=expiration)
    assert token1 != token2
    assert store.validate(token1)
    assert store.validate(token2)
