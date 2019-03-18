# -*- coding: future_fstrings -*-

import json


class Report:
    id_key = 'id'
    name_key = 'name'
    web_url_key = 'webUrl'
    embed_url_key = 'embedUrl'
    dataset_id_key = 'datasetId'
    target_workspace_id_key = 'targetWorkspaceId'
    target_model_id_key = 'targetModelId'

    def __init__(self, report_id, name, web_url, embed_url, dataset_id):
        self.id = report_id
        self.name = name
        self.web_url = web_url
        self.embed_url = embed_url
        self.dataset_id = dataset_id

    @classmethod
    def from_dict(cls, dictionary):
        """
        Creates a report from a dictionary
        :param dictionary: The dictionary to create a report from
        :return: The created dictionary
        """
        # id is required
        if cls.id_key in dictionary:
            report_id = str(dictionary[cls.id_key])
            # id cannot be whitespace
            if report_id.isspace():
                raise RuntimeError(f'Report dict has empty {cls.id_key} key value')
        else:
            raise RuntimeError(f'Report dict has no {cls.id_key} key')

        # name is required
        if cls.name_key in dictionary:
            report_name = str(dictionary[cls.name_key])
            # name cannot be whitespace
            if report_name.isspace():
                raise RuntimeError(f'Report dict has empty {cls.name_key} key value')
        else:
            raise RuntimeError(f'Report dict has no {cls.name_key} key')

        # web url is optional
        if cls.web_url_key in dictionary:
            web_url = str(dictionary[cls.web_url_key])
        else:
            web_url = None

        # embed url is optional
        if cls.embed_url_key in dictionary:
            embed_url = str(dictionary[cls.embed_url_key])
        else:
            embed_url = None

        # dataset id is optional
        dataset_id = dictionary.get(cls.dataset_id_key)

        return Report(report_id, report_name, web_url, embed_url, dataset_id)

    def __repr__(self):
        return f'<Report {str(self.__dict__)}>'


class ReportEncoder(json.JSONEncoder):
    def default(self, o):
        return {
            Report.id_key: o.id,
            Report.name_key: o.name,
            Report.web_url_key: o.web_url,
            Report.embed_url_key: o.embed_url,
            Report.dataset_id_key: o.dataset_id
        }
