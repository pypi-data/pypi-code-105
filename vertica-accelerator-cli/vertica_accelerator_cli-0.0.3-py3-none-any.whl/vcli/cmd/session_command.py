#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on October 05 13:00 2021
#
# Vertica Vaas Okta Session command
#
# Usage:
#   va session list
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
from vcli.models.response_model import ResponseModel
from openapi_client.api.session_v1_api import SessionV1Api


class SessionCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va session list
        session_parser = subparsers.add_parser('session', help=HelpMessage.session_header)
        session_subparser = session_parser.add_subparsers()

        # list command
        session_list = session_subparser.add_parser('list', help=HelpMessage.session_list)
        session_list.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.session_remove_name)
        session_list.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        session_list.set_defaults(func=self.operation_list)

        # remove command
        session_remove = session_subparser.add_parser('remove', help=HelpMessage.session_remove)
        session_remove.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.session_remove_name)
        session_remove.add_argument('--session', metavar='<value>', required=True, type=str, help=HelpMessage.session_remove_id)
        session_remove.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        session_remove.set_defaults(func=self.operation_remove)

    def operation_cmd(self, args: Namespace) -> int:
        pass

    def operation_list(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = SessionV1Api(api_client=api_client).v1_vaas_sessions_dbname_get(dbname=args.name)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_remove(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = SessionV1Api(api_client=api_client).v1_vaas_sessions_dbname_delete(
            dbname=args.name,
            body={
                "session_id": args.session
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)
