# -*- coding: future_fstrings -*-
import requests
import json
import urllib.parse

from requests.exceptions import HTTPError
from .group import Group


class Groups:
    # url snippets
    groups_snippet = 'groups'

    # json keys
    get_reports_value_key = 'value'

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

    def count(self):
        """
        Evaluates the number of groups that the client has access to
        :return: int
            The number of groups
        """
        return len(self.get_groups())

    def has_group(self, group_id):
        """
        Evaluates if client has access to the group
        :param group_id:
        :return: bool
            True if the client has access to the group, False otherwise
        """
        groups = self.get_groups()

        for group in groups:
            if group.id == str(group_id):
                return True

        return False

    def get_groups(self, filter_str=None, top=None, skip=None):
        """
        Fetches all groups that the client has access to
        :param filter_str: OData filter string to filter results
        :param top: int > 0, OData top parameter to limit to the top n results
        :param skip: int > 0,  OData skip parameter to skip the first n results
        :return: list
            The list of groups
        """
        query_parameters = []

        if filter_str:
            query_parameters.append(f'$filter={urllib.parse.quote(filter_str)}')

        if top:
            stripped_top = json.dumps(top).strip('"')
            query_parameters.append(f'$top={urllib.parse.quote(stripped_top)}')

        if skip:
            stripped_skip = json.dumps(skip).strip('"')
            query_parameters.append(f'$skip={urllib.parse.quote(stripped_skip)}')

        # form the url
        url = f'{self.base_url}/{self.groups_snippet}'

        # add query parameters to url if any
        if len(query_parameters) > 0:
            url += f'?{str.join("&", query_parameters)}'

        # form the headers
        headers = self.client.auth_header
        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Groups request returned http error: {response.json()}')

        return self.groups_from_get_groups_response(response)

    @classmethod
    def groups_from_get_groups_response(cls, response):
        """
        Creates a list of groups from a http response object
        :param response:
            The http response object
        :return: list
            The list of groups
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        groups = []

        # go through entries returned from API
        for entry in response_dict[cls.get_reports_value_key]:
            groups.append(Group.from_dict(entry))

        return groups
