# -*- coding: future_fstrings -*-

import json
from unittest import TestCase

from pypowerbi import *


class DatasetTests(TestCase):
    def test_row_json(self):
        row = Row(id=1, name='the name')
        self.assertIsNotNone(row)

        row_json = json.dumps(row, cls=RowEncoder)
        self.assertIsNotNone(row_json)

        expected_json = '{' \
                          '"id": 1, ' \
                          '"name": "the name"' \
                        '}'
        self.assertEqual(row_json, expected_json)

    def test_column_json(self):
        column = Column(name='theNameOfTheString', data_type='string')
        self.assertIsNotNone(column)

        column_json = json.dumps(column, cls=ColumnEncoder)
        self.assertIsNotNone(column_json)

        expected_json = '{' \
                          '"name": "theNameOfTheString", ' \
                          '"dataType": "string"' \
                        '}'
        self.assertEqual(column_json, expected_json)

    def test_table_json(self):
        column0 = Column(name='id', data_type='Int64')
        self.assertIsNotNone(column0)

        column1 = Column(name='name', data_type='string')
        self.assertIsNotNone(column1)

        table = Table(name='testTable', columns=[column0, column1])
        self.assertIsNotNone(table)

        table_json = json.dumps(table, cls=TableEncoder)
        self.assertIsNotNone(table_json)

        expected_json = '{' \
                          '"name": "testTable", ' \
                          '"columns": ' \
                            '[' \
                              '{' \
                                '"name": "id", ' \
                                '"dataType": "Int64"' \
                               '}, ' \
                               '{"name": "name", ' \
                                '"dataType": "string"' \
                               '}' \
                            ']' \
                        '}'
        self.assertEqual(table_json, expected_json)

    def test_dataset_json(self):
        column0 = Column(name='id', data_type='Int64')
        self.assertIsNotNone(column0)

        column1 = Column(name='name', data_type='string')
        self.assertIsNotNone(column1)

        table = Table(name='testTable', columns=[column0, column1])
        self.assertIsNotNone(table)

        dataset = Dataset(name=f'testDataset', tables=[table])
        self.assertIsNotNone(dataset)

        dataset_json = json.dumps(dataset, cls=DatasetEncoder)
        self.assertIsNotNone(dataset_json)

        expected_json = '{' \
                          '"name": "testDataset", ' \
                          '"tables": [' \
                            '{' \
                              '"name": "testTable", ' \
                              '"columns": [' \
                                '{' \
                                  '"name": "id", ' \
                                  '"dataType": "Int64"' \
                                '}, ' \
                                '{' \
                                  '"name": "name", ' \
                                  '"dataType": "string"' \
                                '}' \
                              ']' \
                            '}' \
                          ']' \
                        '}'

        self.assertEqual(dataset_json, expected_json)
