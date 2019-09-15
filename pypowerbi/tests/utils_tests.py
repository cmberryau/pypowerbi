# -*- coding: future_fstrings -*-

import json
from unittest import TestCase

import datetime

from pypowerbi import utils

class UtilsTests(TestCase):
    def test_date_from_powerbi_str(self):
        now = datetime.datetime.now()
        power_bi_date_str = now.strftime(utils._date_fmt_str)
        now_converted = utils.date_from_powerbi_str(power_bi_date_str)
        self.assertEqual(now, now_converted)

    def test_convert_datetime_fields(self):

        # These are essentially random datetimes
        dt1 = datetime.datetime.now()
        dt2 = datetime.datetime(2019, 1, 4, 2, 4, 6, 23)
        dt3 = datetime.datetime(2017, 3, 7, 1, 12, 12, 23)

        # Convert them into Power BI Formatted Date Strings
        dt1_str = dt1.strftime(utils._date_fmt_str)
        dt2_str = dt2.strftime(utils._date_fmt_str)
        dt3_str = dt3.strftime(utils._date_fmt_str)

        # Build up several "Records" to convert. The dict_target dictionaries contain what the data should
        # look like after being converted.

        dict1 = {
            "col1": "Hello",
            "col2": dt1_str,
            "col3": dt2_str
        }

        dict1_target = dict1.copy()
        dict1_target["col2"] = dt1
        dict1_target["col3"] = dt2

        dict2 = {
            "col1": "World",
            "col2": dt3_str,
            "col3": None        # Make sure it doesn't try to convert None
        }
        dict2_target = dict2.copy()
        dict2_target["col2"] = dt3

        dict3 = {
            "col1": "World",
            "col2": '',         # Make sure it doesn't try to convert empty strings
            "col3": dt1_str
        }

        dict3_target = dict3.copy()
        dict3_target["col3"] = dt1

        sample_list = [dict1, dict2, dict3]

        target_list = [dict1_target, dict2_target, dict3_target]

        converted_list = utils.convert_datetime_fields(sample_list, ["col2", "col3"])

        for converted, target in zip(converted_list, target_list):
            self.assertEqual(converted, target)

