# https://hackersandslackers.com/python-poetry-package-manager/
import argparse
import sys
import os
import shutil
import json
import requests
import webbrowser
import subprocess
import boto3
from pathlib import Path
import base64

from http.server import HTTPServer, BaseHTTPRequestHandler

KEEP_RUNNING = True

def save_credential_secrets(info):
    root_path = os.path.join(Path.home(), '.entropy')
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    with open(f"{root_path}/user.conf", "w") as f:
        f.write(json.dumps(info))
    # this will make sure that user has logged in already
    print("credential secrets saved...")

class Serv(BaseHTTPRequestHandler):
    stopped = False
    def do_GET(self):
        print("do get????")
        if self.path == '/':
            print("ever in the path")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
            self.wfile.close()
        else:
            print("in other path")

    def do_OPTIONS(self):
        print("doing options")
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_data_json = json.loads(post_data)
        print(post_data_json)
        if "user_id" in post_data_json:
            print("login success")
            # save the user id to credential file
            info = {"user_id": post_data_json['user_id'],
                    "username": "username"}
            save_credential_secrets(info)
        print("going to send response")
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        success = {"success": True}
        self.wfile.write(b'{"ss":"sss"}')
        # stop the server
        global KEEP_RUNNING
        KEEP_RUNNING=False
        print("stop running temp server")

def do_login_with_web_portal():
    # redirect to page
    # localserver address
    PORT = 9200
    redirect = f"http://localhost:{PORT}"
    url_login = f"http://localhost:3000/cli-auth?redirect_url={redirect}"
    webbrowser.open(url_login, new = 2)
    # get access token and secret key ?
    httpd = HTTPServer(('localhost',PORT), Serv)
    while KEEP_RUNNING:
        httpd.handle_request()


def do_login(username, password):
    # post to the url
    print("do user login")
    data = {'username':username,
            'password':password}
    response = json.loads(requests.post(f"http://localhost:9100/api/auth/cli_login", data = json.dumps(data)).text)
    # this will return the user id
    # save the important information somewhere in the system
    if response['status'] == "success":
        info = {"user_id": response['user_id'],
                "username": username}
