# -*- coding: future_fstrings -*-

import requests
import json

from .import_class import Import


class Imports:
    # url snippets
    groups_snippet = 'groups'
    imports_snippet = 'imports'
    dataset_displayname_snippet = 'datasetDisplayName'
    nameconflict_snippet = 'nameConflict'

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

    @classmethod
    def import_from_response(cls, response):
        response_dict = json.loads(response.text)
        return Import.from_dict(response_dict)

    @classmethod
    def imports_from_response(cls, response):
        response_list = json.loads(response.text).get(Import.value_key)
        return [Import.from_dict(x) for x in response_list]

    def upload_file(self, filename, dataset_displayname, nameconflict=None, group_id=None):
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        url = f'{self.base_url}{groups_part}{self.imports_snippet}' \
              f'?{self.dataset_displayname_snippet}={dataset_displayname}'

        if nameconflict is not None:
            url = url + f'&{self.nameconflict_snippet}={nameconflict}'

        with open(filename, 'rb') as file:
            headers = self.client.auth_header
            response = requests.post(url, headers=headers,
                                     files={
                                         'file': file,
                                     })
        # 200 OK
        if response.status_code == 200:
            import_object = self.import_from_response(response)
        # 202 Accepted
        elif response.status_code == 202:
            import_object = self.import_from_response(response)
        # 490 Conflict (due to name)
        elif response.status_code == 409:
            raise NotImplementedError
        else:
            raise RuntimeError(f"Upload file failed with status code: {response.status_code}")

        return import_object

    def get_import(self, import_id, group_id=None):
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        url = f'{self.base_url}{groups_part}{self.imports_snippet}/{import_id}'

        headers = self.client.auth_header
        response = requests.get(url, headers=headers)

        # 200 OK
        if response.status_code == 200:
            import_object = self.import_from_response(response)
        else:
            raise RuntimeError(f"Get import failed with status code: {response.status_code}")

        return import_object

    def get_imports(self, group_id=None):
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        url = f'{self.base_url}{groups_part}{self.imports_snippet}'

        headers = self.client.auth_header
        response = requests.get(url, headers=headers)

        # 200 OK
        if response.status_code == 200:
            import_object = self.imports_from_response(response)
        else:
            raise RuntimeError(f"Get imports failed with status code: {response.status_code}")

        return import_object
