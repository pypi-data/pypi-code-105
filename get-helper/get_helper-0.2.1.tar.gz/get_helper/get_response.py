from random import choice
import requests
import time
from requests.adapters import HTTPAdapter


class get_helper:
    def __init__(self, app):
        self.app = app
        self.proxies_list = []
        if self.app.config['proxy']['enable_proxy']:
            try:
                with open(self.app.config['proxy']['path'], 'r', encoding='utf-8-sig', newline='') as f:
                    self.proxies_list = [proxy for proxy in f]
            except Exception as e:
                print("not found file with proxies")
                self.app.log_error.error(e, exc_info=True)

    def run(self, url, cookie=None, method='GET', data=None):
        headers = self.app.config['get']['headers']
        headers['user-agent'] = choice(self.app.ua_list)
        proxy = None
        proxies = None
        if self.app.config['proxy']['enable_proxy']:
            for i in range(len(self.proxies_list)):
                if self.proxies_list[i] not in self.app.using_proxies:
                    proxy = self.proxies_list[i]
                    self.app.using_proxies.append(proxy)
                    break
            if self.app.config['proxy']['proxy_autentification']:
                if proxy:
                    proxies = {'https': f"https://{self.app.config['proxy']['login']}:{self.app.config['proxy']['password']}@{proxy}"}
            else:
                if proxy:
                    proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
            if proxies is None:
                print("There are no free proxies")
        r = None
        status_code = 0
        attempt = 1
        limit = 3
        adapter = HTTPAdapter(max_retries=1)
        s = requests.Session()
        s.mount(self.app.config['host'], adapter)
        while attempt < limit:
            try:
                if method == 'GET':
                    r = s.get(url=url, proxies=proxies, headers=headers, timeout=30, cookies=cookie)
                else:
                    r = s.post(url=url, proxies=proxies, headers=headers, timeout=30, cookies=cookie, data=data)
                status_code = r.status_code
                if self.app.config['proxy']['enable_proxy']:
                    print("Status code:", status_code, "Proxy:", proxy)
                else:
                    print("Status code:", status_code, "no proxy")
                break
            except Exception as e:
                self.app.log_error.error(e, exc_info=True)
                print('not connected, there are only', limit - attempt, 'attempts')
                attempt += 1
                time.sleep(2)
        try:
            if self.app.config['proxy']['enable_proxy']:
                self.app.using_proxies.remove(proxy)
        except Exception as e:
            self.app.log_error.error(e, exc_info=True)
        return r, status_code
