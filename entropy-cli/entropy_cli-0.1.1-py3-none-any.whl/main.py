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

from entropy_cli.sample_files import ENTROPY_MAIN, DOCKER_CONTENT
from entropy_cli.build_project import build_and_push_project, update_with_latest_image
from entropy_cli.utils import load_user_credentials
from entropy_cli.local_test import run_local_test
from entropy_cli.login import do_login_with_web_portal, do_login

def fetch_function_details(function_id):
    # post to the url
    print("fetching function information")
    # try to load username
    user_info = load_user_credentials()
    data = {"user_id":user_info['user_id'],
            "function_id":function_id}
    response = json.loads(requests.post(f"http://localhost:9100/api/function/detail/get", data = json.dumps(data)).text)
    return response

def init_dev_environment(project_name, function_id):
    print(f"initializing project {project_name}:{function_id}")
    # initialize the dev env
    function_detail = fetch_function_details(function_id)
    if function_detail['status']!="success":
        print("wrong project id ")
        return

    if os.path.exists(project_name):
        print("project already exists")
        return
    os.mkdir(project_name)
    # also initialize the required files
    # make requirement file
    with open(f"{project_name}/requirements.txt", "w") as f:
        f.write("")
        f.close()
    # write the function file
    with open(f"{project_name}/entropy_main.py", "w") as f:
        f.write(ENTROPY_MAIN)
        f.close()
    with open(f"{project_name}/Dockerfile", "w") as f:
        f.write(DOCKER_CONTENT)
        f.close()

    # build some hidden files to store the function related meta information
    # fetch the function_id --> we have the user_id, access_token, get the function_id
    # fetch the function_details, function params
    with open(f"{project_name}/.entropy_conf", "w") as f:
        conf = {"project_name":project_name,
                "function_id": function_id,
                "function_detail":function_detail}
        f.write(json.dumps(conf))
        f.close()


def main(command_line=None):
    # base parser
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    login = subparser.add_parser('login')
    login.add_argument('-u', '--username', type=str, required=False)
    login.add_argument('-p', '--password', type=str, required=False)

    init = subparser.add_parser('init')
    init.add_argument('-p', '--project', type=str, required=True)
    init.add_argument('-d', '--function-id', type=str, required=True)

    local_test = subparser.add_parser('test')
    local_test.add_argument('--debug', type=str, default=False, required=False)

    deploy = subparser.add_parser('deploy')
    deploy.add_argument('--debug', type=str, default=False, required=False)
    deploy.add_argument('--update', action='store_true')

    args = parser.parse_args()
    if args.command == 'login':
        print('Logging in with username:', args.username,'and password:', args.password)
        # get the user name and last name
        if args.username and args.password:
            do_login(args.username, args.password)
        else:
            do_login_with_web_portal()

    elif args.command == 'init':
        print("initializing the local env")
        init_dev_environment(args.project, args.function_id)
    elif args.command == 'test':
        print("initializing the local test")
        run_local_test()
    elif args.command == 'deploy':
        print("build and deploy to entropy")
        if args.update:
            print("update current image...")
            update_with_latest_image()
        else:
            build_and_push_project()



if __name__ == '__main__':
    main()
