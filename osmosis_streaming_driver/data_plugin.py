#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import logging
import os
import requests

from osmosis_driver_interface.data_plugin import AbstractPlugin
from osmosis_driver_interface.exceptions import OsmosisError
from .proxy_server import PROXY_SERVER_PORT

class Plugin(AbstractPlugin):
    STREAMING_PROXY_ENVVAR = 'STREAMING_PROXY'
    DEFAULT_STREAMING_PROXY = f'https://localhost:{PROXY_SERVER_PORT}'

    def __init__(self, config=None):
        self.config = config
        self._streaming_proxy = os.getenv(Plugin.STREAMING_PROXY_ENVVAR, Plugin.DEFAULT_STREAMING_PROXY)

    def type(self):
        """str: the type of this plugin (``'Streaming'``)"""
        return 'Streaming'

    def upload(self, local_file, remote_file):
        pass

    def download(self, remote_file, local_file):
        pass

    def list(self, remote_folder):
        pass

    @staticmethod
    def _validate_wss_url(stream_url):
        """Validate if it represents correctly a websocket stream
        Args:
             path(str): The path to check.
        """
        return stream_url.startswith('wss://')

    def _obtain_token(self, remote_file):
        new_token_url = f'{self._streaming_proxy}/token?stream_url={remote_file}'
        res = requests.get(new_token_url)
        if not res:
            raise OsmosisError(f'Fetching token for stream failed. '
                               f'Status: "{res.status}". Reason: "{res.text}"')
        return res.text

    def generate_url(self, remote_file):
        if not self._validate_wss_url(remote_file):
            raise OsmosisError(f'{remote_file} does not represent a valid websocket stream.')
        try:
            token = self._obtain_token(remote_file)
        except Exception as e:
            raise OsmosisError(f'Failed to obtain token for "{remote_file}" from proxy server. Reason: "{str(e)}"')

        return f'{self._streaming_proxy}/proxy?token={token}'

    def delete(self, remote_file):
        pass

    def copy(self, source_path, dest_path):
        pass

    def create_directory(self, remote_folder):
        pass

    def retrieve_availability_proof(self):
        pass
