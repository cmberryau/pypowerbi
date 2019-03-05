import datetime

# Datetime's come in from PowerBI in the format 2019-03-05T03:09:31.493Z
_date_fmt_str = '%Y-%m-%dT%H:%M:%S.%fZ'


def date_from_powerbi_str(dstr):
    return datetime.datetime.strptime(dstr, _date_fmt_str)


def convert_datetime_fields(list_of_dicts, fields_to_convert):
    for rec in list_of_dicts:
        for field in fields_to_convert:
            if field in rec.keys() and rec[field] not in [None, '']:
                rec[field] = date_from_powerbi_str(rec[field])

    return list_of_dicts
