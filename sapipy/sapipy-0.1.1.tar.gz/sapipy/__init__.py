"""Solar Analytics API"""
from datetime import datetime
import logging

import requests as r

__version__ = "0.1.1"
__author__ = "aws404"

_LOGGER = logging.getLogger(__name__)
_BASE_URL = "https://portal.solaranalytics.com.au/api/"


class SolarAnalyticsApiConnection:
    """Represents an authenticable connection used to send requests to the Solar Analytics API."""

    email: str = None
    password: str = None
    token: str = None
    token_expires = datetime.now()

    def __init__(self, email: str, password: str, auto_auth: bool = False) -> None:
        self.email = email
        self.password = password
        if auto_auth:
            self.authenticate()

    def authenticate(self) -> bool:
        """Check the current authentication token status, and get a new token if required."""
        if self.is_authenticated():
            return True

        response = r.get(
            _BASE_URL + "v3/token",
            auth=(self.email, self.password),
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data["token"]
            self.token_expires = datetime.fromisoformat(data["expires"])
            _LOGGER.info(
                "Solar Analytics authenticated with token %s until %s. (%s seconds remaining)",
                self.token,
                self.token_expires,
                data["duration"],
            )
            return True

        return False

    def is_authenticated(self) -> bool:
        """Check if the current authentication token is still valid."""
        return self.token != None and self.token_expires.timestamp() >= datetime.now().timestamp()

    def site_list(
        self,
        reseller: bool = False,
        address: bool = False,
        timezone: bool = True,
        postcode: bool = False,
        state: bool = False,
        country: bool = False,
        capacity: bool = True,
        subscription: bool = False,
        account: bool = True,
        hardware: bool = True,
    ) -> dict:
        """Make a site list request to the API."""
        return self._make_request(
            url="v3/site_list",
            params={
                "reseller": reseller,
                "address": address,
                "timezone": timezone,
                "postcode": postcode,
                "state": state,
                "country": country,
                "capacity": capacity,
                "subscription": subscription,
                "account": account,
                "hardware": hardware,
            },
        )

    def site_data(
        self,
        site_id: int,
        tstart: str,
        tend: str,
        gran: str = "hour",
        raw: bool = True,
        trunc: bool = True,
    ) -> dict:
        """Make a site data request to the API."""
        return self._make_request(
            f"v2/site_data/{site_id}",
            params={
                "tstart": tstart,
                "tend": tend,
                "gran": gran,
                "raw": raw,
                "trunc": trunc,
            },
        )

    def site_status(
        self, 
        site_id: int, 
        start_date: str, 
        end_date: str,
        unresolved: bool = True,
        resolved: bool = False,
        average: bool = False,
        all: bool = True,
    ) -> dict:
        """Make a site status request to the API."""
        return self._make_request(
            f"v3/site_status/{site_id}",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "unresolved": unresolved,
                "resolved": resolved,
                "average": average,
                "all": all
            }
        )

    def site_monitors(
        self,
        site_id: int,
    ) -> list:
        """Request a list of all the monitor names for the specified site."""
        data = self._make_request(
            "v2/site_data/" + str(site_id),
            params={
                "tstart": 19000101,
                "tend": 19000101,
                "gran": "year",
                "raw": True,
                "trunc": False,
            },
        )

        monitors = []
        for circuit in data["data"]:
            monitors.append(circuit["monitors"])

        return monitors

    def _make_request(self, url: str, params) -> dict:
        """Make a request to the API.
        This method will ensure the instance is authenticated and will handle error codes.
        The parsed JSON response is returned."""
        if not self.authenticate():
            _LOGGER.error(
                "Tried to make an unuthenticated request to the API (could not get token), aborting.",
            )
            return {"status_code": 401}

        response = r.get(
            _BASE_URL + url,
            params,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        if response.status_code != 200:
            if response.status_code == 429:
                _LOGGER.error(
                    "API returned code %s (too many requests). You may be importing data from too may sites, try reducing your imported site count",
                    response.status_code,
                )
            elif response.status_code == 401:
                _LOGGER.error(
                    "API returned code %s (unauthorised access). Have you changed your Solar Analytics credentials?",
                    response.status_code,
                )
            else:
                _LOGGER.error("API returned code %s", response.status_code)

            return {"status_code": response.status_code}

        return response.json()
