#!/usr/bin/env python

import argparse
from io import StringIO
import json
import os
import os.path

import requests
from yaml import safe_load

parser = argparse.ArgumentParser(description="Motivus cluster CLI utility")
parser.add_argument('command', choices=["build", "push", "clean"])
parser.add_argument(
    '--config-file', help="yaml configuration file location", default="./motivus.yml")
parser.add_argument(
    '--build-dir', help="directory to look for package bundle", default="./build")
parser.add_argument(
    '-D', help="development mode", action='store_true', default=False)
args = parser.parse_args()

base_url = "http://localhost:4000/api/package_registry/algorithms/" if args.D else "https://marketplace.api.motivus.cl/api/package_registry/algorithms/" 

def main():
    with open(args.config_file, 'r') as f:
        config = safe_load(f)

    if args.command == "push":
        algorithm_res = requests.get(
            base_url, params={'name': config["package"]["name"]})
        if (len(algorithm_res.json()["data"]) == 1):
            algorithm_id = algorithm_res.json()["data"][0]["id"]

            package_filename = f'{config["package"]["name"]}-{config["package"]["version"]}.zip'
            package_location = os.path.join(args.build_dir, package_filename)
            version = {
                'name': config["package"]["version"],
                'metadata': config["package"]["metadata"]
            }
            with open(package_location, 'rb') as f:

                json_string = StringIO(json.dumps(version))
                files = {"version": (None, json_string, "application/json"),
                         "package": (package_filename, f, "application/octet-stream")}
                resp = requests.post(
                    f'{base_url}{algorithm_id}/versions', files=files)
                try:
                    res_json = resp.json()
                    data = res_json.get("data", None)
                    errors = res_json.get("errors", None)
                    if data:
                        if data.get("id", None):
                            print(
                                f'{config["package"]["name"]}-{config["package"]["version"]}')
                        else:
                            raise Exception("could not push version")
                    elif errors:
                        if errors.get("name", None):
                            raise Exception(
                                f'this version name {errors.get("name", None)[0]}')
                        else:
                            raise Exception(
                                f'could not push version: {errors}')
                    else:
                        raise Exception(f'could not push version: {errors}')

                except Exception as e:
                    raise e
        else:
            raise Exception(
                f'algorithm not found: {config["package"]["name"]}')

    def run_docker(command=""):
        image = 'motivus/packager-emscripten:0.2.0'
        docker_args = 'docker run -ti --rm  -v $(pwd):/src  -u $(id -u):$(id -g)'

        env = {
            'SOURCE_DIR': config["build"]["source"],
            'BUILD_DIR': args.build_dir,
            'FILESYSTEM_DIR': config["build"]["filesystem"],
            'PACKAGE_NAME': config["package"]["name"],
            'PACKAGE_VERSION': config["package"]["version"],
        }
        env_vars = []
        for k, v in env.items():
            env_vars.append(f'-e {k}={v}')
        os.system(" ".join([docker_args, " ".join(env_vars), image, command]))

    if args.command == "build":
        run_docker()

    if args.command == "clean":
        run_docker("make clean")
