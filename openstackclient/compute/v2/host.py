#   Copyright 2012-2013 OpenStack Foundation
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
#

"""Host action implementations"""

from osc_lib.command import command
from osc_lib import utils

from openstackclient.i18n import _


class ListHost(command.Lister):
    _description = _("DEPRECATED: List hosts")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "--zone",
            metavar="<zone>",
            help=_("Only return hosts in the availability zone"),
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.sdk_connection.compute
        columns = ("Host Name", "Service", "Zone")

        self.log.warning(
            "API has been deprecated. "
            "Please consider using 'hypervisor list' instead."
        )

        # doing this since openstacksdk has decided not to support this
        # deprecated command
        hosts = (
            compute_client.get('/os-hosts', microversion='2.1')
            .json()
            .get('hosts')
        )

        if parsed_args.zone is not None:
            filtered_hosts = []
            for host in hosts:
                if host['zone'] == parsed_args.zone:
                    filtered_hosts.append(host)

            hosts = filtered_hosts

        return columns, (utils.get_dict_properties(s, columns) for s in hosts)


class SetHost(command.Command):
    _description = _("Set host properties")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "host", metavar="<host>", help=_("Host to modify (name only)")
        )
        status = parser.add_mutually_exclusive_group()
        status.add_argument(
            '--enable', action='store_true', help=_("Enable the host")
        )
        status.add_argument(
            '--disable', action='store_true', help=_("Disable the host")
        )
        maintenance = parser.add_mutually_exclusive_group()
        maintenance.add_argument(
            '--enable-maintenance',
            action='store_true',
            help=_("Enable maintenance mode for the host"),
        )
        maintenance.add_argument(
            '--disable-maintenance',
            action='store_true',
            help=_("Disable maintenance mode for the host"),
        )
        return parser

    def take_action(self, parsed_args):
        kwargs = {}

        if parsed_args.enable:
            kwargs['status'] = 'enable'
        if parsed_args.disable:
            kwargs['status'] = 'disable'
        if parsed_args.enable_maintenance:
            kwargs['maintenance_mode'] = 'enable'
        if parsed_args.disable_maintenance:
            kwargs['maintenance_mode'] = 'disable'

        compute_client = self.app.client_manager.compute

        compute_client.api.host_set(parsed_args.host, **kwargs)


class ShowHost(command.Lister):
    _description = _("DEPRECATED: Display host details")

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument("host", metavar="<host>", help=_("Name of host"))
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.sdk_connection.compute
        columns = ("Host", "Project", "CPU", "Memory MB", "Disk GB")

        self.log.warning(
            "API has been deprecated. "
            "Please consider using 'hypervisor show' instead."
        )

        # doing this since openstacksdk has decided not to support this
        # deprecated command
        resources = (
            compute_client.get(
                '/os-hosts/' + parsed_args.host, microversion='2.1'
            )
            .json()
            .get('host')
        )

        data = []
        if resources is not None:
            for resource in resources:
                data.append(resource['resource'])

        return columns, (utils.get_dict_properties(s, columns) for s in data)
