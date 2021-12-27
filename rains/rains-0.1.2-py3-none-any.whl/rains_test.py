import requests

print(requests.post('http://127.0.0.1:3700/login', data={'username': 'admin', 'password': 'admin'}).headers)
