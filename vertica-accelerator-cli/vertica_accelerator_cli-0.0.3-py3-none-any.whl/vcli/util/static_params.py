#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

from enum import Enum


# Ref: https://vertica.atlassian.net/wiki/spaces/VAAS/pages/346128488/Service+actions+static+params
class VAAS_MODULES(Enum):
    VERTICA_CLUSTER = 'vertica_cluster'
    VERTICA_SUBCLUSTER_1 = 'vertica_subcluster_1'
    VERTICA_SUBCLUSTER_2 = 'vertica_subcluster_2'
    VERTICA_SUBCLUSTER_3 = 'vertica_subcluster_3'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, VAAS_MODULES))

    @staticmethod
    def subcluster_list():
        sub_lst = []
        for i in VAAS_MODULES:
            if i.value != VAAS_MODULES.VERTICA_CLUSTER.value:
                sub_lst.append(i.value)
        return sub_lst


class AWS_INSTANCE_TYPES(Enum):
    I3_2XLARGE = 'i3.2xlarge'
    I3_4XLARGE = 'i3.4xlarge'
    I3_8XLARGE = 'i3.8xlarge'
    I3_16XLARGE = 'i3.16xlarge'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, AWS_INSTANCE_TYPES))


class SUPPORTED_VERTICA_VERSIONS(Enum):
    VERSION_10_1_0_1 = '10.1.0-1'
    VERSION_10_1_0_2 = '10.1.0-2'
    VERSION_11_0_0_1 = '11.0.0-1'
    # VERSION_11_0_1_2 = '11.0.1-2'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, SUPPORTED_VERTICA_VERSIONS))


class SUPPORTED_AWS_REGIONS(Enum):
    US_EAST_1 = 'us-east-1'
    US_EAST_2 = 'us-east-2'
    US_WEST_1 = 'us-west-1'
    US_WEST_2 = 'us-west-2'
    AP_EAST_1 = 'ap-east-1'
    AP_SOUTH_1 = 'ap-south-1'
    AP_NORTH_EAST_1 = 'ap-northeast-1'
    AP_NORTH_EAST_2 = 'ap-northeast-2'
    AP_SOUTH_EAST_1 = 'ap-southeast-1'
    AP_SOUTH_EAST_2 = 'ap-southeast-2'
    EU_CENTRAL_1 = 'eu-central-1'
    EU_WEST_1 = 'eu-west-1'
    EU_WEST_3 = 'eu-west-3'
    EU_SOUTH_1 = 'eu-south-1'
    ME_SOUTH_1 = 'me-south-1'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, SUPPORTED_AWS_REGIONS))


class SUPPORTED_AWS_ZONES(Enum):
    US_EAST_1_A = 'us-east-1a'
    US_EAST_1_B = 'us-east-1b'
    US_EAST_1_C = 'us-east-1c'
    US_EAST_1_D = 'us-east-1d'
    US_EAST_1_E = 'us-east-1e'
    US_EAST_1_F = 'us-east-1f'

    US_EAST_2_A = 'us-east-2a'
    US_EAST_2_B = 'us-east-2b'
    US_EAST_2_C = 'us-east-2c'

    US_WEST_1_A = 'us-west-1a'
    US_WEST_1_C = 'us-west-1c'

    US_WEST_2_A = 'us-west-2a'
    US_WEST_2_B = 'us-west-2b'
    US_WEST_2_C = 'us-west-2c'
    US_WEST_2_D = 'us-west-2d'

    AP_EAST_1_A = 'ap-east-1a'
    AP_EAST_1_B = 'ap-east-1b'
    AP_EAST_1_C = 'ap-east-1c'

    AP_NORTH_EAST_1_A = 'ap-northeast-1a'
    AP_NORTH_EAST_1_C = 'ap-northeast-1c'
    AP_NORTH_EAST_1_D = 'ap-northeast-1d'

    AP_NORTH_EAST_2_A = 'ap-northeast-2a'
    AP_NORTH_EAST_2_B = 'ap-northeast-2b'
    AP_NORTH_EAST_2_C = 'ap-northeast-2c'
    AP_NORTH_EAST_2_D = 'ap-northeast-2d'

    AP_SOUTH_1_A = 'ap-south-1a'
    AP_SOUTH_1_B = 'ap-south-1b'
    AP_SOUTH_1_C = 'ap-south-1c'

    AP_SOUTH_EAST_1_A = 'ap-southeast-1a'
    AP_SOUTH_EAST_1_B = 'ap-southeast-1b'
    AP_SOUTH_EAST_1_C = 'ap-southeast-1c'

    AP_SOUTH_EAST_2_A = 'ap-southeast-2a'
    AP_SOUTH_EAST_2_B = 'ap-southeast-2b'
    AP_SOUTH_EAST_2_C = 'ap-southeast-2c'

    EU_CENTRAL_1_A = 'eu-central-1a'
    EU_CENTRAL_1_B = 'eu-central-1b'
    EU_CENTRAL_1_C = 'eu-central-1c'

    EU_WEST_1_A = 'eu-west-1a'
    EU_WEST_1_B = 'eu-west-1b'
    EU_WEST_1_C = 'eu-west-1c'

    EU_WEST_3_A = 'eu-west-3a'
    EU_WEST_3_B = 'eu-west-3b'
    EU_WEST_3_C = 'eu-west-3c'

    EU_SOUTH_1_A = 'eu-south-1a'
    EU_SOUTH_1_B = 'eu-south-1b'
    EU_SOUTH_1_C = 'eu-south-1c'

    ME_SOUTH_1_A = 'me-south-1a'
    ME_SOUTH_1_B = 'me-south-1b'
    ME_SOUTH_1_C = 'me-south-1c'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, SUPPORTED_AWS_ZONES))


class VALID_NODES_NUMBERS(Enum):
    THREE = 3
    SIX = 6
    TWELVE = 12

    @staticmethod
    def list():
        return list(map(lambda t: t.value, VALID_NODES_NUMBERS))


class CRON_ACTION(Enum):
    START = 'start'
    STOP = 'stop'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, CRON_ACTION))


class TOGGLE_ACTION(Enum):
    ENABLE = 'enable'
    DISABLE = 'disable'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, TOGGLE_ACTION))


class VALID_REPORT_NAME(Enum):
    QUERY_PER_HOUR = 'query_per_hour'
    DEPOT_UTILIZATION = 'depot_utilization'
    QUERY_RESPONSE_DISTRIBUTION = 'query_response_distribution'
    QUERY_PER_HOUR_TOP_5_USERS = 'query_by_hour_top_5_users'
    CPU_PER_HOUR_BY_NODE = 'cpu_per_hour_by_node'
    CPU_BY_TIME_RANGE = 'cpu_by_time_range'
    BILLING_SUMMARY = 'billing_summary'
    BILLING_SUMMARY_TOTAL = 'billing_summary_total'
    BILLING_SUMMARY_TOTAL_PER_DB = 'billing_summary_total_per_db'
    MEMORY_USAGE = 'memory_usage'
    ALL_USAGE_BY_TIME_RANGE = 'all_usage_by_time_range'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, VALID_REPORT_NAME))

    @staticmethod
    def generate_list():
        gen_lst = []
        for i in VALID_REPORT_NAME:
            if i.value not in [
                VALID_REPORT_NAME.CPU_BY_TIME_RANGE.value,
                VALID_REPORT_NAME.BILLING_SUMMARY_TOTAL_PER_DB.value,
                VALID_REPORT_NAME.ALL_USAGE_BY_TIME_RANGE.value
            ]:
                gen_lst.append(i.value)
        return gen_lst


class VALID_REPORT_RANGE(Enum):
    THREE_MONTH = '3 months'
    ONE_MONTH = '1 month'
    ONE_WEEK = '1 week'
    ONE_DAY = '1 day'
    EIGHT_HOURS = '8 hours'
    ONE_HOUR = '1 hour'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, VALID_REPORT_RANGE))


class VALID_TASK(Enum):
    ALL = 'all'
    RUNNING = 'running'
    COMPLETED = 'completed'

    @staticmethod
    def list():
        return list(map(lambda t: t.value, VALID_TASK))


class IDLE_SHUTDOWN_TIME(Enum):
    MIN_15 = 15
    MIN_30 = 30
    MIN_45 = 45
    MIN_60 = 60

    @staticmethod
    def list():
        return list(map(lambda t: t.value, IDLE_SHUTDOWN_TIME))
