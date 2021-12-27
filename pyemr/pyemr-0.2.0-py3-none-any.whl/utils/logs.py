"""A collection of aws tools"""
import glob
import gzip
import os
import os.path
import pathlib
import re
from functools import lru_cache
from pathlib import Path

import pandas as pd

from .config import cprint
from .emr import get_cluster_id, get_last_submitted_step, get_log_url
from .s3 import download_s3_folder


# import awswrangler as wr

SPARK_ERRORS = [
    "filenotfound",
    "error",
    "exception",
    "aborted",
    "failure",
    "failed",
    "reason",
]


@lru_cache()
def get_log_paths(cluster_name, step_id, name_pattern, state, out_dir):
    """Returns the log path of the step.

    Args:
      cluster_name:
      step_id:
      name_pattern:
      state:
      out_dir:

    Returns:

    """

    if step_id is None or step_id == "":
        step_id = get_last_submitted_step(cluster_name, name_pattern, state)

    cluster_id = get_cluster_id(cluster_name)

    # download step logs
    log_url = get_log_url(cluster_name)
    step_logs = f"{log_url}/{cluster_id}/steps/{step_id}/"
    out_dir = f"{out_dir}/{step_id}"
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    return step_logs, out_dir


@lru_cache()
def get_application_id(local_stderr):
    """Get the application id of the step.

    Args:
      local_stderr:

    Returns:

    """
    print("local_stderr", local_stderr)
    if os.path.exists(local_stderr):
        with gzip.open(local_stderr, "r") as file:
            stderr = file.read().decode("utf-8")
    else:
        return None

    start = "Application report for application_"
    end = " (state: "
    app_ids = []

    for line in stderr.split("\n"):
        if start in line:
            line = line.split(start)[-1]
            if end in line:
                app_id = line.split(end)[0].strip()
                if app_id:
                    app_ids += [app_id]

    if len(app_ids) == 0:
        return None

    app_id = max(app_ids, key=app_ids.count)
    return f"application_{app_id}"


def download_all_emr_logs(cluster_name, step_id, name_pattern, state, out_dir):
    """Downloads the client logs and application logs.

    Args:
      cluster_name:
      step_id:
      name_pattern:
      state:
      out_dir:

    Returns:

    """

    if step_id is None or step_id == "":
        step_id = get_last_submitted_step(cluster_name, name_pattern, state)

    cluster_id = get_cluster_id(cluster_name)

    # download step logs
    log_url = get_log_url(cluster_name)
    step_logs = f"{log_url}/{cluster_id}/steps/{step_id}/"
    out_dir = f"{out_dir}/{step_id}"
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    download_s3_folder(step_logs, out_dir)

    # download application logs
    local_stderr = f"{out_dir}/stderr.gz"
    app_id = get_application_id(local_stderr)
    print("app_id", app_id)
    if app_id:
        app_logs = f"{log_url}{cluster_id}/containers/{app_id}/"
        pathlib.Path(f"{out_dir}/{app_id}").mkdir(parents=True, exist_ok=True)
        download_s3_folder(app_logs, f"{out_dir}/{app_id}")


def print_tail_gzip_files(in_path, n_lines, color="OKBLUE"):
    """Prints the last n lines of the emr logs.

    Args:
      in_path:
      n:
      color: (Default value = 'OKBLUE')
      n_lines:

    Returns:

    """
    cprint(f"> tail -n {n_lines} '{in_path}': ")
    print("\n")
    lines = []
    with gzip.open(in_path, "r") as file:
        for line in file:
            lines.append(line.decode("utf-8")[:-1])

    lines = lines[-n_lines:]
    for line in lines:
        cprint(line, color)
    print("\n")


def print_emr_log_files_lines(
    log_type,
    n_lines,
    step_id,
    cluster_name,
    name_pattern,
    state,
    out_dir,
    color="WARNING",
):
    """Downloads and prints the emr logs.

    Args:
      log_type:
      n:
      step_id:
      cluster_name:
      name_pattern:
      state:
      out_dir:
      color: (Default value = 'WARNING')
      n_lines:

    Returns:

    """
    s3_path, step_log_dir = get_log_paths(
        cluster_name,
        step_id,
        name_pattern,
        state,
        out_dir,
    )

    if not os.path.exists(f"{step_log_dir}/{log_type}.gz"):
        download_s3_folder(s3_path, step_log_dir)

    print_tail_gzip_files(f"{step_log_dir}/{log_type}.gz", n_lines, color)


def summarize_logs(cluster_name, step_id, name_pattern, state, out_dir):
    """Create a summary of the emr logs.

    Args:
      cluster_name:
      step_id:
      name_pattern:
      state:
      out_dir:

    Returns:

    """

    _, local_path = get_log_paths(
        cluster_name,
        step_id,
        name_pattern,
        state,
        out_dir,
    )

    logs = []
    logs += glob.glob(f"{local_path}/*.gz")
    logs += glob.glob(f"{local_path}/**/*.gz")
    logs = list(set(logs))

    errors = []
    log_types = ["INFO", "WARN", "ERROR"]

    for pattern in ["*.gz", "**/*.gz"]:
        for log in Path(local_path).rglob("*.gz"):
            with gzip.open(log, "r") as file:
                log_text = file.read().decode("utf-8")
                for i, line in enumerate(log_text.split("\n")):
                    for error in SPARK_ERRORS:
                        if error in line.lower():
                            for log_type in log_types:
                                if log_type in line:
                                    message = log_type + line.split(log_type)[-1]
                                    break
                            else:
                                message = line
                            errors.append(
                                [
                                    error,
                                    log,
                                    i,
                                    line,
                                    message,
                                    re.sub("\\d", "x", line),
                                ],
                            )
                            break

    errors = pd.DataFrame(
        errors,
        columns=["error", "file", "line", "text", "message", "pattern"],
    )
    counts = errors.groupby(["error", "file", "pattern"]).first()
    counts["count"] = errors.groupby(["error", "file", "pattern"]).size()
    counts = counts.reset_index()

    counts = counts.sort_values(["error", "file", "line"])[
        ["count", "file", "error", "line", "message"]
    ]
    counts.to_csv(f"{local_path}/errors.csv")
    print("")
    cprint("Log Summary:", "OKBLUE")
    cprint(counts.head(30).to_string(), "OKBLUE")
