#  SPDX-License-Identifier: Apache-2.0
import pytest
from unittest import mock
from datetime import datetime, timedelta

from osmosis_streaming_driver.proxy_server.run import get_test_client

client = get_test_client()


def mocked_ws_connection(*args, **kwargs):
    class MockWebSocket:
        def __init__(self, stream_url):
            self.stream_url = stream_url

        def close(self):
            pass

        def recv(self):
            pass

    if 'wss://valid' in args[0]:
        return MockWebSocket(args[0])

    raise Exception('Invalid stream')


def mocked_register_url(*args, **kwargs):
    return 'Token'


def mocked_get_attributes_from_token(*args, **kwargs):
    token = args[0]
    if token == 'valid':
        return "wss://valid", datetime.now()
    return None, datetime.now()


def test_get_token_without_stream_url():
    assert client.get("/token").status_code == 400


@mock.patch('websocket.create_connection', side_effect=mocked_ws_connection)
@mock.patch('osmosis_streaming_driver.proxy_server.TokenStore.register', side_effect=mocked_register_url)
def test_get_token_valid_stream_no_expiration(mock_ws, mock_register):
    assert client.get("/token?stream_url=wss://valid").status_code == 400

@mock.patch('websocket.create_connection', side_effect=mocked_ws_connection)
@mock.patch('osmosis_streaming_driver.proxy_server.TokenStore.register', side_effect=mocked_register_url)
def test_get_token_valid_stream_with_expiration(mock_ws, mock_register):
    timestamp = datetime.now() + timedelta(hours=3)
    assert client.get(f"/token?stream_url=wss://valid&expires_at={timestamp.isoformat()}").status_code == 200

@mock.patch('websocket.create_connection', side_effect=mocked_ws_connection)
@mock.patch('osmosis_streaming_driver.proxy_server.TokenStore.register', side_effect=mocked_register_url)
def test_get_token_invalid_stream(mock_ws, mock_register):
    timestamp = datetime.now() + timedelta(hours=3)
    assert client.get(f"/token?stream_url=wss://invalid&expires_at={timestamp.isoformat()}").status_code == 500


@mock.patch('websocket.create_connection', side_effect=mocked_ws_connection)
def test_proxy_without_stream_url(mock_ws):
    assert client.get("/proxy").status_code == 400


@mock.patch('websocket.create_connection', side_effect=mocked_ws_connection)
@mock.patch('osmosis_streaming_driver.proxy_server.TokenStore.get_token_attributes', side_effect=mocked_get_attributes_from_token)
def test_proxy_valid_token(mock_ws, mock_get_stream_url):
    assert client.get("/proxy?token=valid").status_code == 200

@mock.patch('websocket.create_connection', side_effect=mocked_ws_connection)
@mock.patch('osmosis_streaming_driver.proxy_server.TokenStore.get_token_attributes', side_effect=mocked_get_attributes_from_token)
def test_proxy_invalid_token(mock_ws, mock_get_stream_url):
    assert client.get("/proxy?token=invalid").status_code == 401


