"""A set of tools for manipulating project toml files"""
import glob
import os
import os.path
import subprocess
import sys
from datetime import datetime
from functools import lru_cache
from os.path import abspath, dirname
# import awswrangler as wr
from typing import Dict

import findspark
import tomlkit


REQUIRED_PARAM = ["s3-staging-dir", "cluster-name", "stage", "region"]
DEFAULT_TOML_PATH = "./pyproject.toml"

DEFAULT_CONFIG_TEMPLATE = {
    "cluster-name": "EDA",
    "s3-staging-dir": "s3://<bucket-name>/<your-staging-directory>",
    "stage": "dev",
    "date-time": "%Y-%m-%dT%H-%M-%S",
    "region": "eu-west-1",
    "s3_patch_dir": "./data/mock/s3",
    "spark_version": "2.4.5",
}

DEFAULT_DEPENDENCIES = dict(
    Cython="0.29.24",
    pybind11="1.0.0",
    pythran="0.10.0",
    scipy="^1.2.0",
    Pillow="6.2.0",
    koalas="^1.8.2",
)

GIT_IGNORE_PATTERNS = [
    ".DS_Store",
    "**/.DS_Store",
    ".docker_venv",
    "**/docker_venv",
    ".Rhistory",
    ".ipynb_checkpoints",
    "**/.ipynb_checkpoints"
]

SIMPLE_KOALAS_EXAMPLE = """
import sys
import pandas as pd
import numpy as np
import databricks.koalas as ks
from pyspark.sql import SparkSession

kdf = ks.DataFrame(
{'a': [1, 2, 3, 4, 5, 6],
 'b': [100, 200, 300, 400, 500, 600],
 'c': ["one", "two", "three", "four", "five", "six"]},
index=[10, 20, 30, 40, 50, 60])

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

""".strip()

MAC_SPARK_DIR = "/usr/local/Cellar/apache-spark"

STDOUT_COLORS = dict(
    HEADER="\033[95m",
    OKBLUE="\033[94m",
    OKCYAN="\033[96m",
    OKGREEN="\033[92m",
    WARNING="\033[93m",
    FAIL="\033[91m",
    ENDC="\033[0m",
    BOLD="\033[1m",
    UNDERLINE="\033[4m",
)


def get_package_dir():
    """Returns pyemr package path."""
    return dirname(dirname(abspath(__file__)))


def get_mock_s3_path():
    """Returns the local s3 mock directory."""
    mock_dir = get_config_attr("s3_patch_dir")
    if mock_dir.endswith("/"):
        mock_dir = mock_dir[:-1]
    return mock_dir


def append_git_ignore(git_ignore_path=".gitignore"):
    """Appends the additional patterns to the gitignore.

    Args:
      git_ignore_path: (Default value = '.gitignore')

    Returns:

    """

    with open(git_ignore_path) as f:
        git_ignore = f.read()

    git_ignore = git_ignore.split("\n")
    for pattern in GIT_IGNORE_PATTERNS:
        if pattern not in git_ignore:
            git_ignore.append(pattern)

    with open(git_ignore_path, "w") as f:
        f.write("\n".join(git_ignore))


def create_git_ignore():
    """Creates git ignore if it doesn't exist."""
    git_ignore_path = ".gitignore"
    if not os.path.isfile(git_ignore_path):
        with open(git_ignore_path, "w") as f:
            f.write("\n".join(GIT_IGNORE_PATTERNS))
    else:
        append_git_ignore(git_ignore_path)


@lru_cache()
def get_config_attr(key, toml_path=DEFAULT_TOML_PATH):
    """Looks for a attribute in the project toml.
       If its not specified then it asks the user for an input.

    Args:
      key:
      toml_path: (Default value = DEFAULT_TOML_PATH)

    Returns:

    """

    if not _pyproject_toml_exists(toml_path):
        cprint(f"No '{toml_path}' found.", "WARNING")
    else:
        conf = load_config()
        if key not in conf:
            cprint(f"No '{key}' found in config.", "WARNING")
        elif conf[key] is None or conf[key] == "":
            cprint(f"No '{key}' found in config.", "WARNING")
        else:
            return conf[key]

    value = cinput(f"Select {key}", DEFAULT_CONFIG_TEMPLATE.get(key, ""))
    if value is None or value == "":
        ValueError(f"'{value}' is not a valid value for '{key}'")

    return value


def get_project_attr(key):
    if _pyproject_toml_exists():
        toml = _get_pyproject_toml()
        return toml.get('tool',{}).get('poetry',{}).get(key,'')
    return ''



def get_project_attrs(attrs):
    res = {}
    for attr in attrs:
        res[attr] = get_project_attr(attr)
    return res

def get_email(author):
    for part in author.split(' '):
        if '@' in part:
            if part.endswith('>'):
                part = part[:-1]
            if part.startswith('<'):
                part = part[1:]
            return part

def get_emails():
    res = []
    authos = get_project_attr('authors')
    for author in authos:
        res.append(get_email(author))
    return res

def get_name(author):
    email = get_email(author)
    author = author.replace(email).replace("<>")
    return author.strip()
    

def get_owner_emails():
    res=[]
    authos = get_project_attr('authors')
    for author in authos:
        email = get_name(author)
        res.append(email)
    return res
    

def get_project_name():
    """Get the name of the project. If it doesn't exists it asks the user."""
    if _pyproject_toml_exists():
        proj_config = _get_pyproject_toml()
        project_name = proj_config["tool"]["poetry"]["name"]
        return project_name

    return cinput("Project name", DEFAULT_CONFIG_TEMPLATE.get("name", "tmp"))


def get_cluster_name(cluster_name: str = ""):
    """Get cluster name.

    Args:
      cluster_name: str:  (Default value = '')

    Returns:

    """

    if cluster_name in ["", None, "None"]:
        cluster_name = get_config_attr("cluster-name")

    return cluster_name


@lru_cache()
def get_version():
    """Returns the package version from the project toml."""
    if _pyproject_toml_exists():
        config = _get_pyproject_toml()
        return config["tool"]["poetry"]["version"]
    else:
        return cinput("Version", "v1")


@lru_cache()
def get_s3_staging_dir():
    """Returns the s3 staging directory."""
    s3_stage_dir = get_config_attr("s3-staging-dir")
    if s3_stage_dir.endswith("/"):
        s3_stage_dir = s3_stage_dir[:-1]
    return s3_stage_dir


def get_env_name():
    """Returns the enviroment name."""
    load_config()
    project_name = get_project_name()
    env_name = project_name.replace(" ", "_").lower()
    version = str(get_version()).replace(".", "_").lower()
    stage = get_config_attr("stage").lower()
    return f"{env_name}_{stage}_{version}"


def get_build_name():
    """Get the project name"""
    project_name = get_env_name()
    return f"{project_name}.tar.gz"


def get_project_type(toml_path: str = DEFAULT_TOML_PATH):
    """Get the type of project. e.g. poetry.

    Args:
      toml_path: str:  (Default value = DEFAULT_TOML_PATH)

    Returns:

    """
    if os.path.isfile(toml_path):
        return "poetry"

    raise ValueError(f'No "{toml_path}" found.')


def _pyproject_toml_exists(pyproj_path: str = DEFAULT_TOML_PATH):
    """Checks if the project toml exists.

    Args:
      pyproj_path: str: (Default value = DEFAULT_TOML_PATH)

    Returns:

    """
    return os.path.isfile(pyproj_path)


def _get_pyproject_toml(pyproj_path: str = DEFAULT_TOML_PATH) -> Dict[str, str]:
    """Returns the pyproject toml file as a dict.

    Args:
      pyproj_path: str:  (Default value = DEFAULT_TOML_PATH)

    Returns:
      dict: Project toml param.

    """

    if _pyproject_toml_exists():
        with open(pyproj_path, encoding="utf8") as pyproject:
            file_contents = pyproject.read()
        return tomlkit.parse(file_contents)
    else:
        raise ValueError(f"'{pyproj_path}' does not exists. Run 'pyemr init'.")

    return {}


def _write_pyproject_toml(file_contents: dict, pyproj_path: str = DEFAULT_TOML_PATH ):
    """Writes a dict into a toml file

    Args:
      file_contents: dict:
      pyproj_path: str:  (Default value = DEFAULT_TOML_PATH)

    Returns:

    """
    with open(pyproj_path, "w", encoding="utf8") as pyproject:
        pyproject.write(tomlkit.dumps(file_contents))


def load_config():
    """Loads the pyemr config parameters from the project toml file."""
    tml = _get_pyproject_toml()
    if "tool" in tml:
        if "pyemr" in tml["tool"]:
            return tml["tool"]["pyemr"]

    return {}


def set_param(key, value):
    """Sets a pyemr param in the project toml.

    Args:
      key:
      value:

    Returns:

    """

    tml = _get_pyproject_toml()

    if "tool" not in tml:
        tml["tool"] = {}

    if "pyemr" not in tml["tool"]:
        tml["tool"]["pyemr"] = {}

    tml[key] = value
    _write_pyproject_toml(tml)


def color_text(text, style="OKCYAN"):
    """Returns a styles text string.

    Args:
      text:
      style: (Default value = 'OKCYAN')

    Returns:

    """
    return f"{STDOUT_COLORS[style]}{text}{STDOUT_COLORS['ENDC']}"


def cinput(variable_name, default):
    """A coloured version of the python prompt funciton.

    Args:
      variable_name:
      default:

    Returns:

    """
    prompt = color_text(variable_name, "OKCYAN")
    prompt += color_text(" [", "OKCYAN")
    prompt += color_text(str(default), "OKGREEN")
    prompt += color_text("]", "OKCYAN")

    print(prompt, end="")
    value = input() or default
    print(value)
    return value


def cprint(text, color="OKCYAN"):
    """Print coloured stdout.

    Args:
      text:
      color: (Default value = 'OKCYAN')

    Returns:

    """
    print(color_text(text, color))


def init_pyemr_param(cluster_name, s3_stage_dir, stage, region):
    """Append EMR pack aparameters to the project toml.

    Args:
      cluster_name:
      stage_dir:
      s3_stage_dir:
      stage:
      region:

    Returns:

    """

    tml = _get_pyproject_toml()

    if "tool" not in tml:
        tml["tool"] = {}

    if "pyemr" not in tml["tool"]:
        tml["tool"]["pyemr"] = {}

    if cluster_name:
        tml["tool"]["pyemr"]["cluster-name"] = cluster_name

    if s3_stage_dir:
        tml["tool"]["pyemr"]["s3-staging-dir"] = s3_stage_dir

    if stage:
        tml["tool"]["pyemr"]["stage"] = stage

    if region:
        tml["tool"]["pyemr"]["region"] = region

    for variable_name, default_value in DEFAULT_CONFIG_TEMPLATE.items():
        if variable_name not in tml["tool"]["pyemr"]:
            if variable_name in REQUIRED_PARAM:
                value = cinput(variable_name, default_value)
            else:
                value = default_value
            tml["tool"]["pyemr"][variable_name] = value

    print("[tool.pyemr]")
    print(tomlkit.dumps(tml["tool"]["pyemr"]))

    _write_pyproject_toml(tml)


def add_dependencies(dep):
    """Add dependencies to the project toml file.

    Args:
      dep:

    Returns:

    """
    tml = _get_pyproject_toml()
    tml["tool"]["poetry"]["dependencies"].update(dep)
    _write_pyproject_toml(tml)


def add_packages_to_toml(package_path):
    """Adds package paths to python project toml.

    Args:
      package_path:

    Returns:

    """

    package_obj = tomlkit.inline_table()
    tml = _get_pyproject_toml()
    package_obj["include"] = package_path
    if "packages" not in tml["tool"]["poetry"]:
        tml["tool"]["poetry"]["packages"] = []

    tml["tool"]["poetry"]["packages"].append(package_obj)
    _write_pyproject_toml(tml)


def add_pyemr_param(key, value):
    """Add a pyemr parameter to the project toml file.

    Args:
      key:
      value:

    Returns:

    """
    tml = _get_pyproject_toml()

    if "tool" not in tml:
        tml["tool"] = {}

    if "pyemr" not in tml["tool"]:
        tml["tool"]["pyemr"] = {}

    tml["tool"]["pyemr"][key] = value
    _write_pyproject_toml(tml)


def create_koalas_example(out_path):
    """Writes a Koalas example to the project template.

    Args:
      out_path:

    Returns:

    """

    path = f"{out_path}/script.py"
    if not os.path.isfile(path):
        with open(path, "w") as f:
            f.write(SIMPLE_KOALAS_EXAMPLE.strip())


def add_main_package():
    """Makes package based on project name."""
    tml = _get_pyproject_toml()
    name = tml["tool"]["poetry"]["name"]
    package_path = name.replace(" ", "_").lower()
    os.system(f"mkdir {package_path}")
    create_koalas_example(package_path)
    add_packages_to_toml(package_path)


def add_scr_package():
    """Creates src math for project."""
    package_path = "src"
    os.system(f"mkdir {package_path}")
    create_koalas_example(package_path)
    add_packages_to_toml(package_path)


def init_pyemr(project_name, cluster_name, s3_stage_dir, stage, region):
    """Init the pyemr project toml.

    Args:
      cluster_name:
      stage_dir:
      project_name:
      s3_stage_dir:
      stage:
      region:

    Returns:

    """

    dep = [
        f"--dependency={name}={version}"
        for name, version in DEFAULT_DEPENDENCIES.items()
    ]

    if not _pyproject_toml_exists():
        if project_name is None or project_name == "":
            project_name = cinput("Project Name", "tmp")
        args = [
            "poetry",
            "init",
            "--python=>=3.7.1,<3.9",
            "-n",
            "--name",
            project_name,
            "--quiet",
        ] + dep
        proc = subprocess.Popen(args)
        proc.communicate()

    # install default dependencies
    # add_dependencies(DEFAULT_DEPENDENCIES)
    add_scr_package()
    init_pyemr_param(cluster_name, s3_stage_dir, stage, region)
    create_git_ignore()
    os.system("open pyproject.toml")


def get_staging_dir():
    """Returns the staging directory along with version and stage."""
    project_name = get_project_name().replace(" ", "_").lower()
    stage = get_config_attr("stage")
    version = get_version()
    s3_stage_dir = get_s3_staging_dir()
    stage_path = f"{s3_stage_dir}/{project_name}/stage={stage}/version={version}"
    return stage_path


def get_datetime_string():
    """Returns the datetime string based on project config"""

    if not _pyproject_toml_exists():
        return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    conf = load_config()
    if conf["date-time"] == "now":
        return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    if conf["date-time"] == "today":
        return datetime.now().strftime("%Y-%m-%d")
    if conf["date-time"] == "latest":
        return "latest"
    if "%" in conf["date-time"]:
        return datetime.now().strftime(conf["date-time"])

    return None


def get_local_poetry_venv_python_path():
    """Returns the poetry virtual enviroment path."""
    os.system("poetry install")
    return os.system("poetry run which python")


def yield_spark_home():
    """Find the spark home"""

    for site_package in sys.path:
        yield f"{site_package}/pyspark"

    if "SPARK_HOME" in os.environ:
        yield os.environ["SPARK_HOME"]

        if "apache-spark" in os.environ["SPARK_HOME"]:
            root = os.environ["SPARK_HOME"].split("apache-spark")[0]
            for path in sorted(glob.glob(root + "apache-spark/*/libexec")):
                yield

    yield from sorted(glob.glob(MAC_SPARK_DIR + "/*/libexec"), reverse=True)

    yield "/usr/local/lib/python3.7/site-packages/pyspark"


def get_new_spark_home():
    """ """

    for path in yield_spark_home():
        if path and path.strip() != "":
            if os.path.isdir(path):
                if path.endswith("/libexec"):
                    return path

    for path in yield_spark_home():
        if path and path.strip() != "":
            if os.path.isdir(path):
                if path.endswith("/site-packages/pyspark"):
                    return path


def set_spark_home():
    """Tries to set the correct spark home."""
    os.environ["SPARK_HOME"] = get_new_spark_home()
    print("SPARK_HOME=", os.environ["SPARK_HOME"])
    findspark.init()


def check_pwd_is_clean():
    """ """
    if os.path.isfile("pyemr"):
        cprint("WARNING: Your pwd contains a folder called 'pyemr'", "WARNING")



if __name__ == "__main__":
    check_pwd_is_clean()
