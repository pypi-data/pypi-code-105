#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on November 23 2021
#
# Vertica Vaas Okta DNS command
#
# Usage:
#   va dns create --name dbname --module vertica_cluster --dnsname name
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
from vcli.util.utils import build_api_client, db_name_validate, dns_name_validate
from vcli.util.static_params import (
    VAAS_MODULES
)
from vcli.models.response_model import ResponseModel
from openapi_client.api.dns_config_v1_api import DnsConfigV1Api


class DNSCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va dns create --name dbname --subcluster_id vertica_cluster --dnsname name

        dns_parser = subparsers.add_parser('dns', help=HelpMessage.dns_header)
        dns_subparser = dns_parser.add_subparsers()

        # list command
        dns_list = dns_subparser.add_parser('list', help=HelpMessage.dns_list)
        dns_list.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.dns_list_name)
        dns_list.add_argument('--dnsname', metavar='<value>', required=False, type=dns_name_validate, help=HelpMessage.dns_list_dnsname)
        dns_list.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        dns_list.set_defaults(func=self.operation_list)

        # create command
        dns_create = dns_subparser.add_parser('create', help=HelpMessage.dns_create)
        dns_create.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.dns_create_name)
        dns_create.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, nargs='*', choices=VAAS_MODULES.list(), help=HelpMessage.dns_create_module)
        dns_create.add_argument('--dnsname', metavar='<value>', required=False, type=dns_name_validate, help=HelpMessage.dns_create_dnsname)
        dns_create.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        dns_create.set_defaults(func=self.operation_create_update)

        # remove command
        dns_remove = dns_subparser.add_parser('remove', help=HelpMessage.dns_remove)
        dns_remove.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.dns_remove_name)
        dns_remove.add_argument('--dnsname', metavar='<value>', required=True, type=dns_name_validate, help=HelpMessage.dns_remove_dnsname)
        dns_remove.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        dns_remove.set_defaults(func=self.operation_remove)

        # update command
        dns_update = dns_subparser.add_parser('update', help=HelpMessage.dns_update)
        dns_update.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.dns_update_name)
        dns_update.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, nargs='*', choices=VAAS_MODULES.list(), help=HelpMessage.dns_update_module)
        dns_update.add_argument('--dnsname', metavar='<value>', required=False, type=dns_name_validate, help=HelpMessage.dns_update_dnsname)
        dns_update.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        dns_update.set_defaults(func=self.operation_create_update)

    def operation_cmd(self, args: Namespace) -> int:
        pass

    def operation_list(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DnsConfigV1Api(api_client=api_client).v1_vaas_dns_dbname_get(
            dbname=args.name,
            dnsname=args.dnsname
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_create_update(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DnsConfigV1Api(api_client=api_client).v1_vaas_dns_dbname_post(
            dbname=args.name, 
            body={
                "dnsname": args.dnsname,
                "module_names": args.subcluster_id,
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_remove(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)
        result = DnsConfigV1Api(api_client=api_client).v1_vaas_dns_dbname_delete(
            dbname=args.name, 
            body={
                "dnsname": args.dnsname
            }
        )
        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)
