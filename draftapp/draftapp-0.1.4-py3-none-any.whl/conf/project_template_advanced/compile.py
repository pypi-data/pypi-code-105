# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from pathlib import Path
import os
import sys

# Get current folder path
mash_path = os.path.dirname(sys.argv[0])

files = list(Path(mash_path).glob("**/*.py"))
extensions = []
files_to_exclude = ["compile", "lint", "setup", "gunicorn", "env", "tasks", "__init__"]
folders_to_exclude = ["tests", "alembic/versions"]

# build .so files from .py files ###
if True:
    for file in files:
        # Take out file name without .py ext
        filename = Path(file).resolve().stem
        if file.stat().st_size != 0 and filename not in files_to_exclude:
            relpath = os.path.relpath(
                os.path.dirname(file.absolute().as_posix()), mash_path
            )
            if relpath not in folders_to_exclude:
                packagename = (
                    relpath.replace("/", ".") + "." + filename
                    if relpath != "."
                    else filename
                )
                print(relpath + ":" + packagename)
                extensions.append([Extension(packagename, [str(file)])])
    for ext in extensions:
        setup(
            ext_modules=cythonize(
                ext,
                compiler_directives={
                    "always_allow_keywords": True,
                    "c_string_type": "str",
                    "c_string_encoding": "utf8",
                    "language_level": 3,
                },
            )
        )


def unlink_files(list_of_files, exclude=True):
    for file in list_of_files:
        if not exclude:
            file.unlink()
            continue
        filename = Path(file).resolve().stem
        relpath = os.path.relpath(
            os.path.dirname(file.absolute().as_posix()), mash_path
        )
        dirname = relpath.split("/")[0]
        if relpath not in folders_to_exclude and filename not in files_to_exclude:
            file.unlink()


unlink_files(files)
unlink_files(list(Path(mash_path).glob("**/*.c")), False)
unlink_files(list(Path(mash_path).glob("**/*.pyc")))
