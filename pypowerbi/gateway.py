# -*- coding: future_fstrings -*-
import json
from typing import Dict, Union, Optional

from .base import Deserializable
from .enums import CredentialType, DatasourceUserAccessRight, PrincipalType, EncryptedConnection, EncryptionAlgorithm, \
    PrivacyLevel


class GatewayPublicKey(Deserializable):
    exponent_key = 'exponent'
    modulus_key = 'modulus'

    def __init__(
            self,
            exponent: str,
            modulus: str
    ):
        """Constructs a GatewayPublicKey object

        :param exponent: The exponent of the public key
        :param modulus: The modulus of the public key
        """
        self.exponent = exponent
        self.modulus = modulus

    def as_dict(self) -> Dict[str, str]:
        return {
            self.exponent_key: self.exponent,
            self.modulus_key: self.modulus
        }

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> 'GatewayPublicKey':
        """Constructs a GatewayPublicKey from a dictionary

        :param dictionary: the dictionary describing the GatewayPublicKey
        :return: GatewayPublicKey based on the dictionary
        :rtype: GatewayPublicKey
        """
        exponent = dictionary.get(cls.exponent_key)
        modulus = dictionary.get(cls.modulus_key)

        return cls(exponent, modulus)

    def __repr__(self) -> str:
        return f'<GatewayPublicKey exponent={self.exponent} modulus={self.modulus}>'


class Gateway(Deserializable):
    id_key = 'id'
    name_key = 'name'
    type_key = 'type'
    gateway_annotation_key = 'gatewayAnnotation'
    public_key_key = 'publicKey'
    status_key = 'gatewayStatus'

    def __init__(
            self,
            gateway_id: str,
            name: str,
            gateway_type: str,
            gateway_annotation: str,
            public_key: GatewayPublicKey,
            status: str
    ):
        """Constructs a Gateway object

        :param gateway_id: The gateway id
        :param name: The gateway name
        :param gateway_type: The gateway type
        :param gateway_annotation: Gateway metadata in json format
        :param public_key: The gateway public key
        :param status: The gateway connectivity status
        """
        self.id = gateway_id
        self.name = name
        self.type = gateway_type
        self.gateway_annotation = gateway_annotation
        self.public_key = public_key
        self.status = status

    @classmethod
    def from_dict(cls, dictionary: Dict[str, Union[str, Dict[str, str]]]) -> 'Gateway':
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

    def __repr__(self) -> str:
        return f'<Gateway id={self.id} name={self.name}>'


class GatewayDatasource(Deserializable):
    gateway_datasource_id_key = 'id'
    gateway_id_key = 'gatewayId'
    credential_type_key = 'credentialType'
    datasource_name_key = 'datasourceName'
    datasource_type_key = 'datasourceType'
    connection_details_key = 'connectionDetails'

    def __init__(
            self,
            gateway_datasource_id: str,
            gateway_id: str,
            credential_type: CredentialType,
            datasource_name: str,
            datasource_type: str,
            connection_details: str
    ):
        """Constructs a GatewayDatasource object

        :param gateway_datasource_id: The unique id for this datasource
        :param gateway_id: The associated gateway id
        :param credential_type: Type of datasource credentials
        :param datasource_name: The name of the datasource
        :param datasource_type: The type of the datasource
        :param connection_details: Connection details in json format
        """
        self.id = gateway_datasource_id
        self.gateway_id = gateway_id
        self.credential_type = credential_type
        self.datasource_name = datasource_name
        self.datasource_type = datasource_type
        self.connection_details = connection_details

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> 'GatewayDatasource':
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

    def __repr__(self):
        return f'<GatewayDatasource id={self.id} name={self.datasource_name} type={self.datasource_type}>'


class DatasourceUser(Deserializable):
    datasource_access_right_key = 'datasourceAccessRight'
    email_address_key = 'emailAddress'
    display_name_key = 'displayName'
    identifier_key = 'identifier'
    principal_type_key = 'principalType'

    def __init__(
        self,
        datasource_access_right: DatasourceUserAccessRight,
        email_address: str = "",
        display_name: str = "",
        identifier: str = "",
        principal_type: Optional[PrincipalType] = None
    ):
        """Constructs a DataSourceUser object

        :param datasource_access_right: The user access rights for the datasource
        :param email_address: Email address of the user
        :param display_name: Display name of the principal
        :param identifier: Identifier of the principal
        :param principal_type: The principal type
        """
        self.datasource_access_right = datasource_access_right
        self.email_address = email_address
        self.display_name = display_name
        self.identifier = identifier
        self.principal_type = principal_type

    @classmethod
    def from_dict(cls, dictionary: Dict[str, str]) -> 'DatasourceUser':
        datasource_user_id = dictionary.get(cls.identifier_key)
        if datasource_user_id is None:
            raise RuntimeError("DatasourceUser dictionary has no identifier key")

        datasource_user_access_right = DatasourceUserAccessRight(dictionary.get(cls.datasource_access_right_key))
        email_address = dictionary.get(cls.email_address_key, "")
        display_name = dictionary.get(cls.display_name_key, "")
        principal_type_value = dictionary.get(cls.principal_type_key, None)
        principal_type = PrincipalType(principal_type_value) if principal_type_value is not None \
            else principal_type_value

        return cls(datasource_user_access_right, email_address, display_name, datasource_user_id, principal_type)

    def as_set_values_dict(self) -> Dict[str, str]:
        set_values_dict = dict()

        set_values_dict[self.datasource_access_right_key] = self.datasource_access_right.value

        if self.email_address:
            set_values_dict[self.email_address_key] = self.email_address

        if self.display_name:
            set_values_dict[self.display_name_key] = self.display_name

        if self.identifier:
            set_values_dict[self.identifier_key] = self.identifier

        if self.principal_type:
            set_values_dict[self.principal_type_key] = self.principal_type.value

        return set_values_dict

    def __repr__(self) -> str:
        return f'<DatasourceUser id={self.identifier} type={self.principal_type.name} display_name={self.display_name}>'


class DatasourceConnectionDetails:
    server_key = "server"
    database_key = "database"
    url_key = "url"

    def __init__(
        self,
        server: str = "",
        database: str = "",
        url: str = ""
    ):
        """Creates a DatasourceConnectionDetails object

        :param server: The connection server
        :param database: The connection database
        :param url: The connection url
        """
        self.server = server
        self.database = database
        self.url = url

    def __repr__(self):
        server_part = f'server={self.server}' if self.server else self.server
        database_part = f'database={self.database}' if self.database else self.database
        url_part = f'url={self.url}' if self.url else self.url

        return f'<DatasourceConnectionDetails {server_part} {database_part} {url_part}>'

    def as_set_values_dict(self) -> Dict[str, str]:
        """Returns a dictionary with only those values of attributes that are set

        :return: Dictionary with set values
        """
        set_values = dict()

        if self.server:
            set_values[self.server_key] = self.server

        if self.database:
            set_values[self.database_key] = self.database

        if self.url:
            set_values[self.url_key] = self.url

        return set_values

    def to_json(self) -> str:
        """Provides a json string that can be used in a PublishDatasourceToGatewayRequest

        :return: json string of set values
        """
        json_dict = self.as_set_values_dict()

        # dump to json string
        # remove spaces between object keys and values
        # replace double backslashes with single slashes
        # remove double quotes at start and end of str
        return json.dumps(json_dict) \
            .replace(r'": ', r'":') \
            .replace('\\\\', '\\')


class CredentialDetails:
    credentials_key = "credentials"
    credential_type_key = "credentialType"
    encrypted_connection_key = "encryptedConnection"
    encryption_algorithm_key = "encryptionAlgorithm"
    privacy_level_key = "privacyLevel"
    use_caller_aad_identity_key = "useCallerAADIdentity"
    use_end_user_o_auth_2_credentials_key = "useEndUserOAuth2Credentials"

    def __init__(
        self,
        credentials: str,
        credential_type: CredentialType,
        encrypted_connection: EncryptedConnection,
        encryption_algorithm: EncryptionAlgorithm,
        privacy_level: PrivacyLevel,
        use_caller_aad_identity: Optional[bool] = None,
        use_end_user_o_auth_2_credentials: Optional[bool] = None
    ):
        """Constructs a CredentialsDetails object

        :param credentials: The credentials to access a datasource
        :param credential_type: The type of credentials to access a datasource
        :param encrypted_connection: Encryption behaviour applied to the datasource connection
        :param encryption_algorithm: The encryption algorithm. For cloud datasource, use 'None'. For an on-premises
         datasource, use the gateway public key with the 'RSA-OAEP' algorithm.
        :param privacy_level: The privacy level. This becomes relevant when combining data from multiple datasources.
        :param use_caller_aad_identity: Should the caller's AAD identity be used for OAuth2 credentials configuration
        :param use_end_user_o_auth_2_credentials: Should the end-user's OAuth2 credentials be used for connecting to
         the datasource in DirectQuery mode. Only supported for Direct Query to SQL Azure.
        """
        self.credentials = credentials
        self.credential_type = credential_type
        self.encrypted_connection = encrypted_connection
        self.encryption_algorithm = encryption_algorithm
        self.privacy_level = privacy_level
        self.use_caller_aad_identity = use_caller_aad_identity
        self.use_end_user_o_auth_2_credentials = use_end_user_o_auth_2_credentials

    def to_dict(self):
        return {
            self.credentials_key: self.credentials,
            self.credential_type_key: self.credential_type.value,
            self.encrypted_connection_key: self.encrypted_connection.value,
            self.encryption_algorithm_key: self.encryption_algorithm.value,
            self.privacy_level_key: self.privacy_level.value,
            self.use_caller_aad_identity_key: self.use_caller_aad_identity,
            self.use_end_user_o_auth_2_credentials_key: self.use_end_user_o_auth_2_credentials
        }

    def __repr__(self) -> str:
        return f"<CredentialDetails type={self.credential_type.value}>"


class PublishDatasourceToGatewayRequest:
    datasource_type_key = "dataSourceType"
    connection_details_key = "connectionDetails"
    credential_details_key = "credentialDetails"
    datasource_name_key = "datasourceName"

    def __init__(
        self,
        datasource_type: str,
        connection_details: str,
        credential_details: CredentialDetails,
        datasource_name: str
    ):
        """Constructs a PublishDatasourceToGatewayRequest

        :param datasource_type: The datasource type
        :param connection_details: The connection details
        :param credential_details: The credentials to access the datasource
        :param datasource_name: The datasource name
        """
        self.datasource_type = datasource_type
        self.connection_details = connection_details
        self.credential_details = credential_details
        self.datasource_name = datasource_name

    def to_dict(self) -> Dict[str, Union[str, Dict[str, str]]]:
        return {
            self.datasource_type_key: self.datasource_type,
            self.connection_details_key: self.connection_details,
            self.credential_details_key: self.credential_details.to_dict(),
            self.datasource_name_key: self.datasource_name
        }

    def __repr__(self):
        return '<PublishDatasourceToGatewayRequest ' \
               f'name={self.datasource_name} ' \
               f'type={self.datasource_type}>'
