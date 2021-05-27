# -*- coding: future_fstrings -*-
import requests
import json
import urllib.parse

from requests.exceptions import HTTPError
from .group import Group
from .group_user import GroupUser


class Groups:
    # url snippets
    groups_snippet = 'groups'
    users_snippet = 'users'

    # json keys
    get_reports_value_key = 'value'

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

    def create_group(self, name, workspace_v2=False):
        """Creates a new workspace

        :param name: The name of the new group to create
        :param workspace_v2: Create a workspace V2
        :return: Group
            The newly created group
        """
        # validate request body
        if name is None or name == "":
            raise ValueError("Group name cannot be empty or None")

        # define request body
        body = {'name': name}

        # create url
        url = f'{self.base_url}/{self.groups_snippet}'

        uri_parameters = []

        if workspace_v2:
            stripped_workspace_v2 = json.dumps(workspace_v2).strip('"')
            uri_parameters.append(f'workspaceV2={urllib.parse.quote(stripped_workspace_v2)}')

        # add query parameters to url if any
        if len(uri_parameters) > 0:
            url += f'?{str.join("&", uri_parameters)}'

        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.post(url, headers=headers, json=body)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(f'Add group request returned the following http error: {response.json()}')

        return self.create_group_from_create_group_response(response)

    @staticmethod
    def create_group_from_create_group_response(response):
        """Creates a Group object from the response to a create_group call

        :param response:
            The http response object
        :return:
            Group object describing the newly created group
        """
        group_dict = json.loads(response.text)
        return Group.from_dict(group_dict)

    def add_group_user(self, group_id, group_user):
        """Adds a user to a group

        :param group_id:
            str - id of the group to add the user to
        :param group_user:
            GroupUser - Description of the user that should be added to the group
        :return:
            None
        """
        # validate request body
        if not isinstance(group_user, GroupUser):
            raise TypeError("group_user should be of type group_user.GroupUser !")

        # define request body
        body = group_user.as_set_values_dict()

        # create url
        stripped_group_id = json.dumps(group_id).strip('"')
        url = f'{self.base_url}/{self.groups_snippet}/{urllib.parse.quote(stripped_group_id)}/{self.users_snippet}'

        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.post(url, headers=headers, json=body)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            # add group user requests return an empty body; get the error from headers instead
            error_info = response.headers['x-powerbi-error-info']
            raise HTTPError(f'Add group request returned the following http error: {error_info}')

    def get_group_users(self, group_id):
        """
        Returns a list of users that have access to the specified workspace.
        GET https://api.powerbi.com/v1.0/myorg/groups/{groupId}/users
        
        :param group_id:
            str - id of the group to add the user to
        """
        # form the url
        url = f'{self.base_url}/{self.groups_snippet}/{group_id}/{self.users_snippet}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)
        # 200 - OK. Indicates success. List of reports.
        if response.status_code == 200:
            reports = self.users_from_get_group_users_response(response)
        else:
            raise HTTPError(response, f'Get reports request returned http error: {response.json()}')

        return reports
            
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

    @classmethod
    def users_from_get_group_users_response(cls, response):
        """
        Creates a list of users from a http response
        :param response: The response to create the users from
        :return: A list of users created from the http response
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        users = []
        # go through entries returned from API
        for entry in response_dict[cls.get_user_value_key]:
            users.append(GroupUser.from_dict(entry))

        return users
