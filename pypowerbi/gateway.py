# -*- coding: future_fstrings -*-
import json
from enum import Enum


class GatewayPublicKey:
    exponent_key = 'exponent'
    modulus_key = 'modulus'

    def __init__(self, exponent, modulus):
        """Constructs a GatewayPublicKey object

        :param exponent: str - the exponent of the public key
        :param modulus: str - the modulus of the public key
        """
        self.exponent = exponent
        self.modulus = modulus

    def as_dict(self):
        return {
            self.exponent_key: self.exponent,
            self.modulus_key: self.modulus
        }

    @classmethod
    def from_dict(cls, dictionary):
        """Constructs a GatewayPublicKey from a dictionary

        :param dictionary: the dictionary describing the GatewayPublicKey
        :return: GatewayPublicKey based on the dictionary
        :rtype: GatewayPublicKey
        """
        exponent = dictionary.get(cls.exponent_key)
        modulus = dictionary.get(cls.modulus_key)

        return cls(exponent, modulus)

    def __repr__(self):
        return f'<GatewayPublicKey exponent={self.exponent} modulus={self.modulus}>'


class Gateway:
    id_key = 'id'
    name_key = 'name'
    type_key = 'type'
    gateway_annotation_key = 'gatewayAnnotation'
    public_key_key = 'publicKey'
    status_key = 'gatewayStatus'

    def __init__(self, gateway_id, name, gateway_type, gateway_annotation, public_key, status):
        """Constructs a Gateway object

        :param gateway_id: str - The gateway id
        :param name: str - The gateway name
        :param gateway_type: str - The gateway type
        :param gateway_annotation: str - Gateway metadata in json format
        :param public_key: GatewayPublicKey - The gateway public key
        :param status: str - The gateway connectivity status
        """
        self.id = gateway_id
        self.name = name
        self.type = gateway_type
        self.gateway_annotation = gateway_annotation
        self.public_key = public_key
        self.status = status

    @classmethod
    def from_dict(cls, dictionary):
        """Constructs a Gateway object from a dict

        :param dictionary: Dictionary describing the gateway
        :return: Gateway based on the dictionary
        :rtype: Gateway
        """
        gateway_id = dictionary.get(cls.id_key)
        if gateway_id is None:
            raise RuntimeError("Gateway dictionary has no id key")

        name = dictionary.get(cls.name_key)
        gateway_type = dictionary.get(cls.type_key)
        gateway_annotation = dictionary.get(cls.gateway_annotation_key)
        public_key = GatewayPublicKey.from_dict(dictionary.get(cls.public_key_key))
        status = dictionary.get(cls.status_key)

        return cls(gateway_id, name, gateway_type, gateway_annotation, public_key, status)

    def __repr__(self):
        return f'<Gateway id={self.id} name={self.name}>'


class CredentialType(Enum):
    ANONYMOUS = 'Anonymous'
    BASIC = 'Basic'
    KEY = 'Key'
    OAUTH2 = 'OAuth2'
    WINDOWS = 'Windows'


class GatewayDatasource:
    gateway_datasource_id_key = 'id'
    gateway_id_key = 'gatewayId'
    credential_type_key = 'credentialType'
    datasource_name_key = 'datasourceName'
    datasource_type_key = 'datasourceType'
    connection_details_key = 'connectionDetails'

    def __init__(
        self,
        gateway_datasource_id,
        gateway_id,
        credential_type,
        datasource_name,
        datasource_type,
        connection_details
    ):
        """Constructs a GatewayDatasource object

        :param gateway_datasource_id: str - The unique id for this datasource
        :param gateway_id: str - The associated gateway id
        :param credential_type: CredentialType - Type of datasource credentials
        :param datasource_name: str - The name of the datasource
        :param datasource_type: str - The type of the datasource
        :param connection_details: str - Connection details in json format
        """
        self.id = gateway_datasource_id
        self.gateway_id = gateway_id
        self.credential_type = credential_type
        self.datasource_name = datasource_name
        self.datasource_type = datasource_type
        self.connection_details = connection_details

    @classmethod
    def from_dict(cls, dictionary):
        """Constructs a GatewayDatasource object from a dict

        :param dictionary: Dictionary describing the gatewayDatasource
        :return: GatewayDatasource based on the dictionary
        :rtype: GatewayDatasource
        """
        gateway_datasource_id = dictionary.get(cls.gateway_datasource_id_key)
        if gateway_datasource_id is None:
            raise RuntimeError("GatewayDatasource dictionary has no id key")

        gateway_id = dictionary.get(cls.gateway_id_key)
        # use round brackets below to access enum by value
        credential_type = CredentialType(dictionary.get(cls.credential_type_key))
        datasource_name = dictionary.get(cls.datasource_name_key)
        datasource_type = dictionary.get(cls.datasource_type_key)
        connection_details = json.dumps(dictionary.get(cls.connection_details_key))

        return cls(
            gateway_datasource_id,
            gateway_id,
            credential_type,
            datasource_name,
            datasource_type,
            connection_details
        )