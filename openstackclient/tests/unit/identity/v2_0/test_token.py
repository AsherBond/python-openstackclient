#   Copyright 2014 eBay Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

from openstackclient.identity.v2_0 import token
from openstackclient.tests.unit.identity.v2_0 import fakes as identity_fakes


class TestTokenIssue(identity_fakes.TestIdentityv2):
    def setUp(self):
        super().setUp()

        self.fake_user = identity_fakes.FakeUser.create_one_user()
        self.fake_project = identity_fakes.FakeProject.create_one_project()

        self.cmd = token.IssueToken(self.app, None)

    def test_token_issue(self):
        auth_ref = identity_fakes.fake_auth_ref(
            identity_fakes.TOKEN,
        )
        self.app.client_manager.auth_ref = auth_ref

        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # In base command class ShowOne in cliff, abstract method take_action()
        # returns a two-part tuple with a tuple of column names and a tuple of
        # data to be shown.
        columns, data = self.cmd.take_action(parsed_args)

        collist = ('expires', 'id', 'project_id', 'user_id')
        self.assertEqual(collist, columns)
        datalist = (
            identity_fakes.token_expires,
            identity_fakes.token_id,
            'project-id',
            'user-id',
        )
        self.assertEqual(datalist, data)

    def test_token_issue_with_unscoped_token(self):
        auth_ref = identity_fakes.fake_auth_ref(
            identity_fakes.UNSCOPED_TOKEN,
        )
        self.app.client_manager.auth_ref = auth_ref

        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        collist = (
            'expires',
            'id',
            'user_id',
        )
        self.assertEqual(collist, columns)
        datalist = (
            identity_fakes.token_expires,
            identity_fakes.token_id,
            'user-id',
        )
        self.assertEqual(datalist, data)


class TestTokenRevoke(identity_fakes.TestIdentityv2):
    TOKEN = 'fob'

    def setUp(self):
        super().setUp()
        self.tokens_mock = self.identity_client.tokens
        self.tokens_mock.reset_mock()
        self.tokens_mock.delete.return_value = True
        self.cmd = token.RevokeToken(self.app, None)

    def test_token_revoke(self):
        arglist = [self.TOKEN]
        verifylist = [('token', self.TOKEN)]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        result = self.cmd.take_action(parsed_args)

        self.tokens_mock.delete.assert_called_with(self.TOKEN)
        self.assertIsNone(result)
