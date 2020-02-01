# -*- coding: future_fstrings -*-
import datetime

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
