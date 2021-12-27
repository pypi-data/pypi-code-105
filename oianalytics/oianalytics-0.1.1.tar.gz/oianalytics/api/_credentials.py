# Imports
import os


# Exceptions
class EnvironmentSetupError(Exception):
    """Raised when environment variables are not properly set"""


# Base class for credentials
class OIAnalyticsAPICredentials:
    _BASE_URL_ENV_KEY = "OIANALYTICS_API_BASE_URL"
    _LOGIN_ENV_KEY = "OIANALYTICS_API_LOGIN"
    _PWD_ENV_KEY = "OIANALYTICS_API_PWD"

    def __init__(self, base_url: str, login: str, pwd: str):
        self.base_url = base_url.strip("/")
        self.login = login
        self.pwd = pwd

    def __repr__(self):
        return f"Base URL: {self.base_url}\nLogin: {self.login}\nPassword: {self.pwd}"

    @classmethod
    def get_from_environment(cls):
        base_url = os.environ.get(cls._BASE_URL_ENV_KEY)
        login = os.environ.get(cls._LOGIN_ENV_KEY)
        pwd = os.environ.get(cls._PWD_ENV_KEY)
        if base_url is None or login is None or pwd is None:
            raise EnvironmentSetupError(
                "OIAnalytics default credentials have not been proprely set using set_default_oianalytics_credentials"
            )
        return cls(base_url=base_url, login=login, pwd=pwd)

    def set_as_default_credentials(self):
        os.environ[self._BASE_URL_ENV_KEY] = self.base_url
        os.environ[self._LOGIN_ENV_KEY] = self.login
        os.environ[self._PWD_ENV_KEY] = self.pwd


# Default crendentials management
def set_default_oianalytics_credentials(base_url: str, login: str, pwd: str):
    OIAnalyticsAPICredentials(
        base_url=base_url, login=login, pwd=pwd
    ).set_as_default_credentials()


def get_default_oianalytics_credentials():
    return OIAnalyticsAPICredentials.get_from_environment()
