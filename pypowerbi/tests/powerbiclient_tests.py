# -*- coding: future_fstrings -*-

import adal
import datetime
import time
from unittest import TestCase

from pypowerbi.client import *
from pypowerbi.reports import *
from pypowerbi.report import *
from pypowerbi.datasets import *
from pypowerbi.dataset import *
from pypowerbi.imports import *
from pypowerbi.import_class import *
from pypowerbi.tests.settings import PowerBITestSettings


class PowerBIAPITests(TestCase):
    # default testing urls
    authority_url = PowerBITestSettings.authority_url
    resource_url = PowerBITestSettings.resource_url
    api_url = PowerBITestSettings.api_url

    # default testing credentials
    client_id = PowerBITestSettings.client_id
    username = PowerBITestSettings.username
    password = PowerBITestSettings.password
    group_ids = PowerBITestSettings.group_ids

    # default test prefixes
    test_dataset_prefix = 'testDataset_'
    test_report_prefix = 'testReport_'
    test_table_prefix = 'testTable_'

    dataset_counts = {}
    report_counts = {}
    client = None

    @classmethod
    def tearDownClass(cls):
        client = PowerBIClient(cls.api_url, PowerBIAPITests().get_token())

        for group_id in cls.group_ids:
            cls.delete_test_datasets(client, group_id)
            cls.delete_test_reports(client, group_id)

    def setUp(self):
        self.client = PowerBIClient(self.api_url, self.get_token())

        # delete and count assets for each group
        for group_id in self.group_ids:
            self.delete_test_assets(self.client, group_id)
            self.count_assets(self.client, group_id)

    def delete_test_assets(self, client, group_id):
        self.delete_test_datasets(client, group_id)
        self.delete_test_reports(client, group_id)

    def count_assets(self, client, group_id):
        self.dataset_counts[group_id] = client.datasets.count(group_id)
        self.report_counts[group_id] = client.reports.count(group_id)

    @classmethod
    def delete_test_datasets(cls, client, group_id=None):
        datasets = client.datasets.get_datasets(group_id)
        for dataset in datasets:
            if cls.test_dataset_prefix in dataset.name:
                client.datasets.delete_dataset(dataset.id, group_id)

    @classmethod
    def delete_test_reports(cls, client, group_id=None):
        reports = client.reports.get_reports(group_id)
        for report in reports:
            if cls.test_report_prefix in report.name:
                client.reports.delete_report(report.id, group_id)

    @classmethod
    def add_mock_dataset(cls, client, table_count=1, group_id=None):
        tables = cls.create_mock_tables(table_count)

        # create the dataset
        dataset = Dataset(name=f'{cls.test_dataset_prefix}{datetime.datetime.utcnow()}', tables=tables)

        # post and return the result
        return client.datasets.post_dataset(dataset, group_id)

    @classmethod
    def add_mock_dataset_with_tables(cls, client, tables, group_id=None):
        # create the dataset
        dataset = Dataset(name=f'{cls.test_dataset_prefix}{datetime.datetime.utcnow()}', tables=tables)

        # post and return the result
        return client.datasets.post_dataset(dataset, group_id)

    @classmethod
    def create_mock_tables(cls, table_count):
        tables = []
        for x in range(0, table_count):
            # we add a column of each type for each table
            columns = [
                Column(name='id', data_type='Int64'),
                Column(name='name', data_type='string'),
                Column(name='is_interesting', data_type='boolean'),
                Column(name='cost_usd', data_type='double'),
                Column(name='purchase_date', data_type='datetime'),
            ]

            table_name = f'{cls.test_table_prefix}{x}'

            measures = [
                Measure(name=f'entry_count_{x}', expression=f'COUNTROWS( \'{table_name}\' )')
            ]

            # add the table
            tables.append(Table(name=table_name, columns=columns, measures=measures))

        return tables

    @classmethod
    def add_mock_report(cls, client, group_id):
        # to add a mock report, we clone an existing one
        reports = client.reports.get_reports(group_id)
        return client.reports.clone_report(reports[0].id,
                                           f'{cls.test_report_prefix}'
                                           f'{datetime.datetime.utcnow()}',
                                           group_id,
                                           reports[0].dataset_id, group_id)

    def get_token(self):
        context = adal.AuthenticationContext(authority=self.authority_url,
                                             validate_authority=True,
                                             api_version=None)

        return context.acquire_token_with_username_password(resource=self.resource_url,
                                                            client_id=self.client_id,
                                                            username=self.username,
                                                            password=self.password)

    def assert_datasets_valid(self, datasets):
        self.assertIsNotNone(datasets)

        for dataset in datasets:
            self.assert_dataset_valid(dataset)

    def assert_dataset_valid(self, dataset):
        self.assertIsNotNone(dataset)
        self.assertIsNotNone(dataset.id)
        self.assertIsNotNone(dataset.name)

    def assert_reports_valid(self, reports):
        self.assertIsNotNone(reports)

        for report in reports:
            self.assert_report_valid(report)

    def assert_report_valid(self, report):
        self.assertIsNotNone(report)
        self.assertIsNotNone(report.id)
        self.assertIsNotNone(report.name)
        self.assertIsNotNone(report.web_url)
        self.assertIsNotNone(report.embed_url)
        self.assertIsNotNone(report.dataset_id)

    def test_aad_auth(self):
        self.assertIsNotNone(self.get_token())

    def test_client_get_datasets(self):
        for group_id in self.group_ids:
            self._test_client_get_datasets_impl(self.client, group_id)

    def _test_client_get_datasets_impl(self, client, group_id=None):
        # validate our initial number of datasets
        datasets = client.datasets.get_datasets(group_id)
        # validate our datasets and the count
        self.assert_datasets_valid(datasets)
        self.assertEqual(len(datasets), 0 + self.dataset_counts[group_id])

        # add a mock dataset
        self.add_mock_dataset(client, group_id=group_id)

        # validate that we now have one more than before
        datasets = client.datasets.get_datasets(group_id)
        # validate our datasets and the count
        self.assert_datasets_valid(datasets)
        self.assertEqual(len(datasets), 1 + self.dataset_counts[group_id])

        # add another
        self.add_mock_dataset(client, group_id=group_id)

        # validate that we now have one more than before
        datasets = client.datasets.get_datasets(group_id)
        # validate our datasets and the count
        self.assert_datasets_valid(datasets)
        self.assertEqual(len(datasets), 2 + self.dataset_counts[group_id])

    def test_client_get_dataset(self):
        for group_id in self.group_ids:
            self._test_client_get_dataset_impl(self.client, group_id)

    def _test_client_get_dataset_impl(self, client, group_id=None):
        # add a mock dataset
        self.add_mock_dataset(client, group_id=group_id)
        # validate that we have some valid datasets
        datasets = client.datasets.get_datasets(group_id)
        self.assertGreater(len(datasets), 0)
        self.assert_datasets_valid(datasets)

        # validate that the single dataset get is what we expect
        dataset = client.datasets.get_dataset(datasets[0].id, group_id)
        self.assert_dataset_valid(dataset)
        self.assertDictEqual(datasets[0].__dict__, dataset.__dict__)

    def test_client_post_dataset(self):
        for group_id in self.group_ids:
            self._test_client_post_dataset_impl(self.client, group_id)

    def _test_client_post_dataset_impl(self, client, group_id=None):
        # validate that we have 0 additional datasets
        datasets = client.datasets.get_datasets(group_id)
        self.assert_datasets_valid(datasets)
        self.assertEqual(len(datasets), 0 + self.dataset_counts[group_id])

        # we add a column of each type
        columns = [
            Column(name='id', data_type='Int64'),
            Column(name='name', data_type='string'),
            Column(name='is_interesting', data_type='boolean'),
            Column(name='cost_usd', data_type='double'),
            Column(name='purchase_date', data_type='datetime')
        ]

        table_name = f'{self.test_table_prefix}0'

        # add a measure
        measures = [
            Measure(name='entry_count_0', expression=f'COUNTROWS( \'{table_name}\' )')
        ]

        table = Table(name=table_name, columns=columns, measures=measures)
        dataset_name = f'{self.test_dataset_prefix}{datetime.datetime.utcnow()}'
        dataset = Dataset(name=dataset_name, tables=[table])

        # validate that the returned dataset is what we expected to be posted
        returned_dataset = client.datasets.post_dataset(dataset, group_id)

        self.assert_dataset_valid(returned_dataset)
        self.assertEqual(dataset_name, returned_dataset.name)

        # validate that we now have one more dataset
        datasets = client.datasets.get_datasets(group_id)
        self.assert_datasets_valid(datasets)
        self.assertEqual(len(datasets), 1 + self.dataset_counts[group_id])

    def test_client_delete_dataset(self):
        for group_id in self.group_ids:
            self._test_client_delete_dataset_impl(self.client, group_id)

    def _test_client_delete_dataset_impl(self, client, group_id=None):
        # validate our initial number of datasets
        datasets = client.datasets.get_datasets(group_id)
        self.assert_datasets_valid(datasets)
        self.assertEqual(len(datasets), 0 + self.dataset_counts[group_id])

        # add another dataset
        dataset = self.add_mock_dataset(client, group_id=group_id)

        # validate that we have an additional dataset
        datasets = client.datasets.get_datasets(group_id)
        self.assertEqual(len(datasets), 1 + self.dataset_counts[group_id])

        # delete a dataset
        client.datasets.delete_dataset(dataset.id, group_id)

        # validate that we have deleted the dataset
        datasets = client.datasets.get_datasets(group_id)
        self.assertEqual(len(datasets), 0 + self.dataset_counts[group_id])

        # ensure no returned dataset has the deleted dataset id
        for returned_dataset in datasets:
            self.assertNotEqual(dataset.id, returned_dataset.id)

    def test_client_get_tables(self):
        for group_id in self.group_ids:
            self._test_client_get_tables_impl(self.client, group_id)

    def _test_client_get_tables_impl(self, client, group_id=None):
        dataset = self.add_mock_dataset(client, 1, group_id)
        tables = client.datasets.get_tables(dataset.id, group_id)

        # make sure that we get one table back
        self.assertIsNotNone(tables)
        self.assertEqual(len(tables), 1)

        # make sure that the tables are named as expected
        for table in tables:
            self.assertIn(self.test_table_prefix, table.name)

        # add another dataset, but with two tables
        dataset = self.add_mock_dataset(client, 2, group_id)
        tables = client.datasets.get_tables(dataset.id, group_id)

        # make sure that we get two tables back
        self.assertIsNotNone(tables)
        self.assertEqual(len(tables), 2)

        # make sure that the tables are named as expected
        for table in tables:
            self.assertIn(self.test_table_prefix, table.name)

    def test_client_get_dataset_parameters(self):
        for group_id in self.group_ids:
            self._test_client_get_dataset_parameters_impl(self.client, group_id)

    def _test_client_get_dataset_parameters_impl(self, client, group_id=None):
        dataset = self.add_mock_dataset(client, 1, group_id)
        parameters = client.datasets.get_dataset_parameters(dataset.id, group_id)

        # make sure that we get some parameters back
        self.assertIsNotNone(parameters)

    def test_client_post_rows(self):
        for group_id in self.group_ids:
            self._test_client_post_rows_impl(self.client, group_id)

    def _test_client_post_rows_impl(self, client, group_id=None):
        dataset = self.add_mock_dataset(client, 1, group_id)
        tables = client.datasets.get_tables(dataset.id, group_id)

        row0 = Row(id=1, name='yabbadabba')
        row1 = Row(id=2, name='oogabooga')

        client.datasets.post_rows(dataset.id, tables[0].name, [row0, row1], group_id)
        tables = client.datasets.get_tables(dataset.id, group_id)

        self.assertIsNotNone(tables)
        self.assertEqual(len(tables), 1)

        # we have no way to validate rows at this point, powerbi api does not allow row queries

    def test_client_delete_rows(self):
        for group_id in self.group_ids:
            self._test_client_delete_rows_impl(self.client, group_id)

    def _test_client_delete_rows_impl(self, client, group_id=None):
        dataset = self.add_mock_dataset(client, 1, group_id)
        tables = client.datasets.get_tables(dataset.id, group_id)

        row0 = Row(id=1, name='yabbadabba')
        row1 = Row(id=2, name='oogabooga')

        client.datasets.post_rows(dataset.id, tables[0].name, [row0, row1], group_id)
        client.datasets.delete_rows(dataset.id, tables[0].name, group_id)

        # we have no way to validate rows at this point, powerbi api does not allow row queries

    def test_client_get_reports(self):
        for group_id in self.group_ids:
            self._test_client_get_reports_impl(self.client, group_id)

    def _test_client_get_reports_impl(self, client, group_id=None):
        reports = client.reports.get_reports(group_id)

        # validate that we got valid reports
        self.assert_reports_valid(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), self.report_counts[group_id])

    def test_client_get_report(self):
        for group_id in self.group_ids:
            self._test_client_get_report_impl(self.client, group_id)

    def _test_client_get_report_impl(self, client, group_id=None):
        reports = client.reports.get_reports(group_id)

        # validate that we got reports
        self.assert_reports_valid(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), self.report_counts[group_id])

        # validate that they are valid
        self.assert_reports_valid(reports)

        # get a specific report using the first report id
        report = client.reports.get_report(reports[0].id, group_id)

        # validate that the returned report is valid
        self.assert_report_valid(report)

        # validate that the first report and the fetched report are the same
        self.assertDictEqual(reports[0].__dict__, report.__dict__)

    def test_client_clone_report(self):
        for group_id in self.group_ids:
            self._test_client_clone_report_impl(self.client, group_id)

    def _test_client_clone_report_impl(self, client, group_id=None):
        reports = client.reports.get_reports(group_id)

        # validate that we got reports
        self.assert_reports_valid(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), self.report_counts[group_id])

        # validate that they are valid
        self.assert_reports_valid(reports)

        # close the first report
        report = client.reports.clone_report(reports[0].id,
                                             f'{self.test_report_prefix}'
                                             f'{datetime.datetime.utcnow()}',
                                             None,
                                             reports[0].dataset_id, group_id)

        # validate that the cloned report is valid
        self.assert_report_valid(report)

        # validate that the cloned report differs from the original where relevant
        self.assertNotEqual(report.id, reports[0].id)
        self.assertIsNotNone(report.name)
        self.assertNotEqual(report.name, reports[0].name)
        self.assertIsNotNone(report.web_url)
        self.assertNotEqual(report.web_url, reports[0].web_url)
        self.assertIsNotNone(report.embed_url)
        self.assertNotEqual(report.embed_url, reports[0].embed_url)
        self.assertIsNotNone(report.dataset_id)

        # validate that the cloned report does not differ from the original where valid
        self.assertEqual(report.dataset_id, reports[0].dataset_id)

        # validate that the report was actually cloned
        reports = client.reports.get_reports(group_id)

        # validate that we got reports
        self.assert_reports_valid(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), 1 + self.report_counts[group_id])

        # validate that the reports are valid
        self.assert_reports_valid(reports)

    def test_client_delete_report(self):
        for group_id in self.group_ids:
            self._test_client_delete_report_impl(self.client, group_id)

    def _test_client_delete_report_impl(self, client, group_id=None):
        reports = client.reports.get_reports(group_id)

        # validate that we got reports
        self.assert_reports_valid(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), self.report_counts[group_id])

        # validate that the reports are valid
        self.assert_reports_valid(reports)

        # add a mock report
        report = self.add_mock_report(client, group_id)

        # validate that the number of reports has increased
        reports = client.reports.get_reports(group_id)

        # validate that we got reports
        self.assert_reports_valid(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), 1 + self.report_counts[group_id])

        # validate that the reports are valid
        self.assert_reports_valid(reports)

        # delete the previously added report
        client.reports.delete_report(report.id, group_id)

        # validate that the number of reports is one less
        reports = client.reports.get_reports(group_id)

        # validate that we got reports
        self.assert_reports_valid(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), self.report_counts[group_id])

        # validate that the reports are valid
        self.assert_reports_valid(reports)

    def test_client_rebind_report(self):
        for group_id in self.group_ids:
            self._test_client_rebind_report_impl(self.client, group_id)

    def _test_client_rebind_report_impl(self, client, group_id=None):
        # get the current reports
        reports = client.reports.get_reports(group_id)

        # validate that we got reports
        self.assert_reports_valid(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), self.report_counts[group_id])

        # validate that the reports are valid
        self.assert_reports_valid(reports)

        # rebind the first report to the second report's dataset
        client.reports.rebind_report(reports[0].id, reports[1].dataset_id, group_id)

        # get the reports again
        reports = client.reports.get_reports(group_id)

        # validate that we got reports
        self.assertIsNotNone(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), self.report_counts[group_id])

        # validate that the reports are valid
        self.assert_reports_valid(reports)

        # validate that the report has been rebound
        self.assertEqual(reports[0].dataset_id, reports[1].dataset_id)

    def test_generate_report_token(self):
        for group_id in self.group_ids:
            # embedding is not supported for non group workspaces
            if group_id is not None:
                self._test_generate_report_token_impl(self.client, group_id)

    def _test_generate_report_token_impl(self, client, group_id):
        # get the current reports
        reports = client.reports.get_reports(group_id)

        # validate that we got reports
        self.assert_reports_valid(reports)
        self.assertGreater(len(reports), 0)
        self.assertEqual(len(reports), self.report_counts[group_id])

        # create the the token request with just a view access level
        token_request = TokenRequest('view')

        # get the token
        token = client.reports.generate_token(reports[0].id, token_request, group_id)

        # validate that we got a token back
        self.assertIsNotNone(token)
        self.assertIsNotNone(token.token)
        self.assertIsNotNone(token.token_id)
        self.assertIsNotNone(token.expiration)

    def test_upload_file(self):
        for group_id in self.group_ids:
            self._test_upload_file_impl(self.client, group_id)

    def _test_upload_file_impl(self, client, group_id):
        # upload the file, get back an import object
        import_object = client.imports.upload_file('test_report.pbix', 'test_report', None, group_id)
        self.assertIsNotNone(import_object)

        # ensure that there is at least one import
        imports = client.imports.get_imports(group_id)
        self.assertLess(0, len(imports))

        # search for our most recent import
        found = False
        for fetched_import in imports:
            self.assertIsNotNone(fetched_import)
            if fetched_import.id == import_object.id:
                found = True

        self.assertTrue(found)

        checks = 0
        while import_object.import_state != Import.import_state_succeeded and checks < 3:
            time.sleep(1)
            # get the import object again to check the import state
            import_object = client.imports.get_import(import_object.id, group_id)
            self.assertIsNotNone(import_object)
            checks = checks + 1

        self.assertEqual(1, len(import_object.datasets))
        self.assertEqual(1, len(import_object.reports))

        dataset = client.datasets.get_dataset(import_object.datasets[0].id, group_id)
        report = client.reports.get_report(import_object.reports[0].id, group_id)

        self.assertIsNotNone(dataset)
        self.assertIsNotNone(report)

        client.reports.delete_report(report.id, group_id)
        client.datasets.delete_dataset(dataset.id, group_id)

    def test_groups_count_method(self):
        group_count = self.client.groups.count()
        self.assertGreater(group_count, 0)

    def test_groups_has_group_method(self):
        for group_id in self.group_ids:
            self._test_groups_has_group_method(self.client, group_id)

    def _test_groups_has_group_method(self, client, group_id):
        self.assertTrue(client.groups.has_group(group_id))

    def test_groups_get_groups_method(self):
        groups = self.client.groups.get_groups()
        for group in groups:
            self.assertTrue(self.client.groups.has_group(group.id))
