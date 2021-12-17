#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia, 2016
#    Copyright by UWA (in the framework of the ICRAR)
#    All rights reserved
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#    MA 02111-1307  USA
#

import os
import subprocess
import sys
import sysconfig

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install

# Version information
# We do like numpy: we have a major/minor/patch hand-written version written
# here. If we find the git commit (either via "git" command execution or in a
# dlg/version.py file) we append it to the VERSION later.
# The RELEASE flag allows us to create development versions properly supported
# by setuptools/pkg_resources or "final" versions.
MAJOR = 2
MINOR = 1
PATCH = 0
RELEASE = True
VERSION = "%d.%d.%d" % (MAJOR, MINOR, PATCH)
VERSION_FILE = "dlg/runtime/version.py"
PTH_FILE = "lib64_dist.pth"


def get_git_version():
    out = subprocess.check_output(["git", "rev-parse", "HEAD"])
    return out.strip().decode("ascii")


def get_version_info():
    git_version = "Unknown"
    if os.path.exists(".git"):
        git_version = get_git_version()
    full_version = VERSION
    if not RELEASE:
        full_version = "%s.dev0+%s" % (VERSION, git_version[:7])
    return full_version, git_version


def write_version_info():
    tpl = """
# THIS FILE IS GENERATED BY SETUP.PY
# DO NOT MODIFY BY HAND
version = '%(version)s'
git_version = '%(git_version)s'
full_version = '%(full_version)s'
is_release = %(is_release)s

if not is_release:
    version = full_version
"""
    full_version, git_version = get_version_info()
    with open(VERSION_FILE, "w") as f:
        info = tpl % {
            "version": VERSION,
            "full_version": full_version,
            "git_version": git_version,
            "is_release": RELEASE,
        }
        f.write(info.strip())


# Every time we overwrite the version file
write_version_info()


# HACK - HACK - HACK - HACK
class lib64_path(install):
    def write_pth_file(self):
        """
        This is a hack to get around some distributions installing stuff into
        lib64/python-x.x/dist-packages
        """
        lp = os.path.abspath(os.path.curdir)
        with open(PTH_FILE, "w") as f:
            f.write(lp.replace("/lib/", "/lib64/"))

    def initialize_options(self):
        install.initialize_options(self)
        self.build_scripts = None

    def finalize_options(self):
        install.finalize_options(self)
        self.set_undefined_options("build", ("build_scripts", "build_scripts"))

    def run(self):
        install.run(self)
        lp = sysconfig.get_path("stdlib")
        with open(PTH_FILE, "w") as f:
            f.write("{0}/dist-packages".format(lp))
        install.copy_file(self, PTH_FILE, os.path.join(self.install_lib, PTH_FILE))

# Core requirements of DALiuGE
# Keep alpha-sorted PLEASE!
install_requires = [
    "wheel",
    "bottle",
    "configobj",
    "crc32c",
    "daliuge-common==%s" % (VERSION,),
    "dill",
    "docker",
    "lockfile",
    # 0.10.6 builds correctly with old (<=3.10) Linux kernels
    "netifaces>=0.10.6",
    "numpy",
    "overrides",
    "paramiko",
    "psutil",
    "pyarrow",
    "python-daemon",
    "pyzmq",
    "scp",
    # 0.19.0 requires netifaces < 0.10.5, exactly the opposite of what *we* need
    "zeroconf >= 0.19.1",
    # 0.6 brings python3 support plus other fixes
    "zerorpc >= 0.6",
]
# Keep alpha-sorted PLEASE!

# Extra requirements that are not needed by your every day daliuge installation
extra_requires = {
    # spead is required only for a specific app and its test, which we
    # skip anyway if spead is not found
    "spead": ["spead2==0.4.0"],
    # drive-casa is used by some manual tests under test/integrate
    "drive-casa": ["drive-casa>0.7"],
    # MPI support (MPIApp drops and HPC experiments) requires mpi4py
    "MPI": ["mpi4py"],
    # AWS storage types
    "aws": ["boto3"],
}


setup(
    name="daliuge-engine",
    version=get_version_info()[0],
    description=u"Data Activated \uF9CA (flow) Graph Engine - Execution Engine",
    long_description="""
        The element of the DALiuGE system executing the workflows. This replaces
        the former 'runtime' package (up to version 1.0). For more information 
        see the [Basics section(https://daliuge.readthedocs.io/en/latest/basics.html)]
        of the DALiuGE documentation.
        """,
    author="ICRAR DIA Group",
    author_email="dfms_prototype@googlegroups.com",
    url="https://github.com/ICRAR/daliuge",
    license="LGPLv2+",
    packages=find_packages(exclude=("test", "test.*", "fabfile")),
    package_data={
        "dlg.apps": ["dlg_app.h", "dlg_app2.h"],
        "dlg.manager": [
            "web/*.html",
            "web/static/css/*.css",
            "web/static/fonts/*",
            "web/static/js/*.js",
            "web/static/js/d3/*",
            "web/static/icons/*",
        ],
        "dlg.dropmake": [
            "web/lg_editor.html",
            "web/*.css",
            "web/*.js",
            "web/*.json",
            "web/*.map",
            "web/img/jsoneditor-icons.png",
            "web/pg_viewer.html",
            "web/matrix_vis.html",
            "lib/libmetis.*",
            "web/static/icons/*",
        ],
        "test.dropmake": ["logical_graphs/*.json"],
        "test.apps": ["dynlib_example.c", "dynlib_example2.c"],
    },
    entry_points = {
        'dlg.tool_commands': ['runtime=dlg.runtime.tool_commands']
    },
    install_requires=install_requires,
    extras_require=extra_requires,
    test_suite="test",
    cmdclass={"install": lib64_path},
)
