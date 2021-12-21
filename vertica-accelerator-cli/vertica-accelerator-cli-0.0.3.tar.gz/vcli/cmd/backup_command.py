#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on October 05 13:00 2021
#
# Vertica Vaas Okta Backup command
#
# Usage:
#   va backup list --name a
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
from openapi_client.api.backup_v1_api import BackupV1Api
from openapi_client.api.backup_restore_v1_api import BackupRestoreV1Api


class BackupCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va backup list --name a
        backup_parser = subparsers.add_parser('backup', help=HelpMessage.backup_header)
        backup_subparser = backup_parser.add_subparsers()

        # list command
        backup_list = backup_subparser.add_parser('list', help=HelpMessage.backup_list)
        backup_list.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.backup_list_name)
        backup_list.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        backup_list.set_defaults(func=self.operation_list)

        # create command
        backup_create = backup_subparser.add_parser('create', help=HelpMessage.backup_create)
        backup_create.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.backup_create_name)
        backup_create.add_argument('--config_script_base', metavar='<value>', required=True, type=str, help=HelpMessage.backup_create_config_script_base)
        backup_create.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        backup_create.set_defaults(func=self.operation_create)

        # restore command
        backup_restore = backup_subparser.add_parser('restore', help=HelpMessage.backup_restore)
        backup_restore.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.backup_restore_name)
        backup_restore.add_argument('--archive_id', metavar='<value>', required=True, type=str, help=HelpMessage.backup_restore_archive_id)
        backup_restore.add_argument('--include_objects', metavar='<value>', default="*", required=False, type=str, help=HelpMessage.backup_restore_include_objects)
        backup_restore.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        backup_restore.set_defaults(func=self.operation_restore)

    def operation_cmd(self, args: Namespace) -> int:
        pass

    def operation_list(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = BackupV1Api(api_client=api_client).v1_vaas_backups_dbname_get(dbname=args.name)
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_create(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = BackupV1Api(api_client=api_client).v1_vaas_backups_dbname_post(
            dbname=args.name,
            body={
                "config_script_base": args.config_script_base
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)

    def operation_restore(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = BackupRestoreV1Api(api_client=api_client).v1_vaas_restore_dbname_archive_id_post(
            archive_id=args.archive_id,
            dbname=args.name,
            body={
                "include_objects": args.include_objects
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            job_id=result.to_dict().get('jobid')
        )
        print(output)
