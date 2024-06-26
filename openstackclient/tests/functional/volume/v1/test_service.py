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

from openstackclient.tests.functional.volume.v1 import common


class VolumeServiceTests(common.BaseVolumeTests):
    """Functional tests for volume service."""

    def test_volume_service_list(self):
        cmd_output = self.openstack('volume service list', parse_output=True)

        # Get the nonredundant services and hosts
        services = list({x['Binary'] for x in cmd_output})

        # Test volume service list --service
        cmd_output = self.openstack(
            'volume service list ' + '--service ' + services[0],
            parse_output=True,
        )
        for x in cmd_output:
            self.assertEqual(services[0], x['Binary'])

        # TODO(zhiyong.dai): test volume service list --host after solving
        # https://bugs.launchpad.net/python-openstackclient/+bug/1664451

    def test_volume_service_set(self):
        # Get a service and host
        cmd_output = self.openstack(
            'volume service list',
            parse_output=True,
        )
        service_1 = cmd_output[0]['Binary']
        host_1 = cmd_output[0]['Host']

        # Test volume service set --enable
        raw_output = self.openstack(
            'volume service set --enable ' + host_1 + ' ' + service_1
        )
        self.assertOutput('', raw_output)

        cmd_output = self.openstack(
            'volume service list --long',
            parse_output=True,
        )
        self.assertEqual('enabled', cmd_output[0]['Status'])
        self.assertIsNone(cmd_output[0]['Disabled Reason'])

        # Test volume service set --disable and --disable-reason
        disable_reason = 'disable_reason'
        raw_output = self.openstack(
            'volume service set --disable '
            + '--disable-reason '
            + disable_reason
            + ' '
            + host_1
            + ' '
            + service_1
        )
        self.assertOutput('', raw_output)

        cmd_output = self.openstack(
            'volume service list --long',
            parse_output=True,
        )
        self.assertEqual('disabled', cmd_output[0]['Status'])
        self.assertEqual(disable_reason, cmd_output[0]['Disabled Reason'])
