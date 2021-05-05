# -*- coding: future_fstrings -*-

from enum import Enum


class GroupUserAccessRight(Enum):
    NONE = 'None'
    MEMBER = 'Member'
    ADMIN = 'Admin'
    CONTRIBUTOR = 'Contributor'
    VIEWER = 'Viewer'


class PrincipalType(Enum):
    USER = "User"
    GROUP = "Group"
    APP = "App"


class DatasourceUserAccessRight(Enum):
    # Removes permission to access the datasource
    NONE = 'None'
    # Datasets owned by the user have read access to this datasource
    READ = 'Read'
    # The user can override the effective identity for PowerBI Embedded
    READ_OVERRIDE_EFFECTIVE_IDENTITY = 'ReadOverrideEffectiveIdentity'


class CredentialType(Enum):
    ANONYMOUS = 'Anonymous'
    BASIC = 'Basic'
    KEY = 'Key'
    OAUTH2 = 'OAuth2'
    WINDOWS = 'Windows'


class EncryptedConnection(Enum):
    ENCRYPTED = 'Encrypted'
    NOT_ENCRYPTED = 'NotEncrypted'


class EncryptionAlgorithm(Enum):
    NONE = 'None'
    RSA_OAEP = 'RSA-OAEP'


class PrivacyLevel(Enum):
    NONE = 'None'
    PUBLIC = 'Public'
    ORGANIZATIONAL = 'Organizational'
    PRIVATE = 'Private'
