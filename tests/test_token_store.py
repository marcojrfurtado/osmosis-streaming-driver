#  SPDX-License-Identifier: Apache-2.0
import pytest
import os
from datetime import datetime, timedelta

from osmosis_streaming_driver.proxy_server import TokenStore

TOKEN_STORE_TEST_DB = './test_token_store.db'


@pytest.fixture(autouse=True)
def before_each():
    if os.path.exists(TOKEN_STORE_TEST_DB):
        os.remove(TOKEN_STORE_TEST_DB)
    yield


def test_validate_token():
    store = TokenStore(TOKEN_STORE_TEST_DB)
    token = store.register('wss://some-url', expiration_date=datetime.now()+timedelta(hours=2))
    stream_url, expiration = store.get_token_attributes(token)
    assert expiration > datetime.now()
    assert stream_url == 'wss://some-url'


def test_validate_expired_token():
    store = TokenStore(TOKEN_STORE_TEST_DB)
    token = store.register('wss://some-url', expiration_date=datetime.now()-timedelta(hours=2))
    stream_url, expiration = store.get_token_attributes(token)
    assert expiration is None
    assert stream_url is None
    assert store.dump() == "[]"


def test_get_two_tokens_same_url():
    store = TokenStore(TOKEN_STORE_TEST_DB)
    expiration = datetime.now() + timedelta(hours=2)
    token1 = store.register('wss://some-url', expiration_date=expiration)
    token2 = store.register('wss://some-url', expiration_date=expiration)
    stream_url1, expiration1 = store.get_token_attributes(token1)
    stream_url2, expiration2 = store.get_token_attributes(token2)

    assert token1 != token2
    assert stream_url1 is not None
    assert stream_url1 == stream_url2
    assert expiration1 > datetime.now()
    assert expiration2 > datetime.now()
