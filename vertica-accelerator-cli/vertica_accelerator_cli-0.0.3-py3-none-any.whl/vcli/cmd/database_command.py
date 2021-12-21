#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on October 05 13:00 2021
#
# Vertica Vaas Okta Database command
#
# Usage:
#   va database create --name a --password b --nodes 3 --region us-east-1 --availability_zone us-east-1a --instance_type i3.2xlarge
#
# (c) Copyright 2021 Micro Focus or one of its affiliates.
# ------------------------------------------------------------------------------
from argparse import Namespace
from vcli.cmd.sub_command import SubCommandImplementation
from vcli.util.help_message import HelpMessage
from vcli.constant import (
    DB_ACTION_START,
    DB_ACTION_STOP,
    VCLI_CONFIG_DEFAULT,
    RETURN_CODE_SUCCESS
)
from vcli.util.utils import build_api_client, str_to_bool, db_name_validate
from vcli.util.static_params import (
    AWS_INSTANCE_TYPES,
    SUPPORTED_AWS_REGIONS,
    SUPPORTED_AWS_ZONES,
    SUPPORTED_VERTICA_VERSIONS,
    VAAS_MODULES,
    VALID_NODES_NUMBERS
)
from vcli.models.response_model import ResponseModel

from openapi_client.api.database_v1_api import DatabaseV1Api
from openapi_client.api.database_detail_v1_api import DatabaseDetailV1Api
from openapi_client.api.database_hibernate_v1_api import DatabaseHibernateV1Api
from openapi_client.api.database_revive_v1_api import DatabaseReviveV1Api
from openapi_client.api.database_resize_v1_api import DatabaseResizeV1Api
from openapi_client.api.database_rescale_v1_api import DatabaseRescaleV1Api
from openapi_client.api.database_upgrade_v1_api import DatabaseUpgradeV1Api
from openapi_client.api.network_config_v1_api import NetworkConfigV1Api


class DatabaseCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va database create --name a --password b --nodes 3 --region us-east-1 --availability_zone us-east-1a --instance_type i3.2xlarge
        database_parser = subparsers.add_parser('database', help=HelpMessage.database_header)
        database_subparser = database_parser.add_subparsers()

        # create command
        database_create = database_subparser.add_parser('create', help=HelpMessage.database_create)
        database_create.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.create_name)
        database_create.add_argument('--password', metavar='<value>', required=True, type=str, help=HelpMessage.create_password)
        database_create.add_argument('--nodes', metavar='<value>', required=True, type=int, choices=VALID_NODES_NUMBERS.list(), help=HelpMessage.create_nodes)
        database_create.add_argument('--region', metavar='<value>', required=True, type=str, choices=SUPPORTED_AWS_REGIONS.list(), help=HelpMessage.create_region)
        database_create.add_argument('--availability_zone', metavar='<value>', required=True, type=str, choices=SUPPORTED_AWS_ZONES.list(), help=HelpMessage.create_availability_zone)
        database_create.add_argument('--instance_type', metavar='<value>', required=True, type=str, choices=AWS_INSTANCE_TYPES.list(), help=HelpMessage.create_instance_type)
        database_create.add_argument('--external_access_cidr_block', metavar='<value>', required=False, type=str, help=HelpMessage.create_external_access_cidr_block)
        database_create.add_argument('--vertica_version', metavar='<value>', required=False, type=str, choices=SUPPORTED_VERTICA_VERSIONS.list(), help=HelpMessage.create_vertica_version)
        database_create.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_create.set_defaults(func=self.operation_create)

        # list command
        database_list = database_subparser.add_parser('list', help=HelpMessage.database_list)
        database_list.add_argument('--brief', metavar='<value>', default=True, required=False, type=str_to_bool, help=HelpMessage.list_brief)
        database_list.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_list.set_defaults(func=self.operation_list)

        # get command
        database_get = database_subparser.add_parser('get', help=HelpMessage.database_get)
        database_get.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.get_name)
        database_get.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_get.set_defaults(func=self.operation_get)

        # start command
        database_start = database_subparser.add_parser('start', help=HelpMessage.database_start)
        database_start.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.start_name)
        database_start.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_start.set_defaults(func=self.operation_start)

        # stop command
        database_stop = database_subparser.add_parser('stop', help=HelpMessage.database_stop)
        database_stop.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.stop_name)
        database_stop.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_stop.set_defaults(func=self.operation_stop)

        # hibernate command
        database_hibernate = database_subparser.add_parser('hibernate', help=HelpMessage.database_hibernate)
        database_hibernate.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.hibernate_name)
        database_hibernate.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_hibernate.set_defaults(func=self.operation_hibernate)

        # revive command
        database_revive = database_subparser.add_parser('revive', help=HelpMessage.database_revive)
        database_revive.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.revive_name)
        database_revive.add_argument('--availability_zone', metavar='<value>', required=True, type=str, choices=SUPPORTED_AWS_ZONES.list(), help=HelpMessage.revive_availability_zone)
        database_revive.add_argument('--instance_type', metavar='<value>', required=True, type=str, choices=AWS_INSTANCE_TYPES.list(), help=HelpMessage.revive_instance_type)
        database_revive.add_argument('--external_access_cidr_block', metavar='<value>', required=False, type=str, help=HelpMessage.revive_external_access_cidr_block)
        database_revive.add_argument('--vertica_version', metavar='<value>', required=False, type=str, choices=SUPPORTED_VERTICA_VERSIONS.list(), help=HelpMessage.revive_vertica_version)
        database_revive.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_revive.set_defaults(func=self.operation_revive)

        # drop command
        database_drop = database_subparser.add_parser('drop', help=HelpMessage.database_drop)
        database_drop.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.drop_name)
        database_drop.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_drop.set_defaults(func=self.operation_drop)

        # increase command
        database_increase = database_subparser.add_parser('increase', help=HelpMessage.database_increase)
        database_increase.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.increase_name)
        database_increase.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.list(), help=HelpMessage.increase_module)
        database_increase.add_argument('--nodes', metavar='<value>', required=True, type=int, choices=VALID_NODES_NUMBERS.list(), help=HelpMessage.increase_nodes)
        database_increase.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_increase.set_defaults(func=self.operation_resize_increase)

        # decrease command
        database_decrease = database_subparser.add_parser('decrease', help=HelpMessage.database_decrease)
        database_decrease.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.decrease_name)
        database_decrease.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.list(), help=HelpMessage.decrease_module)
        database_decrease.add_argument('--nodes', metavar='<value>', required=True, type=int, choices=VALID_NODES_NUMBERS.list(), help=HelpMessage.decrease_nodes)
        database_decrease.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_decrease.set_defaults(func=self.operation_resize_decrease)

        # rescale command
        database_rescale = database_subparser.add_parser('rescale', help=HelpMessage.database_rescale)
        database_rescale.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.rescale_name)
        database_rescale.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.list(), help=HelpMessage.rescale_module)
        database_rescale.add_argument('--instance_type', metavar='<value>', required=True, type=str, choices=AWS_INSTANCE_TYPES.list(), help=HelpMessage.rescale_instance_type)
        database_rescale.add_argument('--subcluster_name', metavar='<value>', default='', required=False, type=str, help=HelpMessage.rescale_subcluster_name)
        database_rescale.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_rescale.set_defaults(func=self.operation_rescale)

        # upgrade command
        database_upgrade = database_subparser.add_parser('upgrade', help=HelpMessage.database_upgrade)
        database_upgrade.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.upgrade_name)
        database_upgrade.add_argument('--vertica_version', metavar='<value>', required=True, type=str, choices=SUPPORTED_VERTICA_VERSIONS.list(), help=HelpMessage.upgrade_vertica_version)
        database_upgrade.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_upgrade.set_defaults(func=self.operation_upgrade)

        # update-network-config command
        database_update_network_config = database_subparser.add_parser('update-network-config', help=HelpMessage.database_update_network_config)
        database_update_network_config.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.update_network_config_name)
        database_update_network_config.add_argument('--external_access_cidr_block', metavar='<value>', required=True, type=str, help=HelpMessage.update_network_config_external_access_cidr_block)
        database_update_network_config.add_argument('--enable_ssh', metavar='<value>', required=False, default=None, type=str_to_bool, help=HelpMessage.update_network_config_enable_ssh)
        database_update_network_config.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_update_network_config.set_defaults(func=self.operation_update_network_config)

    def operation_cmd(self, args: Namespace) -> int:
        pass

    def operation_create(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        external_cird = (args.external_access_cidr_block).split(',') if args.external_access_cidr_block else []
        result = DatabaseV1Api(api_client=api_client).v1_vaas_databases_post(
            body={
                "dbname": args.name,
                "passwd": args.password,
                "primary_cluster_nodes": args.nodes,
                "az": args.availability_zone,
                "instance_type": args.instance_type,
                "region": args.region,
                "external_access_cidr_block": external_cird,
                "vertica_version": args.vertica_version
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_list(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseV1Api(api_client=api_client).v1_vaas_databases_get(brief=args.brief)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_get(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseDetailV1Api(api_client=api_client).v1_vaas_databases_dbname_get(dbname=args.name)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_start(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseDetailV1Api(api_client=api_client).v1_vaas_databases_dbname_put(dbname=args.name, body={
            "db_action": DB_ACTION_START,
            "module_name": VAAS_MODULES.VERTICA_CLUSTER.value
        })
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_stop(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseDetailV1Api(api_client=api_client).v1_vaas_databases_dbname_put(dbname=args.name, body={
            "db_action": DB_ACTION_STOP,
            "module_name": VAAS_MODULES.VERTICA_CLUSTER.value
        })
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_hibernate(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseHibernateV1Api(api_client=api_client).v1_vaas_databases_dbname_hibernate_put(dbname=args.name)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_revive(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        external_cird = (args.external_access_cidr_block).split(',') if args.external_access_cidr_block else []
        result = DatabaseReviveV1Api(api_client=api_client).v1_vaas_databases_dbname_revive_put(dbname=args.name, body={
            "az": args.availability_zone,
            "instance_type": args.instance_type,
            "external_access_cidr_block": external_cird,
            "vertica_version ": args.vertica_version
        })
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_drop(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseDetailV1Api(api_client=api_client).v1_vaas_databases_dbname_delete(dbname=args.name)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_resize_increase(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseResizeV1Api(api_client=api_client).v1_vaas_databases_dbname_resize_increase_put(dbname=args.name, body={
            "instance_count": args.nodes,
            "module_name": args.subcluster_id
        })
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_resize_decrease(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseResizeV1Api(api_client=api_client).v1_vaas_databases_dbname_resize_decrease_put(dbname=args.name, body={
            "instance_count": args.nodes,
            "module_name": args.subcluster_id
        })
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_rescale(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseRescaleV1Api(api_client=api_client).v1_vaas_databases_dbname_rescale_put(dbname=args.name, body={
            "module_name": args.subcluster_id,
            "instance_type": args.instance_type,
            "subcluster_name": args.subcluster_name
        })
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_upgrade(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseUpgradeV1Api(api_client=api_client).v1_vaas_databases_dbname_upgrade_put(dbname=args.name, body={
            "vertica_version": args.vertica_version
        })
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_update_network_config(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        external_cird = (args.external_access_cidr_block).split(',') if args.external_access_cidr_block else []
        body = {
            "external_access_cidr_block": external_cird
        }
        if args.enable_ssh is not None:
            body["enable_ssh"] = args.enable_ssh
        result = NetworkConfigV1Api(api_client=api_client).v1_vaas_config_dbname_cidr_block_put(dbname=args.name, body=body)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)
