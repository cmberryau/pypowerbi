# -*- coding: future_fstrings -*-
import datetime
import json
from typing import Dict, Union, List
from copy import deepcopy

"""
This file contains helper and utility functions used elsewhere in the library.
"""


# Datetime's come in from PowerBI in the format 2019-03-05T03:09:31.493Z
_date_fmt_str = '%Y-%m-%dT%H:%M:%S.%fZ'
_date_fmt_str2 = '%Y-%m-%dT%H:%M:%SZ'


def date_from_powerbi_str(dstr):
    """
    Utility function to convert datetime strings from the Power BI service into Python Datetime objects

    :param dstr: A String retrieved from the Power BI Service that's a datetime
    :return: A Python datetime object generated from the parameter
    """
    if "." in dstr:
        return datetime.datetime.strptime(dstr, _date_fmt_str)
    else:
        # Fractional seconds are not zero padded in the API and will not be included at all if 0, thus the second format
        return datetime.datetime.strptime(dstr, _date_fmt_str2)


def convert_datetime_fields(list_of_dicts, fields_to_convert):
    """
    Takes in a list of dictionaries and for each dictionary it converts all fields in fields_to_convert to
    datetime objects from Power BI Datetime Strings. This is typically used when retrieving a list of records
    from the Power BI Service and you want all date fields to be converted from the date string to python datetimes.

    If the value of the field is None or an empty string, it does nothing for that field.

    :param list_of_dicts: A list of dictionaries
    :param fields_to_convert: A list of fields to be converted to datetimes from Power BI Datetime Strings
    :return: list of dictionaries with all fields specified in 'fields_to_convert' into python datetime objects
    """
    new_list = []
    for rec in list_of_dicts:
        # Create a copy so we don't overwrite the original dictionary
        new_rec = rec.copy()
        new_list.append(new_rec)
        for field in fields_to_convert:
            if field in new_rec.keys() and new_rec[field] not in [None, '']:
                new_rec[field] = date_from_powerbi_str(new_rec[field])

    return new_list


class CredentialsBuilder:
    """
    This class can be used to quickly generate credentials strings for use in a gateway.CredentialDetails object.
    Which methods to use depends on Which enums.CredentialType is passed along with the credentials in the constructor
    for gateway.CredentialDetails.
    """

    credential_data_key = "credentialData"
    username_key = "username"
    password_key = "password"
    key_key = "key"
    access_token_key = "accessToken"

    ANONYMOUS_DICT_TEMPLATE = {credential_data_key: ""}
    BASIC_DICT_TEMPLATE = {credential_data_key: [
        {
            "name": username_key,
            "value": ""
        },
        {
            "name": password_key,
            "value": ""
        }
    ]}

    KEY_DICT_TEMPLATE = {credential_data_key: [
        {
            "name": key_key,
            "value": ""
        }
    ]}

    OAUTH2_DICT_TEMPLATE = {credential_data_key: [
        {
            "name": access_token_key,
            "value": ""
        }
    ]}

    WINDOWS_DICT_TEMPLATE = BASIC_DICT_TEMPLATE

    @staticmethod
    def _serialize(credentials_dict: Dict[str, Union[str, List[Dict[str, str]]]]) -> str:
        # dump twice to get double quotes escaped properly
        # remove spaces between object keys and values
        # replace double backslashes with single slashes
        # remove double quotes at start and end of str
        return json.dumps(credentials_dict)\
            .replace(r'": ', r'":')\
            .replace('\\\\','\\')

    @classmethod
    def get_anonymous_credentials(cls) -> str:
        return cls._serialize(cls.ANONYMOUS_DICT_TEMPLATE)

    @classmethod
    def get_basic_credentials(cls, username: str, password: str) -> str:
        # use deepcopy to avoid mutability issues
        basic_credentials = deepcopy(cls.BASIC_DICT_TEMPLATE)
        # set username
        basic_credentials[cls.credential_data_key][0]["value"] = username
        # set password
        basic_credentials[cls.credential_data_key][1]["value"] = password

        return cls._serialize(basic_credentials)

    @classmethod
    def get_key_credentials(cls, key: str) -> str:
        # use deepcopy to avoid mutability issues
        key_credentials = deepcopy(cls.KEY_DICT_TEMPLATE)
        # set key
        key_credentials[cls.credential_data_key][0]["value"] = key

        return cls._serialize(key_credentials)

    @classmethod
    def get_o_auth_2_credentials(cls, access_token: str):
        # use deepcopy to avoid mutability issues
        o_auth_2_credentials = deepcopy(cls.OAUTH2_DICT_TEMPLATE)
        # set access token
        o_auth_2_credentials[cls.credential_data_key][0]["value"] = access_token

        return cls._serialize(o_auth_2_credentials)

    @classmethod
    def get_windows_credentials(cls, username: str, password: str):
        # use deepcopy to avoid mutability issues
        windows_credentials = deepcopy(cls.WINDOWS_DICT_TEMPLATE)
        # set username
        windows_credentials[cls.credential_data_key][0]["value"] = username
        # set password
        windows_credentials[cls.credential_data_key][1]["value"] = password

        return cls._serialize(windows_credentials)
