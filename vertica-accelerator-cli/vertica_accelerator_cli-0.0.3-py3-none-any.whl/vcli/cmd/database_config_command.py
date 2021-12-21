#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on October 05 13:00 2021
#
# Vertica Vaas Okta Database Config command
#
# Usage:
#   va database database-config idle-shutdown list --name a
#
# (c) Copyright 2021 Micro Focus or one of its affiliates.
# ------------------------------------------------------------------------------
from argparse import Namespace
from vcli.cmd.sub_command import SubCommandImplementation
from vcli.util.help_message import HelpMessage
from vcli.constant import (
    VCLI_CONFIG_DEFAULT,
    RETURN_CODE_SUCCESS
)
from vcli.util.utils import build_api_client, str_to_bool, db_name_validate
from vcli.util.static_params import IDLE_SHUTDOWN_TIME

from vcli.models.response_model import ResponseModel

from openapi_client.api.schedule_idle_shutdown_v1_api import ScheduleIdleShutdownV1Api
from openapi_client.api.schedule_auto_scaling_v1_api import ScheduleAutoScalingV1Api


class DatabaseConfigCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va database database-config idle-shutdown list --name a
        database_config_parser = subparsers.add_parser('database-config', help=HelpMessage.database_config_header)
        database_config_subparser = database_config_parser.add_subparsers()

        # idle-shutdown command
        database_config_idle_shutdown = database_config_subparser.add_parser('idle-shutdown', help=HelpMessage.database_config_idle_shutdown)
        database_config_idle_shutdown_subparser = database_config_idle_shutdown.add_subparsers()

        # idle-shutdown list command
        database_config_idle_shutdown_list = database_config_idle_shutdown_subparser.add_parser('list', help=HelpMessage.database_config_idle_shutdown_list)
        database_config_idle_shutdown_list.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.database_config_idle_shutdown_list_name)
        database_config_idle_shutdown_list.add_argument('--enabled', metavar='<value>', required=False, default=None, type=str_to_bool, help=HelpMessage.database_config_idle_shutdown_list_enabled)
        database_config_idle_shutdown_list.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_config_idle_shutdown_list.set_defaults(func=self.operation_idle_shutdown_list)

        # idle-shutdown update command
        database_config_idle_shutdown_update = database_config_idle_shutdown_subparser.add_parser('update', help=HelpMessage.database_config_idle_shutdown_update)
        database_config_idle_shutdown_update.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.database_config_idle_shutdown_update_name)
        database_config_idle_shutdown_update.add_argument('--shutdown_timeout', metavar='<value>', required=True, type=int, choices=IDLE_SHUTDOWN_TIME.list(), help=HelpMessage.database_config_idle_shutdown_update_shutdown_timeout)
        database_config_idle_shutdown_update.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_config_idle_shutdown_update.set_defaults(func=self.operation_idle_shutdown_update)

        # idle-shutdown delete command
        database_config_idle_shutdown_delete = database_config_idle_shutdown_subparser.add_parser('delete', help=HelpMessage.database_config_idle_shutdown_delete)
        database_config_idle_shutdown_delete.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.database_config_idle_shutdown_delete_name)
        database_config_idle_shutdown_delete.add_argument('--permanent', metavar='<value>', required=False, default=False, type=str_to_bool, help=HelpMessage.database_config_idle_shutdown_delete_shutdown_permanent)
        database_config_idle_shutdown_delete.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_config_idle_shutdown_delete.set_defaults(func=self.operation_idle_shutdown_delete)

        # auto-scale command
        database_config_auto_scale = database_config_subparser.add_parser('auto-scale', help=HelpMessage.database_config_auto_scale)
        database_config_auto_scale_subparser = database_config_auto_scale.add_subparsers()

        # auto-scale list command
        database_config_auto_scale_list = database_config_auto_scale_subparser.add_parser('list', help=HelpMessage.database_config_auto_scale_list)
        database_config_auto_scale_list.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.database_config_auto_scale_list_name)
        database_config_auto_scale_list.add_argument('--enabled', metavar='<value>', required=False, default=None, type=str_to_bool, help=HelpMessage.database_config_auto_scale_list_enabled)
        database_config_auto_scale_list.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_config_auto_scale_list.set_defaults(func=self.operation_auto_scale_list)

        # auto-scale update command
        database_config_auto_scale_update = database_config_auto_scale_subparser.add_parser('update', help=HelpMessage.database_config_auto_scale_update)
        database_config_auto_scale_update.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.database_config_auto_scale_update_name)
        database_config_auto_scale_update.add_argument('--client_drain_time', metavar='<value>', default=5, required=False, type=int, help=HelpMessage.database_config_auto_scale_update_client_drain_time)
        database_config_auto_scale_update.add_argument('--sequence_count', metavar='<value>', default=5, required=False, type=int, help=HelpMessage.database_config_auto_scale_update_sequence_count)
        database_config_auto_scale_update.add_argument('--max_sessions', metavar='<value>', default=5, required=False, type=int, help=HelpMessage.database_config_auto_scale_update_max_sessions)
        database_config_auto_scale_update.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_config_auto_scale_update.set_defaults(func=self.operation_auto_scale_update)

        # auto-scale delete command
        database_config_auto_scale_delete = database_config_auto_scale_subparser.add_parser('delete', help=HelpMessage.database_config_auto_scale_delete)
        database_config_auto_scale_delete.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.database_config_idle_shutdown_delete_name)
        database_config_auto_scale_delete.add_argument('--permanent', metavar='<value>', required=False, default=False, type=str_to_bool, help=HelpMessage.database_config_idle_shutdown_delete_shutdown_permanent)
        database_config_auto_scale_delete.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        database_config_auto_scale_delete.set_defaults(func=self.operation_auto_scale_delete)

    def operation_cmd(self, args: Namespace) -> int:
        pass

    def operation_idle_shutdown_list(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = ScheduleIdleShutdownV1Api(api_client=api_client).v1_vaas_databases_dbname_idle_shutdown_get(dbname=args.name, enabled=args.enabled)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_idle_shutdown_update(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = ScheduleIdleShutdownV1Api(api_client=api_client).v1_vaas_databases_dbname_idle_shutdown_put(
            dbname=args.name,
            body={
                "shutdown_timeout": "00:%02d:00" % (args.shutdown_timeout)
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_idle_shutdown_delete(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = ScheduleIdleShutdownV1Api(api_client=api_client).v1_vaas_databases_dbname_idle_shutdown_delete(
            dbname=args.name,
            body={
                "permanent": args.permanent
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_auto_scale_list(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = ScheduleAutoScalingV1Api(api_client=api_client).v1_vaas_databases_dbname_auto_scaling_get(dbname=args.name, enabled=args.enabled)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_auto_scale_update(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = ScheduleAutoScalingV1Api(api_client=api_client).v1_vaas_databases_dbname_auto_scaling_put(
            dbname=args.name,
            body={
                "client_drain_time": args.client_drain_time,
                "sequence_count": args.sequence_count,
                "subcluster": {
                    "vertica_subcluster_1_max_session": args.max_sessions,
                    "vertica_subcluster_2_max_session": args.max_sessions,
                    "vertica_subcluster_3_max_session": args.max_sessions
                }
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_auto_scale_delete(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = ScheduleAutoScalingV1Api(api_client=api_client).v1_vaas_databases_dbname_auto_scaling_delete(
            dbname=args.name,
            body={
                "permanent": args.permanent
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)
