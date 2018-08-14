# -*- coding: future_fstrings -*-

import json
from unittest import TestCase

from pypowerbi.client import *


class PowerBIClientJSONTests(TestCase):
    def test_effective_identity_json(self):
        roles = ['role0', 'role1']
        datasets = ['jsdbfj783uisdkjfjkdsf', '8923u4ihjknkjnfdsk']
        effective_identity = EffectiveIdentity('yabbadabba', roles, datasets)

        effective_identity_json = json.dumps(effective_identity, cls=EffectiveIdentityEncoder)
        self.assertIsNotNone(effective_identity_json)

        expected_json = '{"username": "yabbadabba", "roles": ["role0", "role1"], "datasets": ["jsdbfj783uisdkjfjkdsf", "8923u4ihjknkjnfdsk"]}'

        self.assertEqual(expected_json, effective_identity_json)

    def test_token_request_json(self):
        roles = ['role0', 'role1']
        datasets = ['jsdbfj783uisdkjfjkdsf', '8923u4ihjknkjnfdsk']
        effective_identity = EffectiveIdentity('yabbadabba', roles, datasets)

        token_request = TokenRequest('view', '8324yihuknjsdf09io2k', True, [effective_identity])

        token_request_json = json.dumps(token_request, cls=TokenRequestEncoder)
        self.assertIsNotNone(token_request_json)

        expected_json = '{"accessLevel": "view", "datasetId": "8324yihuknjsdf09io2k", "allowSaveAs": true, "identities": [{"username": "yabbadabba", "roles": ["role0", "role1"], "datasets": ["jsdbfj783uisdkjfjkdsf", "8923u4ihjknkjnfdsk"]}]}'

        self.assertEqual(expected_json, token_request_json)
