# -*- coding: future_fstrings -*-
import requests
import json

from requests.exceptions import HTTPError


class Features:
    # url snippets
    features_snippet = 'availableFeatures'

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

    @property
    def embed_trial(self):
        feat = self.get_available_features(feature_name='embedTrial')
        feat.usage = feat.additional_info['usage']
        return feat

    @property
    def automatically_push_app_to_end_user(self):
        return self.get_available_features(feature_name='automaticallyPushAppToEndUsers')

    @property
    def publish_app_to_entire_organization(self):
        return self.get_available_features(feature_name='publishAppToEntireOrganization')

    def get_available_features(self, feature_name=None):
        # If feature_name is none, returns all the available features
        if feature_name is not None:
            feature_part = f"(featureName='{feature_name}')"
        else:
            feature_part = ''

        # form the url
        url = f"{self.base_url}/{self.features_snippet}{feature_part}"
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Datasets request returned http error: {response.json()}')

        return Features.features_from_get_available_features_response(response)

    @staticmethod
    def features_from_get_available_features_response(response):
        response_dict = json.loads(response.text)

        # check wether we are returning a single feature or a list of features
        if 'features' in response_dict:
            features_list = []
            for feature in response_dict['features']:
                additional_info = feature[Feature.additional_info_key] if Feature.additional_info_key in feature else  None
                features_list.append(Feature(
                    feature[Feature.name_key],
                    feature[Feature.state_key],
                    feature[Feature.extended_state_key],
                    additional_info
                    ))
            return features_list
        else:
            additional_info = response_dict[Feature.additional_info_key] if Feature.additional_info_key in response_dict else  None
            return Feature(
                response_dict[Feature.name_key],
                response_dict[Feature.state_key],
                response_dict[Feature.extended_state_key],
                additional_info
                )


class Feature:
    name_key = 'name'
    state_key = 'state'
    extended_state_key = 'extendedState'
    additional_info_key = 'additionalInfo'

    def __init__(self, name, state, extended_state, additional_info=None):
        self.name = name
        self.state = state
        self.extended_state = extended_state

        if additional_info is not None:
            self.additional_info = additional_info
