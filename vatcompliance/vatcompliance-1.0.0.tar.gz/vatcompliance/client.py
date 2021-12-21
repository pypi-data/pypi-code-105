import json
import vatcompliance
import requests
from urllib.parse import urlencode


class Client():
    """VatCompliance Python Client"""

    def __init__(self, api_key):
        self.params = None
        self.method = None
        self.url = None
        self.api_key = api_key
        self.session = requests.Session()

    def _post(self):
        response = requests.post(self.url, data=json.dumps(self.params), headers={'content-type': 'application/json'})
        return response.json()

    def _get(self):
        response = requests.get(self.url, headers={'content-type': 'application/json'})
        return response.json()

    def set_params(self, params, method, url):
        self.params = params
        self.method = method.upper()
        self.url = url + '/' + self.api_key

        if 'getParams' in self.params and self.method == 'POST':
            self.url = self.url + '?' + urlencode(self.params['getParams'])
            del self.params['getParams']

        if self.method == 'GET':
            self.url = self.url + '?' + urlencode(self.params)

        self.url = self.url.lower()

    def omp_feed(self, params):
        self.set_params(params, 'POST', vatcompliance.OMP_API_URL + '/omp/feed')
        return self._post()

    def omp_tax_rate(self, params):
        self.set_params(params, 'POST', vatcompliance.OMP_API_URL + '/omp/tax_rate')
        return self._post()

    def omp_report_create(self, params):
        self.set_params(params, 'POST', vatcompliance.OMP_API_URL + '/omp/report/create')
        return self._post()

    def omp_status(self, params):
        self.set_params(params, 'GET', vatcompliance.OMP_API_URL + '/omp/report/status')
        return self._get()

    def omp_get_report(self, params):
        self.set_params(params, 'GET', vatcompliance.OMP_API_URL + '/omp/report')
        return self._get()

    def omp_invoice(self, params):
        self.set_params(params, 'POST', vatcompliance.OMP_API_URL + '/omp/omp_invoice')
        return self._post()

    def merchant_send(self, params):
        self.set_params(params, 'POST', vatcompliance.MERCHANT_API_URL + '/1/send')
        return self._post()

    def merchant_tax_rate(self, params):
        self.set_params(params, 'POST', vatcompliance.MERCHANT_API_URL + '/1/tax_rate')
        return self._post()

    def merchant_vat_checker(self, params):
        self.set_params(params, 'POST',
                        vatcompliance.MERCHANT_API_URL + '/1/returns/declarations/check_users_vat_number')
        return self._post()
