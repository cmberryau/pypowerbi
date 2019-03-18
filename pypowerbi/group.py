# -*- coding: future_fstrings -*-
import json


class Group:
    id_key = 'id'
    name_key = 'name'
    is_readonly_key = 'isReadOnly'
    is_on_dedicated_capacity_key = 'isOnDedicatedCapacity'

    def __init__(self, name, group_id, is_readonly=False, is_on_dedicated_capacity=False):
        self.name = name
        self.id = group_id
        self.is_readonly = is_readonly
        self.is_on_dedicated_capacity = is_on_dedicated_capacity

    @classmethod
    def from_dict(cls, dictionary):
        group_id = dictionary.get(cls.id_key)
        if group_id is None:
            raise RuntimeError("Group dictionary has no id key")

        name = dictionary.get(cls.name_key)
        is_readonly = dictionary.get(cls.is_readonly_key, False)
        is_on_dedicated_capacity = dictionary.get(cls.is_on_dedicated_capacity_key, False)

        return cls(name, group_id, is_readonly, is_on_dedicated_capacity)

    def __repr__(self):
        return f'<Group {str(self.__dict__)}>'
