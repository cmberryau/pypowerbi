from typing import Optional, Dict, List, Union
import json

from pypowerbi import CredentialType


class CredentialsBase:
    CREDENTIAL_TYPE: Optional[CredentialType] = None
    credential_data_key = "credentialData"

    def __init__(self):
        self.credential_data: Dict[str, Union[str, List[Dict[str, str]]]] = {
            self.credential_data_key: []
        }

    def add_credential_data(self, key, value):
        self.credential_data[self.credential_data_key].append(
            {"name": key, "value": value}
        )

    def to_json(self) -> str:
        return json.dumps(self.credential_data, separators=(',', ':'))\
            .replace('\\\\', '\\')


class UsernamePasswordCredentials(CredentialsBase):
    username_key = "username"
    password_key = "password"

    def __init__(self, username: str, password: str):
        super().__init__()

        if not username:
            raise ValueError("An empty string is not a valid username!")
        if not password:
            raise ValueError("An empty string is not a valid password!")

        self.username = username
        self.password = password

        super().add_credential_data(self.username_key, username)
        super().add_credential_data(self.password_key, password)


class AnonymousCredentials(CredentialsBase):
    CREDENTIAL_TYPE = CredentialType.ANONYMOUS

    def __init__(self):
        super().__init__()
        self.credential_data[self.credential_data_key] = ""

    def __repr__(self) -> str:
        return f'<AnonymousCredentials>'


class BasicCredentials(UsernamePasswordCredentials):
    CREDENTIAL_TYPE = CredentialType.BASIC

    def __init__(self, username: str, password: str):
        super().__init__(username, password)

    def __repr__(self) -> str:
        return f'<BasicCredentials username={self.username}>'


class KeyCredentials(CredentialsBase):
    CREDENTIAL_TYPE = CredentialType.KEY
    key_key = "key"

    def __init__(self, key: str):
        super().__init__()

        if not key:
            raise ValueError("An empty string is not a valid key!")

        self.key = key

        super().add_credential_data(self.key_key, key)

    def __repr__(self) -> str:
        return f'<KeyCredentials>'


class OAuth2Credentials(CredentialsBase):
    CREDENTIAL_TYPE = CredentialType.OAUTH2
    access_token_key = "accessToken"

    def __init__(self, access_token: str):
        super().__init__()

        if not access_token:
            raise ValueError("An empty string is not a valid access token!")

        super().add_credential_data(self.access_token_key, access_token)

    def __repr__(self) -> str:
        return f'<OAuth2Credentials>'


class WindowsCredentials(UsernamePasswordCredentials):
    CREDENTIAL_TYPE = CredentialType.WINDOWS

    def __init__(self, username: str, password: str):
        super().__init__(username, password)

    def __repr__(self):
        return f'<WindowsCredentials username={self.username}>'
