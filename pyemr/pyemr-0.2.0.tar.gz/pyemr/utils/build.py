"""Tools for packaging poetry projects"""
import os
import os.path

import awswrangler as wr

from .config import (
    _pyproject_toml_exists, add_pyemr_param, cprint, get_build_name,
    get_cluster_name, get_datetime_string, get_env_name, get_package_dir,get_config_attr
)
from .docker import docker_build, docker_run_sh
from .emr import get_cluster_id, wait_else_cancel
from .s3 import (
    get_file_s3_path, s3_path_exists, upload_file_s3, upload_to_s3_stage
)


# import awswrangler as wr










def get_local_build_path(prefix=None):
    """Returns the build path of the project.

    Args:
      prefix: (Default value = None)

    Returns:
      str: The build path for the project.

    """
    env_name = get_build_name()
    if prefix is None:
        out_path = f"dist/{env_name}"
    else:
        out_path = f"dist/{env_name}"
    return out_path


def get_client_mode_runner_path():
    """Returns the path of the client mode runner script."""
    package_dir=get_package_dir()
    return f"{package_dir}/sh/client_mode_runner.sh"


def pack_poetry_project_in_docker():
    """Creates a pack file from the poetry project in the currently directory."""

    input_dir = os.getcwd()
    local_build_path = get_local_build_path("amazonlinux")

    # build the docker image
    docker_build()

    # run van-pack inside container
    cprint("Building package inside docker container.")
    sh_cmd = f"/pyemr/sh/build.sh {local_build_path}"
    docker_run_sh(input_dir, sh_cmd)

    return local_build_path


def upload_amazonlinux_build_s3(build_path=None):
    """Uploads the prject build to s3 staging path.

    Args:
      build_path: (Default value = None)

    Returns:

    """
    if build_path is None:
        build_path = get_local_build_path("amazonlinux")
    s3_build_path = upload_file_s3(build_path, out_dir="code")
    return s3_build_path


def get_amazonlinux_build_path_s3():
    """Returns the package build 3s path."""
    build_path = get_local_build_path("amazonlinux")
    s3_build_path = get_file_s3_path(build_path, "latest", "code")
    return s3_build_path


def build(cluster_name):
    """Build the project using pack then uploads it to s3.

    Args:
      location: (Default value = "s3")
      cluster_name:

    Returns:

    """

    build_path = pack_poetry_project_in_docker()
    s3_build_path = upload_amazonlinux_build_s3(build_path)
    add_pyemr_param("latest_build", s3_build_path)
    return s3_build_path


def upload_client_mode_runner_to_s3():
    """Upload client mode runner script to s3."""
    client_runner_path = get_client_mode_runner_path()
    return upload_to_s3_stage(client_runner_path, "latest", "code")



def _get_standalone_spark_step(
        s3_script_path,
        submit_mode='client',
        action_on_failure='CONTINUE',
        args_str='',
        kwargs_str='',
    ):
    
    script_name = s3_script_path.split('/')[-1]
    env_name = "pyemr"
    step_name = f"{env_name}:spark-submit:{script_name}"
    jar_args = ['spark-submit' ,'--deploy-mode', submit_mode ,s3_script_path]
    
    if args_str:
        jar_args.append(args_str)
    
    if kwargs_str:
        jar_args.append(kwargs_str)

    spark_step = {
        "Name": step_name ,
        "ActionOnFailure": action_on_failure ,
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": jar_args,
        },
    }
    
    return spark_step
    
    

def _get_client_spark_step(
        s3_script_path,
        action_on_failure='CONTINUE',
        args_str='',
        kwargs_str='',
    ):
    
    script_name = s3_script_path.split('/')[-1]
    client_runner_s3_path = upload_client_mode_runner_to_s3()
    s3_build_path = get_amazonlinux_build_path_s3()
    
    jar_args = [
        client_runner_s3_path, s3_build_path,
        'sudo', 'PYARROW_IGNORE_TIMEZONE=1' ,
        'PYSPARK_DRIVER_PYTHON=./env/bin/python3' ,
        'PYSPARK_PYTHON=./env/bin/python3' ,
        'spark-submit' ,
        '--deploy-mode', 'client' , s3_script_path
    ]
    
    # add args if they exist
    if args_str:
        jar_args.append(args_str)
    
    if kwargs_str:
        jar_args.append(kwargs_str)
    
    region = get_config_attr('region')
    env_name = get_env_name()
    step_name = f"{env_name}:spark-submit:{script_name}"
    jar = f's3://{region}.elasticmapreduce/libs/script-runner/script-runner.jar'
    spark_step = {
        "Name": step_name ,
        "ActionOnFailure": action_on_failure ,
        "HadoopJarStep": {
            "Jar": jar,
            "Args": jar_args,
        },
    }
    return spark_step



def _get_cluster_spark_step(
        s3_script_path,
        action_on_failure='CONTINUE',
        args_str='',
        kwargs_str='',
    ):
    
    script_name = s3_script_path.split('/')[-1]
    s3_build_path = get_amazonlinux_build_path_s3()
    
    jar_args = [
        'sudo' ,'spark-submit' ,
        '--conf', 'spark.yarn.appMasterEnv.PYSPARK_PYTHON=./env/bin/python3' ,
        '--conf', f'spark.yarn.dist.archives={s3_build_path}#env' ,
        '--master', 'yarn' ,
        '--deploy-mode', 'cluster' ,s3_script_path
    ]
    
    if args_str:
        jar_args.append(args_str)
    
    if kwargs_str:
        jar_args.append(kwargs_str)
    
    env_name = get_env_name()
    step_name = f"{env_name}:spark-submit:{script_name}"
    
    spark_step = {
        "Name": step_name ,
        "ActionOnFailure": action_on_failure ,
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": jar_args,
        },
    }
    
    return spark_step


def get_spark_step(
        local_script_path,
        submit_mode='client',
        action_on_failure='CONTINUE',
        *args,
        **kwargs,
    ):
    """Get spark step config"""
    
    args_str = " ".join(args)
    kwargs_str  = " ".join([f"--{k}={v}" for k, v in kwargs.items()])
    date_time = get_datetime_string()
    s3_script_path = upload_to_s3_stage(local_script_path, date_time, "code")
    submit_mode = submit_mode.lower()
    if not _pyproject_toml_exists():
        spark_step = _get_standalone_spark_step(
            s3_script_path, submit_mode, action_on_failure, args_str, kwargs_str,
        )
    elif submit_mode == "client":
        spark_step = _get_client_spark_step(
            s3_script_path, action_on_failure, args_str,kwargs_str,
        )
    elif submit_mode == "cluster":
        spark_step = _get_cluster_spark_step(
            s3_script_path, action_on_failure,args_str , kwargs_str
        )
    else:
        raise ValueError(f"No submit mode called '{submit_mode}")
    
    return spark_step



def submit_spark_step(
    local_script_path,
    submit_mode,
    cluster_name,
    wait=True,
    *args,
    **kwargs,
):
    """Submit python script to emr cluster.
    
    Args:
      local_script_path:
      submit_mode:
      cluster_name:
      wait: (Default value = True)
      **kwargs:
      *args:

    Returns:
      str: Step id of submited step.

    """
    
    # get the cluster id
    cluster_id = get_cluster_id(cluster_name)
    
    # get spark step dict
    spark_step = get_spark_step(
        local_script_path,
        submit_mode,
        'CONTINUE',
        *args,
        **kwargs,
    )
    
    # check if its a script runner of command runner
    script = spark_step['Jar'].endswith("script-runner.jar")
    
    # submit the step
    step_id = wr.emr.submit_step(
        cluster_id=cluster_id,
        name=spark_step['Name'],
        command=spark_step['HadoopJarStep']['Args'],
        script=script,
    )
    
    # wait till the step is complete
    if wait:
        wait_else_cancel(
            cluster_id,
            step_id,
        )
    
    return step_id
