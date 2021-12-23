import requests
import backoff
import base64
import json

from typing import Callable, Dict, List, Optional, cast, Union

from .const import PINTEREST_SERVER_URL
from .exceptions import PinterestAccountLostAccessException

API_VERSION = 'v4'

class PinterestClient:
    def __init__(self, pinterest_credentials_path: str, _adscale_log: Optional[Callable] = None) -> None:
        with open(pinterest_credentials_path) as credentials:
            pinterest_credentials = json.load(credentials)
            pinterest_credentials = cast(Dict[str, str], pinterest_credentials)
        self._app_id = pinterest_credentials.get('app_id'),
        self._app_secret = pinterest_credentials.get('app_secret'),
        self._token = pinterest_credentials.get('access_token')
        # To get owner user id, you should go to Pinterest > Business Access > Select Arcane - The Feed Agency > Employee > Select the employee (ie: reporting@arcane.run (production) or pierre@arcane.run(staging))
        # > Get the last id in url: pinterest.fr/business/business-access/{business_id}/employees/{owner_user_id}/details/
        self._owner_user_id = pinterest_credentials.get('owner_user_id')
        if _adscale_log:
            self.log = _adscale_log
        else:
            self.log = print


    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=5)
    def _make_request(self, endpoint: str, method: str, params: Dict = None, headers: Dict = None, **kwargs) -> Dict:
        """Send a request to Pinterest API"""
        if headers == None:
            headers={'Authorization': f'Bearer {self._token}'}
        response = requests.request(method=method, url=f"{PINTEREST_SERVER_URL}{endpoint}", headers=headers, params=params, **kwargs)
        response.raise_for_status()
        response = response.json()
        response_temp = response
        while 'bookmark' in response_temp:
            if params is None:
                params = {
                    'bookmark' : response_temp['bookmark']
                }
            else:
                params['bookmark'] = response_temp['bookmark']
            response_temp = requests.request(method=method, url=f"{PINTEREST_SERVER_URL}{endpoint}", headers=headers, params=params, **kwargs)
            response_temp.raise_for_status()
            response_temp = response_temp.json()
            response['data'] += response_temp['data']

        return response

    def get_advertiser_campaigns(self, advertiser_id: str) -> List[Dict[str, str]]:
        """Get advertiser campaigns given its ID."""
        try:
            response = self._make_request(
                f'/ads/{API_VERSION}/advertisers/{advertiser_id}/campaigns/',
                'GET'
                )
        except requests.exceptions.HTTPError as e:
            error_code = e.response.status_code
            if error_code in [401, 403]:
                raise PinterestAccountLostAccessException(f"We cannot access your pinterest account with the id: {advertiser_id}. Are you sure you granted access?")
            if error_code == 404:
                raise PinterestAccountLostAccessException(f"We cannot find this account with the id: {advertiser_id}. Are you sure you entered the correct id?")
            raise
        return [{
            'id': campaign.get('id'),
            'name': campaign.get('name'),
            'status': campaign.get('status')
        } for campaign in response['data']]

    def check_access_account(self, advertiser_id: str) -> None:
        """Check access by getting advertiser campaigns given its ID."""
        self.get_advertiser_campaigns(advertiser_id)

    def _get_all_advertisers(self) -> Dict:
        params = {
            'owner_user_id': self._owner_user_id,
            'include_acl': True
        }
        response = self._make_request(
                f'/ads/{API_VERSION}/advertisers/',
                'GET',
                params
                )
        return response['data']

    def get_advertiser_currency_code(self, advertiser_id: str) -> str:
        all_advertisers = self._get_all_advertisers()
        try:
            advertiser = next(advertiser for advertiser in all_advertisers if advertiser.get('id') == advertiser_id)
        except StopIteration:
            raise ValueError(f"Pinterest incorrest reponse: No advertiser with id: {advertiser_id}")
        return advertiser['currency']

    def get_advertiser_name(self, advertiser_id: str) -> str:
        all_advertisers = self._get_all_advertisers()
        try:
            advertiser = next(advertiser for advertiser in all_advertisers if advertiser.get('id') == advertiser_id)
        except StopIteration:
            raise ValueError(f"Pinterest incorrest reponse: No advertiser with id: {advertiser_id}")
        return advertiser['name']

    def post_advertiser_metrics_report(
        self,
        advertiser_id: str,
        start_date: str,
        end_date: str,
        columns: Optional[List[str]] = None,
        level: str = 'CAMPAIGN',
        granularity: str = 'DAY'
    ) -> Dict:
        """Calling https://developers.pinterest.com/docs/redoc/combined_reporting_ads_v4/#operation/create_async_delivery_metrics_handler

        Args:
            advertiser_id (str): The advertiser id
            start_date (str): Report start date (UTC): YYYY-MM-DD. Start date and end date must be within 30 days of each other.
            end_date (str): Report end date (UTC): YYYY-MM-DD
            columns (Optional[List[str]]): Metrics that you want to have in the report
            level (str, optional): Requested report type. Defaults to 'CAMPAIGN'.
            granularity (str, optional): the scale to aggregate metrics
        Returns:
            Dict: A token you can use to download the report once it is ready.
        """
        json_params: Dict[str, Union[str, List[str]]] = {
            'start_date': start_date,
            'end_date': end_date,
            'level': level,
            'granularity': granularity
        }

        if columns:
            json_params['columns'] =  columns

        return self._make_request(
                f'/ads/{API_VERSION}/advertisers/{advertiser_id}/delivery_metrics/async/',
                'POST',
                json=json_params
                )

    def get_campaign_metrics(self, advertiser_id: str, token: str) -> Dict:
        """Calling https://developers.pinterest.com/docs/redoc/combined_reporting_ads_v4/#operation/get_async_delivery_metrics_handler

        Args:
            advertiser_id (str): The advertiser id
            token (str): Token returned from post_advertiser_metrics_report

        Returns:
            Dict: Dict with the delivery metrics report url if ready
        """
        params = {
            'token': token
        }
        return self._make_request(
                f'/ads/{API_VERSION}/advertisers/{advertiser_id}/delivery_metrics/async/',
                'GET',
                params=params
                )

    def get_new_access_token(self, code: str) -> str:
        """Get the acccess token for Pinterest API

        This function is composed of two step:

        #1: Get the pinterest APP_ID (Directly from pinterest website or from pinterest credentials)
            Manually visit https://www.pinterest.com/oauth/?client_id=<APP_ID>&redirect_uri=https://app.arcane.run/&response_type=code.
            You will be redirect to a pinterest dialog where you should login and then authorize the app.
            Once the app is authorized, you will be redirect to AMS with a params named code in the url. Get the value, it will be the arg needed in this function.

        #2: Initiate the pinterest client. Then call this function with the code and you will get in response the new access token.
            With this new access token, you can update the credentials.

        For more information, please refers to: https://developers.pinterest.com/docs/redoc/combined_reporting/#section/User-Authorization

        Args:
            code (str): This is the code you must use to get the access token.

        Returns:
            str: The new access token
        """
        # Second step:
        # Should be used as it is more secured but was not working. Check the comment below to find another method
        client_information_encoded = base64.b64encode(f'{self._app_id}:{self._app_secret}'.encode()).decode('utf-8')
        reponse = self._make_request(
            '/v3/oauth/access_token/',
            'PUT',
            data={'code': code, 'redirect_uri': 'https://app.arcane.run/', 'grant_type': 'authorization_code'},
            headers={'Authorization': f"Basic {client_information_encoded}"}
            )
        return reponse['data']['access_token']

        #### Not secured:
        # response = requests.request(
        #     method='PUT',
        #     url=f"{PINTEREST_SERVER_URL}{'/v3/oauth/access_token'}",
        #     data={'code': code, 'redirect_uri': 'https://app.arcane.run/', 'grant_type': 'authorization_code', 'client_id': self._app_id, 'client_secret': self._app_secret}
        # )

        # response = response.json()

        # return response['data']['access_token']
