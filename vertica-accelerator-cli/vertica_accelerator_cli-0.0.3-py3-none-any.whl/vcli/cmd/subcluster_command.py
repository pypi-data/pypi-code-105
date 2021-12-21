#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on November 10, 2021
#
# Vertica Vaas Okta Subcluster command
#
# Usage:
#   va subcluster create --name a --subcluster_name xyz --instance_type i3.2xlarge --nodes 3 --module vertica_subcluster_1
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
from vcli.util.utils import build_api_client, db_name_validate
from vcli.util.static_params import (
    AWS_INSTANCE_TYPES,
    VALID_NODES_NUMBERS,
    VAAS_MODULES
)
from vcli.models.response_model import ResponseModel
from openapi_client.api.subcluster_v1_api import SubclusterV1Api
from openapi_client.api.database_detail_v1_api import DatabaseDetailV1Api


class SubclusterCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va subcluster create --name a --subcluster_name xyz --instance_type i3.2xlarge --nodes 3 --subcluster_id vertica_subcluster_1
        subcluster_parser = subparsers.add_parser('subcluster', help=HelpMessage.subcluster_header)
        subcluster_subparser = subcluster_parser.add_subparsers()

        # create command
        subcluster_create = subcluster_subparser.add_parser('create', help=HelpMessage.subcluster_create)
        subcluster_create.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.sub_create_name)
        subcluster_create.add_argument('--subcluster_name', metavar='<value>', required=True, type=str, help=HelpMessage.sub_create_subcluster_name)
        subcluster_create.add_argument('--nodes', metavar='<value>', required=True, type=int, choices=VALID_NODES_NUMBERS.list(), help=HelpMessage.sub_create_nodes)
        subcluster_create.add_argument('--instance_type', metavar='<value>', required=True, type=str, choices=AWS_INSTANCE_TYPES.list(), help=HelpMessage.sub_create_instance_type)
        subcluster_create.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.subcluster_list(), help=HelpMessage.sub_create_module)
        subcluster_create.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        subcluster_create.set_defaults(func=self.operation_create)

        # drop command
        subcluster_drop = subcluster_subparser.add_parser('drop', help=HelpMessage.subcluster_drop)
        subcluster_drop.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.sub_drop_name)
        subcluster_drop.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.subcluster_list(), help=HelpMessage.sub_drop_module)
        subcluster_drop.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        subcluster_drop.set_defaults(func=self.operation_drop)

        # start command
        subcluster_start = subcluster_subparser.add_parser('start', help=HelpMessage.subcluster_start)
        subcluster_start.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.sub_start_name)
        subcluster_start.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.subcluster_list(), help=HelpMessage.sub_start_module)
        subcluster_start.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        subcluster_start.set_defaults(func=self.operation_start)

        # stop command
        subcluster_stop = subcluster_subparser.add_parser('stop', help=HelpMessage.subcluster_stop)
        subcluster_stop.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.sub_stop_name)
        subcluster_stop.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.subcluster_list(), help=HelpMessage.sub_stop_module)
        subcluster_stop.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        subcluster_stop.set_defaults(func=self.operation_stop)

    def operation_cmd(self, args: Namespace) -> int:
        pass

    def operation_create(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = SubclusterV1Api(api_client=api_client).v1_vaas_databases_dbname_subclusters_post(
            dbname=args.name,
            body={
                "subcluster_name": args.subcluster_name,
                "module_name": args.subcluster_id,
                "instance_count": args.nodes,
                "instance_type": args.instance_type
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_drop(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = SubclusterV1Api(api_client=api_client).v1_vaas_databases_dbname_subclusters_delete(
            dbname=args.name,
            body={
                "module_name": args.subcluster_id
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_start(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseDetailV1Api(api_client=api_client).v1_vaas_databases_dbname_put(
            dbname=args.name,
            body={
                "db_action": DB_ACTION_START,
                "module_name": args.subcluster_id
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_stop(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DatabaseDetailV1Api(api_client=api_client).v1_vaas_databases_dbname_put(
            dbname=args.name,
            body={
                "db_action": DB_ACTION_STOP,
                "module_name": args.subcluster_id
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)
