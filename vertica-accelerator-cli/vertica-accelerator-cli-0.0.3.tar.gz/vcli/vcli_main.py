#!/bin/python3
# PYTHON_ARGCOMPLETE_OK
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on September 29 11:03 2021
# (c) Copyright 2021 Micro Focus or one of its affiliates.
# ------------------------------------------------------------------------------
import argparse
import sys
import argcomplete
import traceback

from vcli.exceptions.vcli_custom_exception import BaseCustomException
from vcli.models.response_model import ResponseModel
from vcli.util.vcli_logger import logger
from vcli.util.help_message import HelpMessage as ARG_DESC
from vcli.util.error_message import ErrorMessage
from vcli.util.utils import log_arg_func
from vcli.constant import RETURN_CODE_SUCCESS, RETURN_CODE_ERROR, RETURN_CODE_UNKNOWN

from vcli.cmd.sub_command import SubCommand
from vcli.cmd.auth_command import AuthCommand
from vcli.cmd.config_command import ConfigCommand
from vcli.cmd.database_command import DatabaseCommand
from vcli.cmd.database_config_command import DatabaseConfigCommand
from vcli.cmd.subcluster_command import SubclusterCommand
from vcli.cmd.backup_command import BackupCommand
from vcli.cmd.session_command import SessionCommand
from vcli.cmd.task_command import TaskCommand
from vcli.cmd.cron_command import CronCommand
from vcli.cmd.report_command import ReportCommand
from vcli.cmd.dns_command import DNSCommand

from openapi_client.exceptions import ApiException, UnauthorizedException


class VcliMain:
    def __init__(self):
        # Config command
        self.config_command = SubCommand(ConfigCommand())

        # Login command
        self.auth_command = SubCommand(AuthCommand())

        # Database command
        self.database_command = SubCommand(DatabaseCommand())

        # Database Config command
        self.database_config_command = SubCommand(DatabaseConfigCommand())

        # Subcluster command
        self.subcluster_command = SubCommand(SubclusterCommand())

        # Backup command
        self.backup_command = SubCommand(BackupCommand())

        # Session command
        self.session_command = SubCommand(SessionCommand())

        # Task command
        self.task_command = SubCommand(TaskCommand())

        # Cron command
        self.cron_command = SubCommand(CronCommand())

        # Report command
        self.report_command = SubCommand(ReportCommand())

        # DNS command
        self.dns_command = SubCommand(DNSCommand())

    def parse(self):
        parser = argparse.ArgumentParser(description=ARG_DESC.vcli_header)
        subparsers = parser.add_subparsers()

        self.config_command.arg_define(subparsers)
        self.auth_command.arg_define(subparsers)
        self.database_command.arg_define(subparsers)
        self.database_config_command.arg_define(subparsers)
        self.subcluster_command.arg_define(subparsers)
        self.backup_command.arg_define(subparsers)
        self.session_command.arg_define(subparsers)
        self.task_command.arg_define(subparsers)
        self.cron_command.arg_define(subparsers)
        self.report_command.arg_define(subparsers)
        self.dns_command.arg_define(subparsers)

        # Autocompleter
        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        try:
            log_arg_func(args)
            args.func(args)
        except AttributeError as e:
            logger.exception(traceback.format_exc())
            logger.error(e)
            parser.parse_args(['-h'])
            sys.exit(RETURN_CODE_ERROR)
        except BaseCustomException as ce:
            logger.error(ce)
            output = ResponseModel(
                return_code=ce.error_code,
                error_message=ce.msg
            )
            print(output, file=sys.stderr)
            sys.exit(ce.error_code)
        except UnauthorizedException as ue:
            logger.error(ue)
            output = ResponseModel(
                return_code=RETURN_CODE_ERROR,
                error_message=ErrorMessage.ERROR_VERIFY_ACCESS_TOKEN_FAIL
            )
            print(output, file=sys.stderr)
            sys.exit(RETURN_CODE_ERROR)
        except ApiException as ae:
            logger.error(ae)
            output = ResponseModel(
                return_code=RETURN_CODE_ERROR,
                error_message=ae.reason
            )
            print(output, file=sys.stderr)
            sys.exit(RETURN_CODE_ERROR)
        except Exception as e:
            logger.exception(traceback.format_exc())
            logger.error(e)
            output = ResponseModel(
                return_code=RETURN_CODE_UNKNOWN,
                error_message=ErrorMessage.GENERAL_ERROR
            )
            print(output, file=sys.stderr)
            sys.exit(RETURN_CODE_UNKNOWN)
        sys.exit(RETURN_CODE_SUCCESS)


def va_command():
    vcli_main = VcliMain()
    vcli_main.parse()


if __name__ == '__main__':
    vcli_main = VcliMain()
    vcli_main.parse()
