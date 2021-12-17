# SPDX-FileCopyrightText: Copyright 2021, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the license found in the LICENSE.txt file in the root
# directory of this source tree.


# =======
# Imports
# =======

import sys
import platform
import os
from os.path import join
import re
import json

__all__ = ['locate_cuda', 'get_cuda_version']


# ============
# find in path
# ============

def _find_in_path(executable_name, path):
    """
    Recursively searches the executable ``executable_name`` in all of the
    directories in the given path, and returns the full path of the executable
    once its first occurrence is found.. If no executable is found, ``None`` is
    returned. This is used to find CUDA's directories.
    """

    for dir in path.split(os.pathsep):
        executable_path = join(dir, executable_name)
        if os.path.exists(executable_path):
            return os.path.abspath(executable_path)
    return None


# ===========
# locate cuda
# ===========

def locate_cuda():
    """
    Finds the executable ``nvcc`` (or ``nvcc.exe`` if windows). If found,
    creates a dictionary of cuda's executable path, include and lib directories
    and home directory. This is used for GPU.
    """

    # List of environment variables to search for cuda
    environs = ['CUDA_HOME', 'CUDA_ROOT', 'CUDA_PATH']
    cuda_found = False

    # nvcc binary
    nvcc_binary_name = 'nvcc'
    if sys.platform == 'win32':
        nvcc_binary_name = nvcc_binary_name + '.exe'

    # Search in each of the possible environment variables, if they exist
    for env in environs:
        if env in os.environ:

            # Home
            home = os.environ[env]
            if not os.path.exists(home):
                continue

            # nvcc binary
            nvcc = join(home, 'bin', nvcc_binary_name)
            if not os.path.exists(nvcc):
                continue
            else:
                cuda_found = True
                break

    # Brute-force search in all path to find nvcc binary
    if not cuda_found:
        nvcc = _find_in_path(nvcc_binary_name, os.environ['PATH'])
        if nvcc is None:
            cuda = {}
            return cuda

        home = os.path.dirname(os.path.dirname(nvcc))

    # Include directory
    include = join(home, 'include')
    if not os.path.exists(include):
        cuda = {}
        return cuda

    # Library directory
    lib = join(home, 'lib')
    if not os.path.exists(lib):
        lib64 = join(home, 'lib64')
        if not os.path.exists(lib64):
            raise EnvironmentError("The CUDA's lib directory could not be " +
                                   "located in %s or %s." % (lib, lib64))
        lib = lib64

    # For windows, add "x64" or "x86" to the end of lib path
    if sys.platform == "win32":

        # Detect architecture is 64bit or 32bit
        if platform.machine().endswith('64'):
            lib = join(lib, 'x64')
        else:
            lib = join(lib, 'x86')

        if not os.path.exists(lib):
            raise EnvironmentError("The CUDA's lib sub-directory could not " +
                                   "be located in %s." % lib)

    # Get a dictionary of cuda version with keys 'major', 'minor', and 'patch'.
    version = get_cuda_version(home)

    # Output dictionary of set of paths
    cuda = {
        'home': home,
        'nvcc': nvcc,
        'include': include,
        'lib': lib,
        'version': version
    }

    return cuda


# ================
# get cuda version
# ================

def get_cuda_version(cuda_home):
    """
    Gets the version of CUDA library.

    :param cuda_home: The CUDA home paths.
    :type cuda_home: str

    :return: A dictionary with version info containing the keys 'major',
        'minor', and 'patch'.
    :rtype: dict
    """

    version_txt_file = join(cuda_home, 'version.txt')
    version_json_file = join(cuda_home, 'version.json')
    if os.path.isfile(version_txt_file):

        # txt version file is used in CUDA 10 and earlier.
        with open(version_txt_file, 'r') as file:

            # Version_string is like "11.3.1"
            version_string = file.read()

    elif os.path.isfile(version_json_file):

        # json version file is used in CUDA 11 and newer
        with open(version_json_file, 'r') as file:
            info = json.load(file)

            # Version_string is like "11.3.1"
            version_string = info['cuda']['version']

    else:
        # Find cuda version directly by grep-ing include/cuda.h file
        cuda_filename = join(cuda_home, 'include', 'cuda.h')

        # Regex pattern finds a match like "#define CUDA_VERSION 11030"
        regex_pattern = r'^#define CUDA_VERSION.\d+$'
        match = ''

        with open(cuda_filename, 'r') as file:
            for line in file:
                if re.match(regex_pattern, line):
                    match = line
                    break

        if match != '':

            # version_string is like "11030"
            version_string = match.split()[-1]

            # Place a dot to separate major and minor version to parse them
            # later. Here, version_string becomes something like "11.03.0"
            version_string = version_string[:-3] + "." + version_string[-3:]
            version_string = version_string[:-1] + "." + version_string[-1:]

        else:
            error_message_1 = 'Cannot find CUDA "version.txt" or ' + \
                              '"version.json" file in %s. ' % cuda_home
            error_message_2 = 'Cannot find "CUDA_VERSION" in header file %s.' \
                              % cuda_filename
            raise FileNotFoundError(error_message_1 + error_message_2)

    # Convert string to a list of int
    version_string_list = version_string.split(' ')[-1].split('.')
    version_int = [int(v) for v in version_string_list]

    # Output dictionary
    version = {
            'major': None,
            'minor': None,
            'patch': None
    }

    # Fill output dictionary
    if len(version_int) == 0:
        raise ValueError('Cannot detect CUDA major version.')
    else:
        version['major'] = version_int[0]
    if len(version_int) > 1:
        version['minor'] = version_int[1]
    if len(version_int) > 2:
        version['patch'] = version_int[2]

    return version
