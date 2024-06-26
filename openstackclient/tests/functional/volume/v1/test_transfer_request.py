#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import uuid

from openstackclient.tests.functional.volume.v1 import common


class TransferRequestTests(common.BaseVolumeTests):
    """Functional tests for transfer request."""

    NAME = uuid.uuid4().hex
    VOLUME_NAME = uuid.uuid4().hex

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cmd_output = cls.openstack(
            'volume create --size 1 ' + cls.VOLUME_NAME,
            parse_output=True,
        )
        cls.assertOutput(cls.VOLUME_NAME, cmd_output['name'])

        cls.wait_for_status("volume", cls.VOLUME_NAME, "available")

    @classmethod
    def tearDownClass(cls):
        try:
            raw_output_volume = cls.openstack(
                'volume delete ' + cls.VOLUME_NAME
            )
            cls.assertOutput('', raw_output_volume)
        finally:
            super().tearDownClass()

    def test_volume_transfer_request_accept(self):
        volume_name = uuid.uuid4().hex
        name = uuid.uuid4().hex

        # create a volume
        cmd_output = self.openstack(
            'volume create --size 1 ' + volume_name,
            parse_output=True,
        )
        self.assertEqual(volume_name, cmd_output['name'])

        # create volume transfer request for the volume
        # and get the auth_key of the new transfer request
        cmd_output = self.openstack(
            'volume transfer request create '
            + volume_name
            + ' --name '
            + name,
            parse_output=True,
        )
        auth_key = cmd_output['auth_key']
        self.assertTrue(auth_key)

        # accept the volume transfer request
        output = self.openstack(
            'volume transfer request accept '
            + name
            + ' '
            + '--auth-key '
            + auth_key,
            parse_output=True,
        )
        self.assertEqual(name, output.get('name'))

        # the volume transfer will be removed by default after accepted
        # so just need to delete the volume here
        raw_output = self.openstack('volume delete ' + volume_name)
        self.assertEqual('', raw_output)

    def test_volume_transfer_request_list_show(self):
        name = uuid.uuid4().hex
        cmd_output = self.openstack(
            'volume transfer request create '
            + ' --name '
            + name
            + ' '
            + self.VOLUME_NAME,
            parse_output=True,
        )
        self.addCleanup(
            self.openstack, 'volume transfer request delete ' + name
        )
        self.assertOutput(name, cmd_output['name'])
        auth_key = cmd_output['auth_key']
        self.assertTrue(auth_key)

        cmd_output = self.openstack(
            'volume transfer request list',
            parse_output=True,
        )
        self.assertIn(name, [req['Name'] for req in cmd_output])

        cmd_output = self.openstack(
            'volume transfer request show ' + name,
            parse_output=True,
        )
        self.assertEqual(name, cmd_output['name'])
