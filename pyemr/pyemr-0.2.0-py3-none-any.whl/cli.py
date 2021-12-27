# pylint: disable=R0201
"""Command Line Interface"""

import os
from pprint import pprint
# import awswrangler as wr
from subprocess import check_output

import fire

from pyemr.utils.mocking import (
    mock_part_s3_folder, mock_s3_folder, mock_test_some_script,
)
from pyemr.utils.notebook import (
    launch_mock_notebook_docker, run_notebook_in_poetry, run_notebook_on_sys,
)
from pyemr.utils.python import (
    launch_mock_python, launch_mock_python_docker, launch_mock_python_venv,
)

from .utils.build import build, submit_spark_step
from .utils.config import init_pyemr
from .utils.docker import (
    launch_docker_bash, launch_docker_shell, run_docker_test,
)
from .utils.emr import (
    cancel_step, describe_cluster, describe_step, get_clusters_list_df,
    get_step_state, list_steps, ssm_cluster,
)
from .utils.linting import format_code, lint_wd
from .utils.logs import (
    download_all_emr_logs, print_emr_log_files_lines, summarize_logs,
)
from pyemr.utils.export import export_airflow_template


class Cli:
    """Command line interface for the package."""

    def init(
        self,
        project_name="",
        target_cluster="",
        s3_stage_dir="",
        stage="",
        region="",
    ):
        """Create a pyproject.toml containing pyemr config.

        Args:
          cluster_name: (Default value = '')
          stage_dir: (Default value = '')
          project_name: (Default value = '')
          target_cluster: (Default value = "")
          s3_stage_dir: (Default value = "")
          stage: (Default value = '')
          region: (Default value = '')

        Returns:

        """
        init_pyemr(project_name, target_cluster, s3_stage_dir, stage, region)

    def ssh(self, cluster_name=""):
        """A proxy name for ssm.

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        self.ssm(cluster_name)

    def ssm(self, cluster_name=""):
        """smm into the cluster master node.

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        ssm_cluster(cluster_name)

    def build(self, cluster_name=""):
        """Zips the python package and dependencies and then uploads them s3 staging directory.

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        build(cluster_name)

    def install(self, cluster_name=""):
        """

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        self.build(cluster_name)

    def submit(
        self,
        script,
        submit_mode="client",
        cluster_name="",
        wait=True,
        **kwargs,
    ):
        """

        Args:
          script:
          submit_mode: (Default value = 'client')
          cluster_name: (Default value = '')
          wait: (Default value = True)
          *args:
          **kwargs:

        Returns:

        """
        submit_spark_step(script, submit_mode, cluster_name, wait, **kwargs)

    def config(self, toml_path="pyproject.toml"):
        """

        Args:
          toml_path: (Default value = "./pyproject.toml")

        Returns:

        """
        input_dir = os.getcwd()
        check_output(["open", f"{input_dir}/{toml_path}"])

    def export(
            self,
            local_script_path,
            submit_mode='client',
            action_on_failure='CONTINUE',
            *args,
            **kwargs,
        ):
        """

        Args:
          type:

        Returns:

        """
        #assert type in ["aws", "bash", "python", "airflow", "awswrangler"]
        export_airflow_template(
                local_script_path,
                submit_mode='client',
                action_on_failure='CONTINUE',
                *args,
                **kwargs,
        )
        

    def steps(
        self,
        cluster_name="",
        n=10,
        step_name="{env_name}:*",
        states="*",
        all=False,
    ):
        """

        Args:
          cluster_name: (Default value = "")
          n: (Default value = 10)
          step_name: (Default value = "*{env_name}*")
          states: (Default value = '*')
          all: (Default value = False)

        Returns:

        """
        if all:
            step_name = states = "*"
        pprint(list_steps(cluster_name, n, step_name, states))

    def cancel(
        self,
        step_id="latest",
        cluster_name="",
        step_name_pattern="{env_name}:*",
        state="*",
    ):
        """

        Args:
          step_id: (Default value = "")
          cluster_name: (Default value = "")
          step_name_pattern: (Default value = "*{env_name}*")
          state: (Default value = "*")

        Returns:

        """
        pprint(cancel_step(cluster_name, step_id, step_name_pattern, state))

    def describe_step(
        self,
        step_id="latest",
        cluster_name="",
        name="{env_name}:*",
        state="*",
    ):
        """

        Args:
          step_id: (Default value = "")
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")

        Returns:

        """
        pprint(describe_step(cluster_name, step_id, name, state))

    def stderr(
        self,
        step_id="latest",
        n=30,
        cluster_name="",
        name="*{env_name}*",
        state="*",
        out_dir="logs",
    ):
        """

        Args:
          step_id: (Default value = "")
          n: (Default value = 30)
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")
          out_dir: (Default value = "./logs")

        Returns:

        """
        print_emr_log_files_lines(
            "stderr",
            n,
            step_id,
            cluster_name,
            name,
            state,
            out_dir,
            "FAIL",
        )

    def stdout(
        self,
        step_id="latest",
        n=30,
        cluster_name="",
        name="*{env_name}*",
        state="*",
        out_dir="logs",
    ):
        """

        Args:
          step_id: (Default value = "")
          n: (Default value = 30)
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")
          out_dir: (Default value = "./logs")

        Returns:

        """
        print_emr_log_files_lines(
            "stdout",
            n,
            step_id,
            cluster_name,
            name,
            state,
            out_dir,
            "OKCYAN",
        )

    def state(self, step_id="latest", cluster_name="", name="*{env_name}*", state="*"):
        """

        Args:
          step_id: (Default value = "")
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")

        Returns:

        """
        get_step_state(cluster_name, step_id, name, state)

    def describe_cluster(self, cluster_name=""):
        """

        Args:
          cluster_name: (Default value = "")

        Returns:

        """
        pprint(describe_cluster(cluster_name))

    def clusters(self, states="RUNNING|WAITING", n=10):
        """List the clusters in the given states.

        Args:
          states: (Default value = "RUNNING|WAITING" )
          n: (Default value = 10)

        Returns:

        """
        print(get_clusters_list_df(states, n))

    def notebook(
        self,
        env: str = "docker",
    ):
        """Runs docker notebooks with s3 patch.

        Args:
          env: str:  (Default value = 'docker')
          env: str:  (Default value = "docker")

        Returns:

        """
        assert env in ["sys", "local", "os", "poetry", "venv", "docker", "linux"]

        if env in ["sys", "local", "os"]:
            run_notebook_on_sys()

        if env in ["venv", "poetry"]:
            run_notebook_in_poetry()

        if not os.path.exists("pyproject.toml"):
            raise ValueError(
                "No pyproject.toml exists. Try 'pyemr python -env sys' or run 'pyemr init'",
            )

        if env in ["docker", "linux"]:
            launch_mock_notebook_docker()

    def venv_python(self):
        """Runs interactive python session with s3 patch inside the virtuual env."""
        launch_mock_python_venv()

    def python(self, env: str = "docker"):
        """Runs interactive docker python session with s3 patch.

        Args:
          env: str:  (Default value = 'docker')
          env: str:  (Default value = "docker")

        Returns:

        """
        assert env in ["sys", "local", "os", "poetry", "venv", "docker", "linux"]

        if env in ["sys", "local", "os"]:
            launch_mock_python()

        if not os.path.exists("pyproject.toml"):
            raise ValueError(
                "No pyproject.toml exists. Try 'pyemr python -env sys' or run 'pyemr init'",
            )

        if env in ["poetry", "venv"]:
            launch_mock_python_venv()

        if env in ["docker", "linux"]:
            launch_mock_python_docker()

    def sh(self):
        """Stats a docker shell session."""
        launch_docker_shell()

    def bash(self):
        """Stats a docker bash session."""
        launch_docker_bash()

    def local_test(self, script, *args, **kwargs):
        """Run a script locally with s3 patch.

        Args:
          script:
          *args:
          **kwargs:

        Returns:

        """
        mock_test_some_script(script, *args, **kwargs)

    def test(self, script, *args, **kwargs):
        """Run a script inside the docker with s3 patch..

        Args:
          script:
          *args:
          **kwargs:

        Returns:

        """
        run_docker_test(script, *args, **kwargs)

    def logs(
        self,
        step_id="latest",
        out_dir="logs",
        cluster_name="",
        name="*{env_name}*",
        state="*",
    ):
        """Downloads logs for a step, and creates a summary or errors/warnings.

        Args:
          out_dir: (Default value = "logs")
          step_id: (Default value = "")
          cluster_name: (Default value = "")
          name: (Default value = "*{env_name}*")
          state: (Default value = "*")

        Returns:

        """
        download_all_emr_logs(cluster_name, step_id, name, state, out_dir)
        summarize_logs(cluster_name, step_id, name, state, out_dir)

    def local(self, script, *args, **kwargs):
        """Test locally. Outside the docker.

        Args:
          script:
          *args:
          **kwargs:

        Returns:

        """
        self.local_test(script, *args, **kwargs)

    def lint(self, *args, **kwargs):
        """Lints the code in the current directory.

        Args:
          *args:
          **kwargs:

        Returns:

        """

        lint_wd(*args, **kwargs)

    def format(self):
        """Auto-formats the code in the current directory."""
        format_code()

    def mock(self, s3_path: str, all: bool = False):
        """Finds and downloads a part of the file.

        Args:
          seld:
          s3_path: str:
          s3_path: str:
          all: bool:  (Default value = False)
          s3_path: str:
          all: bool:  (Default value = False)

        Returns:

        """
        if all:
            mock_s3_folder(s3_path)
        else:
            mock_part_s3_folder(s3_path)


def main():
    """ """
    fire.Fire(Cli)


if __name__ == "__main__":
    main()
