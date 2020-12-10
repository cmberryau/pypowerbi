# -*- coding: future_fstrings -*-
from typing import List, Type, Any

import requests
import json

from requests.exceptions import HTTPError

from . import PowerBIClient
from .gateway import Gateway, GatewayDatasource, DatasourceUser
from .base import Deserializable


class Gateways:
    # url snippets
    gateways_snippet = 'gateways'
    datasources_snippet = 'datasources'
    users_snippet = 'users'

    # json keys
    odata_response_wrapper_key = 'value'

    def __init__(self, client: PowerBIClient):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

    def get_gateways(self) -> List[Gateway]:
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

        return self._models_from_get_multiple_response(response, Gateway)

    def get_datasources(self, gateway_id: str) -> List[GatewayDatasource]:
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

        return self._models_from_get_multiple_response(response, GatewayDatasource)

    def get_datasource_users(self, gateway_id: str, datasource_id: str) -> List[DatasourceUser]:
        """Returns a list of users who have access to the specified datasource

        :param gateway_id: The gateway id
        :param datasource_id: The datasource id
        """
        # form the url
        url = f'{self.base_url}/{self.gateways_snippet}/{gateway_id}' \
              f'/{self.datasources_snippet}/{datasource_id}/{self.users_snippet}'

        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Datasource Users request returned http error: {response.json()}')

        return self._models_from_get_multiple_response(response, DatasourceUser)

    @classmethod
    def _models_from_get_multiple_response(
            cls,
            response: requests.Response,
            model_class: Type[Deserializable]
    ) -> List[Any]:
        """Creates a list of models from a http response object

        :param response:
            The http response object
        :param model_class:
            The model to transform the response items into
        :return: list
            The list of model_class instances
        """

        # parse json response into a dict
        response_dict = json.loads(response.text)

        # Add parsed Gateway objects to list
        items = []
        for entry in response_dict[cls.odata_response_wrapper_key]:
            items.append(model_class.from_dict(entry))

        return items
