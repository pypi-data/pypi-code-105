#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on November 19 2021
#
# Vertica Vaas Okta Cron command
#
# Usage:
#   va cron add --name a --cron_name b --cron_action start --cron_expression "30 14 ? * * *" --module vertica_cluster
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
from vcli.util.utils import build_api_client, db_name_validate, cron_name_validate
from vcli.util.static_params import (
    VAAS_MODULES,
    CRON_ACTION,
    TOGGLE_ACTION
)
from vcli.models.response_model import ResponseModel
from openapi_client.api.cron_job_config_v1_api import CronJobConfigV1Api
from openapi_client.api.cron_update_config_v1_api import CronUpdateConfigV1Api


class CronCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va cron add --name a --cron_name b --cron_action start --cron_expression "30 14 ? * * *" --subcluster_id vertica_cluster
        
        cron_parser = subparsers.add_parser('cron', help=HelpMessage.cron_header)
        cron_subparser = cron_parser.add_subparsers()

        # list command
        cron_list = cron_subparser.add_parser('list', help=HelpMessage.cron_list)
        cron_list.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.list_name)
        cron_list.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        cron_list.set_defaults(func=self.operation_list)

        # add command
        cron_start = cron_subparser.add_parser('add', help=HelpMessage.cron_add)
        cron_start.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.add_name)
        cron_start.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.list(), help=HelpMessage.add_module)
        cron_start.add_argument('--cron_name', metavar='<value>', required=True, type=cron_name_validate, help=HelpMessage.add_cron_name)
        cron_start.add_argument('--cron_action', metavar='<value>', required=True, type=str, choices=CRON_ACTION.list(), help=HelpMessage.add_cron_action)
        cron_start.add_argument('--cron_expression', metavar='<value>', required=True, type=str, help=HelpMessage.add_cron_expression)
        cron_start.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        cron_start.set_defaults(func=self.operation_add)

        # remove command
        cron_stop = cron_subparser.add_parser('remove', help=HelpMessage.cron_remove)
        cron_stop.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.remove_name)
        cron_stop.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.list(), help=HelpMessage.remove_module)
        cron_stop.add_argument('--cron_name', metavar='<value>', required=True, type=cron_name_validate, help=HelpMessage.remove_cron_name)
        cron_stop.add_argument('--cron_action', metavar='<value>', required=True, type=str, choices=CRON_ACTION.list(), help=HelpMessage.remove_cron_action)
        cron_stop.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        cron_stop.set_defaults(func=self.operation_remove)

        # set command
        cron_set = cron_subparser.add_parser('set', help=HelpMessage.cron_set)
        cron_set.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.set_name)
        cron_set.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.list(), help=HelpMessage.set_module)
        cron_set.add_argument('--cron_name', metavar='<value>', required=True, type=cron_name_validate, help=HelpMessage.set_cron_name)
        cron_set.add_argument('--cron_action', metavar='<value>', required=True, type=str, choices=CRON_ACTION.list(), help=HelpMessage.set_cron_action)
        cron_set.add_argument('--action', metavar='<value>', required=True, type=str, choices=TOGGLE_ACTION.list(), help=HelpMessage.set_action)
        cron_set.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        cron_set.set_defaults(func=self.operation_set)

        # update command
        cron_update = cron_subparser.add_parser('update', help=HelpMessage.cron_update)
        cron_update.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.update_name)
        cron_update.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.list(), help=HelpMessage.update_module)
        cron_update.add_argument('--cron_name', metavar='<value>', required=True, type=cron_name_validate, help=HelpMessage.update_cron_name)
        cron_update.add_argument('--cron_action', metavar='<value>', required=True, type=str, choices=CRON_ACTION.list(), help=HelpMessage.update_cron_action)
        cron_update.add_argument('--cron_expression', metavar='<value>', required=True, type=str, help=HelpMessage.update_cron_expression)
        cron_update.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        cron_update.set_defaults(func=self.operation_update)

    def operation_cmd(self, args: Namespace) -> int:
        pass

    def operation_list(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = CronJobConfigV1Api(api_client=api_client).v1_vaas_cron_dbname_get(dbname=args.name)
        if result.to_dict().get('data') == None:
            output = ResponseModel(
                return_code=RETURN_CODE_SUCCESS,
                data="There are no cronjobs associated with the database."
            )
        else:
            output = ResponseModel(
                return_code=RETURN_CODE_SUCCESS,
                data=result.to_dict().get('data')
            )
        print(output)

    def operation_add(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = CronJobConfigV1Api(api_client=api_client).v1_vaas_cron_dbname_post(
            dbname=args.name,
            body={
                "action": args.cron_action,
                "expr": args.cron_expression,
                "module": args.subcluster_id,
                "name": args.cron_name
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_remove(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = CronJobConfigV1Api(api_client=api_client).v1_vaas_cron_dbname_delete(
            dbname=args.name,
            body={
                "action": args.cron_action,
                "module": args.subcluster_id,
                "name": args.cron_name
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_set(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        set_action = True if args.action == TOGGLE_ACTION.ENABLE.value else False
        result = CronUpdateConfigV1Api(api_client=api_client).v1_vaas_cron_dbname_schedule_name_post(
            dbname=args.name,
            schedule_name=args.cron_name,
            body={
                "action": args.cron_action,
                "enable": set_action,
                "module": args.subcluster_id
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_update(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = CronUpdateConfigV1Api(api_client=api_client).v1_vaas_cron_dbname_schedule_name_put(
            dbname=args.name,
            schedule_name=args.cron_name,
            body={
                "action": args.cron_action,
                "expr": args.cron_expression,
                "module": args.subcluster_id
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)
