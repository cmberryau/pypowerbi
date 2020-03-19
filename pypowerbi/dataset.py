# -*- coding: future_fstrings -*-
import json


class Dataset:
    # json keys
    id_key = 'id'
    name_key = 'name'
    add_rows_api_enabled_key = 'addRowsAPIEnabled'
    configured_by_key = 'configuredBy'
    is_refreshable_key = 'isRefreshable'
    is_effective_identity_required_key = 'isEffectiveIdentityRequired'
    is_effective_identity_roles_required_key = 'isEffectiveIdentityRolesRequired'
    is_on_prem_gateway_required_key = 'isOnPremGatewayRequired'
    tables_key = 'tables'

    def __init__(self, name, dataset_id=None, tables=None, add_rows_api_enabled=None,
                 configured_by=None, is_refreshable=None, is_effective_identity_required=None,
                 is_effective_identity_roles_required=None, is_on_prem_gateway_required=None):
        self.name = name
        self.id = dataset_id
        self.tables = tables
        self.add_rows_api_enabled = add_rows_api_enabled
        self.configured_by = configured_by
        self.is_refreshable = is_refreshable
        self.is_effective_identity_required = is_effective_identity_required
        self.is_effective_identity_roles_required = is_effective_identity_roles_required
        self.is_on_prem_gateway_required = is_on_prem_gateway_required

    @classmethod
    def from_dict(cls, dictionary):
        """
        Creates a dataset from a dictionary, key values for 'id' and 'name' required
        :param dictionary: The dictionary to create the dataset from
        :return: A dataset created from the given dictionary
        """
        # id is required
        if Dataset.id_key in dictionary:
            dataset_id = str(dictionary[Dataset.id_key])
            # id cannot be whitespace
            if dataset_id.isspace():
                raise RuntimeError('Dataset dict has empty id key value')
        else:
            raise RuntimeError('Dataset dict has no id key')
        # name is required
        if Dataset.name_key in dictionary:
            dataset_name = str(dictionary[Dataset.name_key])
            # name cannot be whitespace
            if dataset_id.isspace():
                raise RuntimeError('Dataset dict has empty name key value')
        else:
            raise RuntimeError('Dataset dict has no name key')

        # add api enabled is optional
        if Dataset.add_rows_api_enabled_key in dictionary:
            add_rows_api_enabled = bool(dictionary[Dataset.add_rows_api_enabled_key])
        else:
            add_rows_api_enabled = None

        # configured by is optional
        if Dataset.configured_by_key in dictionary:
            configured_by = str(dictionary[Dataset.configured_by_key])
        else:
            configured_by = None

        # is refreshable is optional
        if Dataset.is_refreshable_key in dictionary:
            is_refreshable = bool(dictionary[Dataset.is_refreshable_key])
        else:
            is_refreshable = None

        # is effective identity required is optional
        if Dataset.is_effective_identity_required_key in dictionary:
            is_effective_identity_required = bool(dictionary[Dataset.is_effective_identity_required_key])
        else:
            is_effective_identity_required = None

        # is effective identity roles required is optional
        if Dataset.is_effective_identity_roles_required_key in dictionary:
            is_effective_identity_roles_required = bool(dictionary[Dataset.is_effective_identity_roles_required_key])
        else:
            is_effective_identity_roles_required = None

        # is on prem gateway required is optional
        if Dataset.is_on_prem_gateway_required_key in dictionary:
            is_on_prem_gateway_required = bool(dictionary[Dataset.is_on_prem_gateway_required_key])
        else:
            is_on_prem_gateway_required = None

        return Dataset(dataset_name, dataset_id, add_rows_api_enabled=add_rows_api_enabled,
                       configured_by=configured_by, is_refreshable=is_refreshable,
                       is_effective_identity_required=is_effective_identity_required,
                       is_effective_identity_roles_required=is_effective_identity_roles_required,
                       is_on_prem_gateway_required=is_on_prem_gateway_required)

    def __repr__(self):
        return f'<Dataset {str(self.__dict__)}>'


class DatasetEncoder(json.JSONEncoder):
    def default(self, o):
        table_encoder = TableEncoder()

        json_dict = {
            Dataset.name_key: o.name,
            Dataset.tables_key: [table_encoder.default(x) for x in o.tables],
        }

        return json_dict


class Table:
    name_key = 'name'
    columns_key = 'columns'
    measures_key = 'measures'

    @classmethod
    def from_dict(cls, dictionary):
        """
        Creates a table from a dictionary, 'name' key value required
        :param dictionary: The dictionary to create the table from
        :return: A table created from the dictionary
        """
        # name is required
        if Table.name_key in dictionary:
            table_name = str(dictionary[Table.name_key])
            # name cannot be whitespace
            if table_name.isspace():
                raise RuntimeError('Table dict has empty name key value')
        else:
            raise RuntimeError('Table dict has no name key')

        # measures are optional
        if Table.measures_key in dictionary:
            table_measures = [Table.from_dict(x) for x in dictionary[Table.measures_key]]
        else:
            table_measures = None

        return Table(name=table_name, measures=table_measures)

    def __init__(self, name, columns=None, measures=None):
        self.name = name
        self.columns = columns
        self.measures = measures

    def __repr__(self):
        return f'<Table {str(self.__dict__)}>'


class TableEncoder(json.JSONEncoder):
    def default(self, o):
        json_dict = {
            Table.name_key: o.name,
        }

        if o.columns is not None:
            column_encoder = ColumnEncoder()
            json_dict[Table.columns_key] = [column_encoder.default(x) for x in o.columns]

        if o.measures is not None:
            measure_encoder = MeasureEncoder()
            json_dict[Table.measures_key] = [measure_encoder.default(x) for x in o.measures]

        return json_dict


class Measure:
    name_key = 'name'
    expression_key = 'expression'
    formatstring_key = 'formatString'
    is_hidden_key = 'isHidden'

    @classmethod
    def from_dict(cls, dictionary):
        # name is required
        if Measure.name_key in dictionary:
            measure_name = str(dictionary[Measure.name_key])
            # name cannot be whitespace
            if measure_name.isspace():
                raise RuntimeError('Measure dict has empty name key value')
        else:
            raise RuntimeError('Measure dict has no name key')

        # expression is required
        if Measure.expression_key in dictionary:
            measure_expression = str(dictionary[Measure.expression_key])
            # expression cannot be whitespace
            if measure_expression.isspace():
                raise RuntimeError('Measure dict has empty expression key value')
        else:
            raise RuntimeError('Measure dict has no expression key')

        if Measure.formatstring_key in dictionary:
            measure_formatstring = str(dictionary[Measure.formatstring_key])
        else:
            measure_formatstring = None

        if Measure.is_hidden_key in dictionary:
            measure_is_hidden = bool(dictionary[Measure.is_hidden_key])
        else:
            measure_is_hidden = None

        return Measure(name=measure_name, expression=measure_expression, formatstring=measure_formatstring,
                       is_hidden=measure_is_hidden)

    def __init__(self, name, expression, formatstring=None, is_hidden=None):
        self.name = name
        self.expression = expression
        self.formatstring = formatstring
        self.is_hidden = is_hidden

    def __repr__(self):
        return f'<Measure {str(self.__dict__)}>'


class MeasureEncoder(json.JSONEncoder):
    def default(self, o):
        json_dict = {
            Measure.name_key: o.name,
            Measure.expression_key: o.expression,
        }

        if o.formatstring is not None:
            json_dict[Measure.formatstring_key] = o.formatstring

        if o.is_hidden is not None:
            json_dict[Measure.is_hidden_key] = o.is_hidden

        return json_dict


class Column:
    name_key = 'name'
    datatype_key = 'dataType'
    formatstring_key = 'formatString'

    def __init__(self, name, data_type, formatstring=None):
        self.name = name
        self.data_type = data_type
        self.formatstring = formatstring

    def __repr__(self):
        return f'<Column {str(self.__dict__)}>'


class ColumnEncoder(json.JSONEncoder):
    def default(self, o):
        json_dict = {
            Column.name_key: o.name,
            Column.datatype_key: o.data_type
        }

        if o.formatstring is not None:
            json_dict[Column.formatstring_key] = o.formatstring

        return json_dict


class Row:
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return f'<Row {str(self.__dict__)}>'


class RowEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
