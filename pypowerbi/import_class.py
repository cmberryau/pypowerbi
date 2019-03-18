# -*- coding: future_fstrings -*-

from .dataset import Dataset
from .report import Report


class Import:
    # json keys
    id_key = 'id'
    name_key = 'name'
    created_timedate_key = 'createdDateTime'
    datasets_key = 'datasets'
    import_state_key = 'importState'
    reports_key = 'reports'
    updated_datetime_key = 'updatedDateTime'
    source_key = 'source'
    connection_type_key = 'connectionType'
    value_key = 'value'

    # import state values
    import_state_succeeded = 'Succeeded'
    import_state_publishing = 'Publishing'

    def __init__(self, import_id, name=None, created_datetime=None, datasets=None, import_state=None,
                 reports=None, updated_datetime=None, source=None, connection_type=None):
        self.id = import_id
        self.name = name
        self.created_datetime = created_datetime
        self.datasets = datasets
        self.import_state = import_state
        self.reports = reports
        self.updated_datetime = updated_datetime
        self.source = source
        self.connection_type = connection_type

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
        source = dictionary.get(cls.source_key)
        connection_type = dictionary.get(cls.connection_type_key)

        return cls(import_id, name, created_datetime, datasets, import_state,
                   reports, updated_datetime, source, connection_type)

    def __repr__(self):
        return f'<Import {str(self.__dict__)}>'
