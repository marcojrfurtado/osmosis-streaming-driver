#  SPDX-License-Identifier: Apache-2.0
import pytest
from unittest import mock

from osmosis_streaming_driver.data_plugin import Plugin
from osmosis_driver_interface.exceptions import OsmosisError

from osmosis_streaming_driver.proxy_server import PROXY_SERVER_PORT, PROXY_SERVER_HOST

plugin = Plugin()


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status):
            self.text = text
            self.status = status

        def __bool__(self):
            return self.status < 400

    if args[0].endswith('wss://valid'):
        return MockResponse('valid_token', 200)
    return MockResponse('', 400)


def test_driver_type():
    assert plugin.type() == 'Streaming'


@pytest.mark.xfail(raises=OsmosisError)
def test_generate_url_not_a_stream():
    plugin.generate_url('https://not-a-wss-stream')


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_generate_url_valid_stream(mock_get):
    stream_url = plugin.generate_url('wss://valid')
    assert stream_url == f'http://{PROXY_SERVER_HOST}:{PROXY_SERVER_PORT}/proxy?token=valid_token'


@pytest.mark.xfail(raises=OsmosisError)
@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_generate_url_invalid_stream(mock_get):
    plugin.generate_url('wss://invalid')
