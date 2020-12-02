# -*- coding: future_fstrings -*-
import requests
import json

from requests.exceptions import HTTPError
from .gateway import Gateway


class Gateways:
    # url snippets
    gateways_snippet = 'gateways'

    # json keys
    get_gateways_value_key = 'value'

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

    def get_gateways(self):
        """Fetches all gateways the user is an admin for"""

        # form the url
        url = f'{self.base_url}/{self.gateways_snippet}'

        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Gateways request returned http error: {response.json()}')

        return self.gateways_from_get_gateways_response(response)


    @classmethod
    def gateways_from_get_gateways_response(cls, response):
        """Creates a list of gateways from a http response object

        :param response:
            The http response object
        :return: list
            The list of gateways
        """

        # parse json response into a dict
        response_dict = json.loads(response.text)

        # Add parsed Gateway objects to list
        gateways = []
        for entry in response_dict[cls.get_gateways_value_key]:
            gateways.append(Gateway.from_dict(entry))

        return gateways
