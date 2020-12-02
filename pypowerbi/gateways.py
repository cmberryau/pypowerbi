# -*- coding: future_fstrings -*-
import requests
import json

from requests.exceptions import HTTPError
from .gateway import Gateway, GatewayDatasource


class Gateways:
    # url snippets
    gateways_snippet = 'gateways'
    datasources_snippet = 'datasources'

    # json keys
    odata_response_wrapper_key = 'value'

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
        for entry in response_dict[cls.odata_response_wrapper_key]:
            gateways.append(Gateway.from_dict(entry))

        return gateways

    def get_datasources(self, gateway_id):
        """Returns a list of datasources from the specified gateway

        :param gateway_id: The gateway id to return responses for
        :return: list
            The list of datasources
        """

        # form the url
        url = f'{self.base_url}/{self.gateways_snippet}/{gateway_id}/{self.datasources_snippet}'

        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Gateway Datasources request returned http error: {response.json()}')

        return self.datasources_from_get_datasources_response(response)

    @classmethod
    def datasources_from_get_datasources_response(cls, response):
        """Creates a list of gateway datasources from a http response object

        :param response:
            The http response object
        :return: list
            The list of gateway datasources
        """

        # parse json response into a dict
        response_dict = json.loads(response.text)

        # Add parsed Gateway objects to list
        gateway_datasources = []
        for entry in response_dict[cls.odata_response_wrapper_key]:
            gateway_datasources.append(GatewayDatasource.from_dict(entry))

        return gateway_datasources
