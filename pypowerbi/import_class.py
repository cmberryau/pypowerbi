# -*- coding: future_fstrings -*-

import json

from .dataset import Dataset, DatasetEncoder
from .report import Report, ReportEncoder


class Import:
    # json keys
    id_key = 'id'
    name_key = 'name'
    created_timedate_key = 'createdDateTime'
    datasets_key = 'datasets'
    import_state_key = 'importState'
    reports_key = 'reports'
    updated_datetime_key = 'updatedDateTime'

    def __init__(self, import_id, name=None, created_datetime=None, datasets=None,
                 import_state=None, reports=None, updated_datetime=None):
        self.id = import_id
        self.name = name
        self.created_datetime = created_datetime
        self.datasets = datasets
        self.import_state = import_state
        self.reports = reports
        self.updated_datetime = updated_datetime

    @classmethod
    def from_dict(cls, dictionary):
        import_id = dictionary.get(cls.id_key)
        if import_id is None:
            raise RuntimeError("Import dictionary has no id key")

        name = dictionary.get(cls.name_key)
        created_datetime = dictionary.get(cls.created_timedate_key)

        if cls.datasets_key in dictionary:
            datasets = [Dataset.from_dict(x) for x in dictionary.get(cls.datasets_key)]
        else:
            datasets = None

        import_state = dictionary.get(cls.import_state_key)

        if cls.reports_key in dictionary:
            reports = [Report.from_dict(x) for x in dictionary.get(cls.reports_key)]
        else:
            reports = None

        updated_datetime = dictionary.get(cls.updated_datetime_key)

        return cls(import_id, name, created_datetime, datasets,
                   import_state, reports, updated_datetime)


class ImportEncoder(json.JSONEncoder):
    def default(self, o):
        json_dict = {
            Import.id_key: o.id,
        }

        if o.name is not None:
            json_dict[Import.name_key] = o.name

        if o.created_datetime is not None:
            json_dict[Import.created_timedate_key] = o.created_datetime

        if o.datasets is not None:
            encoder = DatasetEncoder()
            json_dict[Import.datasets_key] = [encoder.default(x) for x in o.datasets]

        if o.import_state is not None:
            json_dict[Import.import_state_key] = o.import_state

        if o.reports is not None:
            encoder = ReportEncoder()
            json_dict[Import.reports_key] = [encoder.default(x) for x in o.reports]

        if o.update_datetime is not None:
            json_dict[Import.updated_datetime_key] = o.update_datetime

        return json_dict


class ImportConflictHandlerMode:
    pass


class ImportInfo:
    # json keys
    connection_type_key = 'connectionType'
    filepath_key = 'filePath'
    fileurl_key = 'fileUrl'

    def __init__(self):
        pass
