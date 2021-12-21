#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on October 05 13:00 2021
#
# Vertica Vaas Okta Task command
#
# Usage:
#   va task list
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
from vcli.util.utils import build_api_client, db_name_validate
from vcli.util.static_params import (
    VALID_TASK
)
from vcli.models.response_model import ResponseModel

from openapi_client.api.task_v1_api import TaskV1Api
from openapi_client.api.task_detail_v1_api import TaskDetailV1Api
from openapi_client.api.task_latest_status_detail_v1_api import TaskLatestStatusDetailV1Api


class TaskCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va task list
        task_parser = subparsers.add_parser('task', help=HelpMessage.task_header)
        task_subparser = task_parser.add_subparsers()

        # list command
        task_list = task_subparser.add_parser('list', help=HelpMessage.task_list)
        task_list.add_argument('--name', metavar='<value>', required=False, type=db_name_validate, help=HelpMessage.task_list_name)
        task_list.add_argument('--type', metavar='<value>', required=False, default=VALID_TASK.ALL.value, choices=VALID_TASK.list(), type=str, help=HelpMessage.task_list_type)
        task_list.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        task_list.set_defaults(func=self.operation_list)

        # get command
        task_get = task_subparser.add_parser('get', help=HelpMessage.task_get)
        task_get.add_argument('--task_id', metavar='<value>', required=True, type=str, help=HelpMessage.task_get_id)
        task_get.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        task_get.set_defaults(func=self.operation_get)

        # status command
        task_status = task_subparser.add_parser('status', help=HelpMessage.task_status)
        task_status.add_argument('--task_id', metavar='<value>', required=True, type=str, help=HelpMessage.task_get_id)
        task_status.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        task_status.set_defaults(func=self.operation_status)

    def operation_cmd(self, args: Namespace) -> int:
        pass

    def operation_list(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = TaskV1Api(api_client=api_client).v1_vaas_tasks_get(
            dbname=args.name,
            type=args.type
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_get(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = TaskDetailV1Api(api_client=api_client).v1_vaas_tasks_task_id_get(task_id=args.task_id)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_status(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = TaskLatestStatusDetailV1Api(api_client=api_client).v1_vaas_tasks_task_id_latest_status_get(task_id=args.task_id)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)
