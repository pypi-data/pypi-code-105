#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

from environs import Env
from os.path import expanduser

env = Env()

VCLI_CONFIG_PATH = env("VCLI_CONFIG_PATH", f"{expanduser('~')}/.vcli")
VCLI_CONFIG_FILE = env("VCLI_CONFIG_FILE", "config")
VCLI_CREDENTIAL_FILE = env("VCLI_CREDENTIAL_FILE", "credentials")
REDIRECT_URL_CONSTANT = env("REDIRECT_URL_CONSTANT", "implicit/callback")
OA_SERVICE_PROXY_SURFFIX = env("OA_SERVICE_PROXY_SURFFIX", "api/oa")
VCLI_CONFIG_DEFAULT = "default"

LOG_LEVEL = env("LOG_LEVEL", "info")
LOG_FILE = env("LOG_FILE", expanduser("~") + '/.vcli/vcli.log')

MAX_ATTEMPTS_DEFAULT = 3

VCLI_USER = env("VCLI_USER", "")
VCLI_PASSWORD = env("VCLI_PASSWORD", "")

DB_ACTION_START = 'start'
DB_ACTION_STOP = 'stop'

MIN_DB_NAME_LENGTH = 1
MAX_DB_NAME_LENGTH = 18

MIN_DNS_NAME_LENGTH = 3
MAX_DNS_NAME_LENGTH = 18

MAX_CRON_NAME_LENGTH = 8

RETURN_CODE_SUCCESS = 0
RETURN_CODE_ERROR = 1
RETURN_CODE_UNKNOWN = 255
