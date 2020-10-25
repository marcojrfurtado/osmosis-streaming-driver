#  SPDX-License-Identifier: Apache-2.0
import pytest
from unittest import mock

from datetime import datetime, timedelta
from web3 import Web3

from osmosis_streaming_driver.data_plugin import Plugin
from osmosis_driver_interface.exceptions import OsmosisError

from osmosis_streaming_driver.proxy_server import PROXY_SERVER_PORT, PROXY_SERVER_HOST

plugin = Plugin()
web3 = Web3()

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status):
            self.text = text
            self.status = status

        def __bool__(self):
            return self.status < 400

    if 'wss://valid' in args[0]:
        return MockResponse('valid_token', 200)
    return MockResponse('', 400)


def test_driver_type():
    assert plugin.type() == 'Streaming'


@pytest.mark.xfail(raises=OsmosisError)
def test_generate_url_not_a_stream():
    plugin.generate_url('https://not-a-wss-stream', None, None)


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_generate_url_valid_stream(mock_get):
    stream_url = plugin.generate_url('wss://valid', None, None)
    assert stream_url == f'http://{PROXY_SERVER_HOST}:{PROXY_SERVER_PORT}/proxy?token=valid_token'


@pytest.mark.xfail(raises=OsmosisError)
@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_generate_url_invalid_stream(mock_get):
    plugin.generate_url('wss://invalid', None, None)

@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_generate_url_with_expiration(mock_get):
    class MockService:
        def get_cost(self):
            return '2'
    class MockTransferEventArgs:
        def __init__(self):
            self.value = web3.toWei(6, 'ether')
        
    transfer_event_args = MockTransferEventArgs()
    service = MockService()
    stream_url = plugin.generate_url('wss://valid', service, transfer_event_args)
    assert stream_url == f'http://{PROXY_SERVER_HOST}:{PROXY_SERVER_PORT}/proxy?token=valid_token'


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_ensure_correct_expiration(mock_get):
    class MockService:
        def get_cost(self):
            return '2'
    class MockTransferEventArgs:
        def __init__(self):
            self.value = web3.toWei(6, 'ether')
        
    transfer_event_args = MockTransferEventArgs()
    service = MockService()

    expiration = plugin.get_expiration_date(service, transfer_event_args)
    now = datetime.now()
    expected_expiration = now + timedelta(hours=3)
    assert expiration < expected_expiration + timedelta(minutes=5)
    assert expiration > expected_expiration - timedelta(minutes=5)

