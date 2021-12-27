"""DNS Authenticator for Innovativity DNS Manager."""
import logging
from json import JSONDecodeError
from typing import Callable
from typing import Dict
from typing import Optional

import requests
from certbot import errors
from certbot.plugins import dns_common
from certbot.plugins.dns_common import CredentialsConfiguration

logger = logging.getLogger(__name__)


class Authenticator(dns_common.DNSAuthenticator):
    """
    DNS Authenticator for Innovativity DNS Manager

    This Authenticator uses the Innovativity DNS Manager API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record using the DNS Manager module for Innovativity Dashboards."
    ttl = 120

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None
        self._record_id = None

    @classmethod
    def add_parser_arguments(
        cls, add: Callable[..., None], default_propagation_seconds: int = 10
    ) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="Innovativity DNS Manager credentials INI file.")

    def more_info(self) -> str:
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using the "
            "Innovativity DNS Manager API."
        )

    def _validate_credentials(self, credentials: CredentialsConfiguration) -> None:
        token = credentials.conf("api-token")
        base_url = credentials.conf("dashboard-url")
        if not token or not base_url:
            raise errors.PluginError(
                "{}: dns_innovativity_dashboard_url and dns_innovativity_token are required".format(
                    credentials.confobj.filename
                )
            )

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            "credentials",
            "Innovativity DNS Manager credentials INI file",
            None,
            self._validate_credentials,
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        url, headers = self._get_innovativity_request_config()
        data = {
            "record_name": validation_name,
            "record_content": validation,
        }
        logger.debug("Attempting to add TXT record: POST {} {}".format(url, data))
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            try:
                raise errors.PluginError("Could not create TXT record: {}".format(response.json()['details']))
            except (JSONDecodeError, KeyError):
                raise errors.PluginError("Could not create TXT record: {}".format(response.content))

        self._record_id = response.json()['record_id']
        logger.debug("Successfully added TXT record with ID {}".format(self._record_id))

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        # skip if record has not been created
        if not self._record_id:
            return

        url, headers = self._get_innovativity_request_config()
        data = {
            "record_id": self._record_id,
        }
        logger.debug("Attempting to delete TXT record: DELETE {} {}".format(url, data))
        response = requests.delete(url, headers=headers, json=data)
        if response.status_code != 200:
            try:
                logging.warning("Could not delete TXT record: {}".format(response.json()['details']))
            except (JSONDecodeError, KeyError):
                logging.warning("Could not delete TXT record: {}".format(response.content))

        else:
            logger.debug("Successfully deleted TXT record with ID {}".format(self._record_id))

    def _get_innovativity_request_config(self) -> (str, Dict[str, str]):
        base_url = self.credentials.conf("dashboard-url")
        if not base_url.endswith('/'):
            base_url += '/'

        token = self.credentials.conf("api-token")
        return "{}api/dns/certbot/".format(base_url), {"Authorization": "Bearer {}".format(token)}
