# -*- coding: future_fstrings -*-

import json
import datetime
import adal

from .reports import Reports
from .datasets import Datasets
from .imports import Imports
from .groups import Groups
from .activity_logs import ActivityLogs


class PowerBIClient:
    default_resource_url = 'https://analysis.windows.net/powerbi/api'
    default_api_url = 'https://api.powerbi.com'
    default_authority_url = 'https://login.windows.net/common'

    api_version_snippet = 'v1.0'
    api_myorg_snippet = 'myorg'

    @staticmethod
    def get_client_with_username_password(client_id, username, password, authority_url=None, resource_url=None, api_url=None):
        """
        Constructs a client with the option of using common defaults.

        :param client_id: The Power BI Client ID
        :param username: Username
        :param password: Password
        :param authority_url: The authority_url; defaults to 'https://login.windows.net/common'
        :param resource_url: The resource_url; defaults to 'https://analysis.windows.net/powerbi/api'
        :param api_url: The api_url: defaults to 'https://api.powerbi.com'
        :return:
        """
        if authority_url is None:
            authority_url = PowerBIClient.default_authority_url

        if resource_url is None:
            resource_url = PowerBIClient.default_resource_url

        if api_url is None:
            api_url = PowerBIClient.default_api_url

        context = adal.AuthenticationContext(authority=authority_url,
                                             validate_authority=True,
                                             api_version=None)

        # get your authentication token
        token = context.acquire_token_with_username_password(resource=resource_url,
                                                             client_id=client_id,
                                                             username=username,
                                                             password=password)

        return PowerBIClient(api_url, token)

    def __init__(self, api_url, token):
        self.api_url = api_url
        self.token = token
        self.datasets = Datasets(self)
        self.reports = Reports(self)
        self.imports = Imports(self)
        self.groups = Groups(self)
        self.activity_logs = ActivityLogs(self)

    @property
    def auth_header(self):
        if self._auth_header is None:
            self._auth_header = {
                'Authorization': f'Bearer {self.token["accessToken"]}'
            }

        return self._auth_header

    _auth_header = None


class EffectiveIdentity:
    username_key = 'username'
    roles_key = 'roles'
    datasets_key = 'datasets'

    def __init__(self, username, roles, datasets):
        self.username = username
        self.roles = roles
        self.datasets = datasets


class EffectiveIdentityEncoder(json.JSONEncoder):
    def default(self, o):
        return {
            EffectiveIdentity.username_key: o.username,
            EffectiveIdentity.roles_key: o.roles,
            EffectiveIdentity.datasets_key: o.datasets,
        }


class TokenRequest:
    access_level_key = 'accessLevel'
    dataset_id_key = 'datasetId'
    allow_saveas_key = 'allowSaveAs'
    identities_key = 'identities'

    def __init__(self, access_level, dataset_id=None, allow_saveas=None, identities=None):
        self.access_level = access_level
        self.dataset_id = dataset_id
        self.allow_saveas = allow_saveas
        self.identities = identities


class TokenRequestEncoder(json.JSONEncoder):
    def default(self, o):
        effective_identity_encoder = EffectiveIdentityEncoder()

        json_dict = {
            TokenRequest.access_level_key: o.access_level
        }

        if o.dataset_id is not None:
            json_dict[TokenRequest.dataset_id_key] = o.dataset_id

        if o.allow_saveas is not None:
            json_dict[TokenRequest.allow_saveas_key] = o.allow_saveas

        if o.identities is not None:
            json_dict[TokenRequest.identities_key] = [effective_identity_encoder.default(x) for x in o.identities]

        return json_dict


class EmbedToken:
    token_key = 'token'
    token_id_key = 'tokenId'
    expiration_key = 'expiration'

    def __init__(self, token, token_id, expiration):
        self.token = token
        self.token_id = token_id
        self.expiration = expiration

    @classmethod
    def from_dict(cls, dictionary):
        if cls.token_key not in dictionary:
            raise RuntimeError(f'Token dict has no {cls.token_key} key')

        token = dictionary[cls.token_key]
        token_id = dictionary[cls.token_id_key]
        expiration = dictionary[cls.expiration_key]

        return EmbedToken(token, token_id, expiration)

    @property
    def expiration_as_datetime(self):
        return datetime.datetime.strptime(self.expiration, '%Y-%m-%dT%H:%M:%SZ')
