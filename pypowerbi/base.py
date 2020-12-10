import abc
from typing import Dict, Union


class Deserializable(metaclass=abc.ABCMeta):
    """Interface to ensure operations modules need fewer methods to turn responses into objects"""
    @classmethod
    @abc.abstractmethod
    def from_dict(cls, dictionary: Dict[str, Union[str, Dict[str, str]]]):
        pass
