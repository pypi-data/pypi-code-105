#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on November 25 2021
#
# Vertica Vaas Okta Report command
#
# Usage:
#   va report show --name dbname --module vertica_cluster --report_name query_per_hour --range '1 hour'
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
from vcli.util.utils import build_api_client, get_date_time, db_name_validate
from vcli.util.static_params import (
    VAAS_MODULES,
    VALID_REPORT_NAME,
    VALID_REPORT_RANGE
)
from vcli.models.response_model import ResponseModel

# all post apis
from openapi_client.api.dc_graph_query_per_hour_v1_api import DcGraphQueryPerHourV1Api
from openapi_client.api.dc_graph_depot_utilization_v1_api import DcGraphDepotUtilizationV1Api
from openapi_client.api.dc_graph_query_response_distribution_v1_api import DcGraphQueryResponseDistributionV1Api
from openapi_client.api.dc_graph_total_queries_per_hr_v1_api import DcGraphTotalQueriesPerHrV1Api
from openapi_client.api.dc_graph_cpu_per_hour_by_node_v1_api import DcGraphCpuPerHourByNodeV1Api
from openapi_client.api.dc_graph_billing_summary_v1_api import DcGraphBillingSummaryV1Api
from openapi_client.api.dc_graph_billing_summary_total_v1_api import DcGraphBillingSummaryTotalV1Api
from openapi_client.api.dc_graph_memory_usage_v1_api import DcGraphMemoryUsageV1Api

# all get apis
from openapi_client.api.dc_graph_get_report_query_per_hour_v1_api import DcGraphGetReportQueryPerHourV1Api
from openapi_client.api.dc_graph_get_report_depot_utilization_v1_api import DcGraphGetReportDepotUtilizationV1Api
from openapi_client.api.dc_graph_get_report_query_response_distribution_v1_api import DcGraphGetReportQueryResponseDistributionV1Api
from openapi_client.api.dc_graph_get_report_total_queries_per_hr_v1_api import DcGraphGetReportTotalQueriesPerHrV1Api
from openapi_client.api.dc_graph_get_report_cpu_per_hour_by_node_v1_api import DcGraphGetReportCpuPerHourByNodeV1Api
from openapi_client.api.dc_graph_get_report_usage_by_time_range_v1_api import DcGraphGetReportUsageByTimeRangeV1Api
from openapi_client.api.dc_graph_get_report_all_usage_by_time_range_v1_api import DcGraphGetReportAllUsageByTimeRangeV1Api
from openapi_client.api.dc_graph_get_report_billing_summary_v1_api import DcGraphGetReportBillingSummaryV1Api
from openapi_client.api.dc_graph_get_report_billing_total_summary_v1_api import DcGraphGetReportBillingTotalSummaryV1Api
from openapi_client.api.dc_graph_get_report_billing_total_per_db_summary_v1_api import DcGraphGetReportBillingTotalPerDbSummaryV1Api
from openapi_client.api.dc_graph_get_report_memory_usage_v1_api import DcGraphGetReportMemoryUsageV1Api


class ReportCommand(SubCommandImplementation):
    def operation_define(self, subparsers) -> None:
        # Supported command line options:
        #   va report show --name dbname --subcluster_id vertica_cluster --report_name query_per_hour --range '1 hour'

        report_parser = subparsers.add_parser('report', help=HelpMessage.report_header)
        report_subparser = report_parser.add_subparsers()

        # show command
        report_show = report_subparser.add_parser('show', help=HelpMessage.report_show)
        report_show.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.report_show_name)
        report_show.add_argument('--subcluster_id', metavar='<value>', required=True, type=str, choices=VAAS_MODULES.list(), help=HelpMessage.report_show_module)
        report_show.add_argument('--report_name', metavar='<value>', required=True, type=str, choices=VALID_REPORT_NAME.list(), help=HelpMessage.report_show_report_name)
        report_show.add_argument('--range', metavar='<value>', required=False, type=str, default=VALID_REPORT_RANGE.ONE_MONTH.value, choices=VALID_REPORT_RANGE.list(), help=HelpMessage.report_show_range)
        report_show.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        report_show.set_defaults(func=self.operation_show)

        # generate command
        report_generate = report_subparser.add_parser('generate', help=HelpMessage.report_generate)
        report_generate.add_argument('--name', metavar='<value>', required=True, type=db_name_validate, help=HelpMessage.report_generate_name)
        report_generate.add_argument('--report_name', metavar='<value>', required=True, type=str, choices=VALID_REPORT_NAME.generate_list(), help=HelpMessage.report_generate_report_name)
        report_generate.add_argument('--profile', metavar='<value>', default=VCLI_CONFIG_DEFAULT, required=False, type=str, help=HelpMessage.profile)
        report_generate.set_defaults(func=self.operation_generate)

    def operation_cmd(self, args: Namespace) -> int:
        pass

    def operation_show(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)

        if args.report_name == VALID_REPORT_NAME.QUERY_PER_HOUR.value:
            result = DcGraphGetReportQueryPerHourV1Api(api_client=api_client).v1_vaas_reports_dbname_query_per_hour_get(
                dbname=args.name,
                module=args.subcluster_id,
                time_range=args.range
            )
        elif args.report_name == VALID_REPORT_NAME.DEPOT_UTILIZATION.value:
            result = DcGraphGetReportDepotUtilizationV1Api(api_client=api_client).v1_vaas_reports_dbname_depot_utilization_get(
                dbname=args.name,
                module=args.subcluster_id,
                time_range=args.range
            )
        elif args.report_name == VALID_REPORT_NAME.QUERY_RESPONSE_DISTRIBUTION.value:
            result = DcGraphGetReportQueryResponseDistributionV1Api(api_client=api_client).v1_vaas_reports_dbname_response_distribution_get(
                dbname=args.name,
                module=args.subcluster_id,
                time_range=args.range
            )
        elif args.report_name == VALID_REPORT_NAME.QUERY_PER_HOUR_TOP_5_USERS.value:
            result = DcGraphGetReportTotalQueriesPerHrV1Api(api_client=api_client).v1_vaas_reports_dbname_query_by_hour_top5_users_get(
                dbname=args.name,
                module=args.subcluster_id,
                time_range=args.range
            )
        elif args.report_name == VALID_REPORT_NAME.CPU_PER_HOUR_BY_NODE.value:
            result = DcGraphGetReportCpuPerHourByNodeV1Api(api_client=api_client).v1_vaas_reports_dbname_cpu_per_hour_by_node_get(
                dbname=args.name,
                module=args.subcluster_id,
                time_range=args.range
            )
        elif args.report_name == VALID_REPORT_NAME.CPU_BY_TIME_RANGE.value:
            # Convert time range into date-time format
            start_date_time, end_date_time = get_date_time(args.range)

            result = DcGraphGetReportUsageByTimeRangeV1Api(api_client=api_client).v1_vaas_reports_dbname_usage_by_time_range_get(
                dbname=args.name,
                end_dttm=end_date_time,
                start_dttm=start_date_time
            )
        elif args.report_name == VALID_REPORT_NAME.ALL_USAGE_BY_TIME_RANGE.value:
            # Convert time range into date-time format
            start_date_time, end_date_time = get_date_time(args.range)

            result = DcGraphGetReportAllUsageByTimeRangeV1Api(api_client=api_client).v1_vaas_reports_usage_by_time_range_get(
                end_dttm=end_date_time,
                start_dttm=start_date_time
            )
        elif args.report_name == VALID_REPORT_NAME.BILLING_SUMMARY.value:
            result = DcGraphGetReportBillingSummaryV1Api(api_client=api_client).v1_vaas_reports_dbname_billing_summary_get(
                dbname=args.name,
                module=args.subcluster_id,
                time_range=args.range
            )
        elif args.report_name == VALID_REPORT_NAME.BILLING_SUMMARY_TOTAL.value:
            result = DcGraphGetReportBillingTotalSummaryV1Api(api_client=api_client).v1_vaas_reports_billing_summary_total_get(
                dbname=args.name,
                time_range=args.range
            )
        elif args.report_name == VALID_REPORT_NAME.BILLING_SUMMARY_TOTAL_PER_DB.value:
            result = DcGraphGetReportBillingTotalPerDbSummaryV1Api(api_client=api_client).v1_vaas_reports_billing_summary_total_per_db_get(
                dbname=args.name,
                time_range=args.range
            )
        elif args.report_name == VALID_REPORT_NAME.MEMORY_USAGE.value:
            result = DcGraphGetReportMemoryUsageV1Api(api_client=api_client).v1_vaas_reports_dbname_memory_usage_get(
                dbname=args.name,
                module=args.subcluster_id,
                time_range=args.range
            )

        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)

    def operation_generate(self, args: Namespace) -> int:
        api_client = build_api_client(profile=args.profile)

        if args.report_name == VALID_REPORT_NAME.QUERY_PER_HOUR.value:
            result = DcGraphQueryPerHourV1Api(api_client=api_client).v1_vaas_reports_dbname_query_per_hour_post(dbname=args.name)
        elif args.report_name == VALID_REPORT_NAME.DEPOT_UTILIZATION.value:
            result = DcGraphDepotUtilizationV1Api(api_client=api_client).v1_vaas_reports_dbname_depot_utilization_post(dbname=args.name)
        elif args.report_name == VALID_REPORT_NAME.QUERY_RESPONSE_DISTRIBUTION.value:
            result = DcGraphQueryResponseDistributionV1Api(api_client=api_client).v1_vaas_reports_dbname_response_distribution_post(dbname=args.name)
        elif args.report_name == VALID_REPORT_NAME.QUERY_PER_HOUR_TOP_5_USERS.value:
            result = DcGraphTotalQueriesPerHrV1Api(api_client=api_client).v1_vaas_reports_dbname_query_by_hour_top5_users_post(dbname=args.name)
        elif args.report_name == VALID_REPORT_NAME.CPU_PER_HOUR_BY_NODE.value:
            result = DcGraphCpuPerHourByNodeV1Api(api_client=api_client).v1_vaas_reports_dbname_cpu_per_hour_by_node_post(dbname=args.name)
        elif args.report_name == VALID_REPORT_NAME.BILLING_SUMMARY.value:
            result = DcGraphBillingSummaryV1Api(api_client=api_client).v1_vaas_reports_dbname_billing_summary_post(dbname=args.name)
        elif args.report_name == VALID_REPORT_NAME.BILLING_SUMMARY_TOTAL.value:
            result = DcGraphBillingSummaryTotalV1Api(api_client=api_client).v1_vaas_reports_billing_summary_total_post()
        elif args.report_name == VALID_REPORT_NAME.MEMORY_USAGE.value:
            result = DcGraphMemoryUsageV1Api(api_client=api_client).v1_vaas_reports_dbname_memory_usage_post(dbname=args.name)

        output = ResponseModel(
            return_code=RETURN_CODE_SUCCESS,
            data=result.to_dict().get('data')
        )
        print(output)
