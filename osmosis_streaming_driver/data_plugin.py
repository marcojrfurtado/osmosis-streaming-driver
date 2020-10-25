#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import logging
import os
import requests

from datetime import datetime, timedelta
from web3 import Web3

from osmosis_driver_interface.data_plugin import AbstractPlugin
from osmosis_driver_interface.exceptions import OsmosisError
from osmosis_streaming_driver.proxy_server import PROXY_SERVER_PORT, PROXY_SERVER_HOST

web3 = Web3()
logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):
    STREAMING_PROXY_ENVVAR = 'STREAMING_PROXY'
    DEFAULT_STREAMING_PROXY = f'http://{PROXY_SERVER_HOST}:{PROXY_SERVER_PORT}'

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
    
    def get_expiration_date(self, service, transfer_event_args):
        if service is None or transfer_event_args is None:
            return None
        transfer_amount = round(web3.fromWei(int(transfer_event_args.value), 'ether'))
        hours_purchased = int(transfer_amount / int(service.get_cost()))
        logger.info(f'An amount of {str(transfer_amount)} has been transferred for the purchase of {hours_purchased} hours.')
        return datetime.now() + timedelta(hours=hours_purchased) 

    def _obtain_token(self, remote_file, expiration_date=None):
        new_token_url = f'{self._streaming_proxy}/token?stream_url={remote_file}'
        if expiration_date is not None:
            new_token_url += f'&expires_at={expiration_date.isoformat()}'
        res = requests.get(new_token_url)

        if not res:
            raise OsmosisError(f'Fetching token with "{new_token_url}"" failed. Status: {str(res.status_code)}; Reason: {str(res.content)}')

        return res.text
        

    def generate_url(self, remote_file, service, transfer_event_args):
        if not self._validate_wss_url(remote_file):
            raise OsmosisError(f'{remote_file} does not represent a valid websocket stream.')
        try:
            expiration_date = self.get_expiration_date(service, transfer_event_args)
            token = self._obtain_token(remote_file, expiration_date)
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
