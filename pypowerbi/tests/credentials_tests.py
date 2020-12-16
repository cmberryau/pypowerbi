from unittest import TestCase

from pypowerbi import CredentialType
from pypowerbi.credentials import AnonymousCredentials, BasicCredentials, KeyCredentials, OAuth2Credentials, \
    WindowsCredentials


# The following tests are based on the examples found here:
# https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/updatedatasource#examples
class CredentialsTestCase(TestCase):
    def test_anonymous_credentials(self):
        anonymous_credentials = AnonymousCredentials()

        expected = r'{"credentialData":""}'
        actual = anonymous_credentials.to_json()

        self.assertEqual(expected, actual)
        self.assertEqual(
            CredentialType.ANONYMOUS,
            anonymous_credentials.CREDENTIAL_TYPE
        )

    def test_basic_credentials(self):
        basic_credentials = BasicCredentials("john", "*****")

        expected = r'{"credentialData":[{"name":"username","value":"john"},{"name":"password","value":"*****"}]}'
        actual = basic_credentials.to_json()

        with self.assertRaises(ValueError):
            # empty username
            BasicCredentials("", "myPassword")

        with self.assertRaises(ValueError):
            # empty password
            BasicCredentials("myUsername", "")

        self.assertEqual(expected, actual)
        self.assertEqual(
            CredentialType.BASIC,
            basic_credentials.CREDENTIAL_TYPE
        )

    def test_key_credentials(self):
        key_credentials = KeyCredentials("ec....LA=")

        expected = r'{"credentialData":[{"name":"key","value":"ec....LA="}]}'
        actual = key_credentials.to_json()

        with self.assertRaises(ValueError):
            # empty key
            KeyCredentials("")

        self.assertEqual(expected, actual)

        self.assertEqual(
            CredentialType.KEY,
            key_credentials.CREDENTIAL_TYPE
        )

    def test_o_auth_2_credentials(self):
        o_auth_2_credentials = OAuth2Credentials("eyJ0....fwtQ")

        expected = r'{"credentialData":[{"name":"accessToken","value":"eyJ0....fwtQ"}]}'
        actual = o_auth_2_credentials.to_json()

        with self.assertRaises(ValueError):
            # empty access token
            OAuth2Credentials("")

        self.assertEqual(expected, actual)

        self.assertEqual(
            CredentialType.OAUTH2,
            o_auth_2_credentials.CREDENTIAL_TYPE
        )

    def test_windows_credentials(self):
        windows_credentials = WindowsCredentials(r'contoso\\john', "*****")

        expected = r'{"credentialData":[{"name":"username","value":"contoso\\john"},' \
                   r'{"name":"password","value":"*****"}]}'
        actual = windows_credentials.to_json()

        with self.assertRaises(ValueError):
            # empty username
            WindowsCredentials("", "myPassword")

        with self.assertRaises(ValueError):
            # empty password
            WindowsCredentials("myUsername", "")

        self.assertEqual(expected, actual)
        self.assertEqual(
            CredentialType.WINDOWS,
            windows_credentials.CREDENTIAL_TYPE
        )
