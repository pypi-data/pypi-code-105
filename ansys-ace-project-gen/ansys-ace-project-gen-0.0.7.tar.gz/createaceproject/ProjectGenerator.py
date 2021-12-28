# Copyright (c) 2022 Ansys, Inc. and its affiliates. Unauthorised use, distribution or duplication is prohibited
# LICENSE file is in the root directory of this source tree.
import os
import subprocess
import shutil
from easygui import *


def hasPipx():
    try:
        subprocess.run(["pipx", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False


def get_templates(templates_directory):
    templates = None

    if not os.path.isdir(templates_directory):
        raise Exception('templates directory not found')
    else:
        templates = os.listdir(templates_directory)
    return [x for x in templates if x != 'shared' and not x.startswith('.') and not x.startswith('README')]


def copy_template(templates_directory, template, destination):
    # Copy shared resources
    shared_directory = os.path.join(templates_directory, 'shared')
    shutil.copytree(shared_directory, destination, dirs_exist_ok=True)

    # Copy template resources
    template_directory = os.path.join(templates_directory, template)
    shutil.copytree(template_directory, destination, dirs_exist_ok=True)


def generate_project_folder(root_directory, project_name=None, user_template=None):
    templates_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../templates')
    available_templates = get_templates(templates_dir)

    if not project_name:
        project_name = enterbox("Project Name", "Ansys ACE Project Generator", "What should we name your project ?")

    destination_directory = os.path.join(root_directory, project_name)
    if os.path.isdir(destination_directory):
        exit(1)

    if not user_template:
        exit(1)
    if user_template in available_templates:
        copy_template(templates_dir, user_template, destination_directory)