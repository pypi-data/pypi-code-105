# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Copyright (C) 2021, SirLez
#
# Welcome to ReCaptcha ByPasser V3!
# Please do not edit/change/stole anything!
# Special Thanks to Bovonos#3359 - Oustex#3860
# this generator designed to generate recaptcha for any anchor url
#
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# *                                                                                                       *
# *    Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except   *
# *    in compliance with the License. You may obtain a copy of the License at                            *
# *                                                                                                       *
# *    http://www.apache.org/licenses/LICENSE-2.0                                                         *
# *                                                                                                       *
# *    Unless required by applicable law or agreed to in writing, software distributed under the License  *
# *    is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express   *
# *    or implied. See the License for the specific language governing permissions and limitations under  *
# *    the License.                                                                                       *
# *                                                                                                       *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

import re
import os
import requests
from typing import Dict, Union

# from fake_useragent import UserAgent

from .exceptions import RecaptchaResponseNotFound, RecaptchaTokenNotFound
from .utils import BASE_API, BASE_HEADERS, POST_DATA
from . import utils


def request(endpoint: str, data: Union[str, Dict] = None, params: str = None, header: dict = None, proxies: dict = None) -> requests.Response:
    if not header:
        header = BASE_HEADERS
    # header["user-agent"] = UserAgent().random
    header["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    if data:
        response = requests.post(f"{BASE_API.format(endpoint)}", data=data, params=params, headers=header, proxies=proxies)
    else:
        response = requests.get(f"{BASE_API.format(endpoint)}", params=params, headers=header, proxies=proxies)

    return response


class ReCaptcha:
    def __init__(self, anchor: str, proxies: dict = None):
        self.proxies = proxies
        self.anchor = anchor

    def generate_captcha(self, isBGD: bool = False) -> str:
        try:
            with open("token.txt", "r") as file:
                utils.TOKEN = file.read()
        except FileNotFoundError:
            with open("token.txt", "w") as file:
                utils.TOKEN = self.generate_token()
                file.write(utils.TOKEN)

        data = self.generate_data()
        endpoint = data["endpoint"]
        params = dict(pair.split('=') for pair in data['params'].split('&'))
        data = POST_DATA.format(params["v"], utils.TOKEN, params["k"], params["co"])
        response = request(f"{endpoint}/reload", data=data, params=f"k={params['k']}", proxies=self.proxies)

        if isBGD:
            results = re.findall(r'],"(.*?)",null', response.text)
        else:
            results = re.findall(r'"rresp","(.*?)"', response.text)

        if not results:
            raise RecaptchaResponseNotFound()

        return results[0]

    def generate_token(self) -> str:
        data = self.generate_data()
        params = data["params"]
        endpoint = data["endpoint"]

        response = request(f"{endpoint}/anchor", params=params, proxies=self.proxies)
        results = re.findall(r'"recaptcha-token" value="(.*?)"', response.text)

        if not results:
            raise RecaptchaTokenNotFound()

        return results[0]

    def generate_data(self) -> dict:
        regex = "(?P<endpoint>[api2|enterprise]+)\/anchor\?(?P<params>.*)"
        for match in re.finditer(regex, self.anchor):
            return match.groupdict()

    def regenerate_token(self):
        os.remove("token.txt")
        with open("token.txt", "w") as file:
            file.write(self.generate_token())
