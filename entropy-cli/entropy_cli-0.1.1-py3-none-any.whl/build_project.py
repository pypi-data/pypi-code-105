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

from entropy_cli.utils import load_user_credentials

REGION = "us-east-1"
ACCOUNT_ID = "603027427785"
AWS_ACCESS_KEY_ID="AKIAYYZZ4KHE4C74HC52"
AWS_SECRET_ACCESS_KEY = "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"

def get_boto3_session():
    #TODO: get a temparory access key and security token for the user
    BOTO3_SESSION = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION)
    return BOTO3_SESSION

def get_image_uri(repository_name):
    return f"{ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{repository_name}"

def tag_latest_uri(image_uri):
    return f"{image_uri}:latest"

def create_ecr_repository(ecr_client, function_id, company, team, user):
    response = ecr_client.create_repository(
        repositoryName=function_id,
        imageTagMutability="MUTABLE",
        tags=[
            {
                "Key": "company",
                "Value": company
            },
            {
                "Key": "team",
                "Value": team
            },
            {
                "Key": "user",
                "Value": user
            }
        ])
    print(response)
    code = int(response['ResponseMetadata']['HTTPStatusCode'])
    if (code == 200):
        return {
            "uri": response['repository']['repositoryUri'],
            'arn': response['repository']['repositoryArn']
        }
    else:
        raise Exception("Error creating repo")

def validate_project_folder():
    if not os.path.exists(".entropy_conf"):
        raise Exception("no conf file found for the current folder, cd to the correct project folder")
    if (not os.path.exists("requirements.txt")):
        raise Exception("Upload must contain requirements.txt")
    if (not os.path.exists("entropy_main.py")):
        raise Exception("Upload must contain entropy_main.py")

def build_and_push_image(entropy_conf, latest_image_uri):
    # invoke docker to build image
    subprocess.run([f"aws ecr get-login-password --region {REGION} | docker login --username AWS --password-stdin {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com"], shell=True)
    subprocess.run([f"docker build -t {entropy_conf['function_id']} ."], shell=True)
    subprocess.run([f"docker tag {entropy_conf['function_id']}:latest {latest_image_uri}"], shell=True)
    subprocess.run([f"docker push {latest_image_uri}"], shell=True)

def build_and_push_project():
    validate_project_folder()
    with open(".entropy_conf", "r") as f:
        entropy_conf = json.load(f)
    boto3_session = get_boto3_session()
    ecr_client = boto3_session.client('ecr')

    latest_image_uri = tag_latest_uri(get_image_uri(entropy_conf['function_id']))
    print(f"latest image url is {latest_image_uri}")

    create_ecr_repository(ecr_client, entropy_conf['function_id'], "test_company", "test_team", "test_user")
    build_and_push_image(entropy_conf, latest_image_uri)

    # send post request to the backend to create the lambda function from the image url
    # we define how to create the lambda and get the image
    user_info = load_user_credentials()
    data = {"user_id":user_info['user_id'],
            "function_id":entropy_conf['function_id'],
            "latest_image_uri":latest_image_uri}
    response = requests.post(f"http://localhost:9100/api/function/create_lambda", data = json.dumps(data))
    print(response)

    if response.status_code == 200:
        response = json.loads(response.text)
        print(response)
    else:
        print("encountered some errors")

def update_with_latest_image():
    validate_project_folder()
    with open(".entropy_conf", "r") as f:
        entropy_conf = json.load(f)
    boto3_session = get_boto3_session()
    ecr_client = boto3_session.client('ecr')

    latest_image_uri = tag_latest_uri(get_image_uri(entropy_conf['function_id']))
    print(f"latest image url is {latest_image_uri}")

    # invoke docker to build image
    build_and_push_image(entropy_conf, latest_image_uri)
    user_info = load_user_credentials()
    data = {"user_id":user_info['user_id'],
            "function_id":entropy_conf['function_id'],
            "latest_image_uri":latest_image_uri}
    response = requests.post(f"http://localhost:9100/api/function/update_lambda", data = json.dumps(data))
    print(response)
