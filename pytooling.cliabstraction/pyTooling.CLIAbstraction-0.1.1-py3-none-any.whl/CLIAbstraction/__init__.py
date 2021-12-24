# ==================================================================================================================== #
#             _____           _ _               ____ _     ___    _    _         _                  _   _              #
#  _ __  _   |_   _|__   ___ | (_)_ __   __ _  / ___| |   |_ _|  / \  | |__  ___| |_ _ __ __ _  ___| |_(_) ___  _ __   #
# | '_ \| | | || |/ _ \ / _ \| | | '_ \ / _` || |   | |    | |  / _ \ | '_ \/ __| __| '__/ _` |/ __| __| |/ _ \| '_ \  #
# | |_) | |_| || | (_) | (_) | | | | | | (_| || |___| |___ | | / ___ \| |_) \__ \ |_| | | (_| | (__| |_| | (_) | | | | #
# | .__/ \__, ||_|\___/ \___/|_|_|_| |_|\__, (_)____|_____|___/_/   \_\_.__/|___/\__|_|  \__,_|\___|\__|_|\___/|_| |_| #
# |_|    |___/                          |___/                                                                          #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2021 Patrick Lehmann - Bötzingen, Germany                                                             #
# Copyright 2007-2016 Technische Universität Dresden - Germany                                                         #
#                     Chair of VLSI-Design, Diagnostics and Architecture                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
#                                                                                                                      #
# SPDX-License-Identifier: Apache-2.0                                                                                  #
# ==================================================================================================================== #
#
"""\
Basic abstraction layer for executables.
"""
__author__ =    "Patrick Lehmann"
__email__ =     "Paebbels@gmail.com"
__copyright__ = "2014-2021, Patrick Lehmann"
__license__ =   "Apache License, Version 2.0"
__version__ =   "0.1.1"
__keywords__ =  ["abstract", "executable", "cli", "cli arguments"]

from pathlib              import Path
from platform             import system
from typing import Dict, Optional, ClassVar, Type, List, Iterable, Tuple

from pyTooling.Decorators import export
from pyTooling.Exceptions import ExceptionBase, PlatformNotSupportedException
from pyAttributes         import Attribute

from .Argument import CommandLineArgument, ExecutableArgument, ValuedFlagArgument, NameValuedCommandLineArgument, TupleArgument


@export
class CLIAbstractionException(ExceptionBase):
	pass


@export
class DryRunException(CLIAbstractionException):
	"""This exception is raised if an executable is launched while in dry-run mode."""


@export
class CLIOption(Attribute):
	pass


@export
class Program:
	"""Represent an executable."""
	_platform:         str
	_executableNames:  ClassVar[Dict[str, str]]
	_executablePath:   Path
	_dryRun:           bool
	__cliOptions__:    ClassVar[Dict[Type[CommandLineArgument], Optional[CommandLineArgument]]]
	__cliParameters__: Dict[Type[CommandLineArgument], Optional[CommandLineArgument]]

	def __init_subclass__(cls, *args, **kwargs):
		super().__init_subclass__(*args, **kwargs)

		# register all available CLI options (nested classes marked with attribute 'CLIOption')
		cls.__cliOptions__: Dict[CommandLineArgument, Optional[CommandLineArgument]] = {}
		for option in CLIOption.GetClasses():
			cls.__cliOptions__[option] = None

	def __init__(self, executablePath: Path = None, binaryDirectoryPath: Path = None, dryRun: bool = False):
		self._platform =    system()
		self._dryRun =      dryRun

		if executablePath is not None:
			if isinstance(executablePath, Path):
				if not executablePath.exists():
					if dryRun:
						self.LogDryRun(f"File check for '{executablePath}' failed. [SKIPPING]")
					else:
						raise CLIAbstractionException(f"Program '{executablePath}' not found.") from FileNotFoundError(executablePath)
			else:
				raise TypeError(f"Parameter 'executablePath' is not of type 'Path'.")
		elif binaryDirectoryPath is not None:
			if isinstance(binaryDirectoryPath, Path):
				try:
					executablePath = binaryDirectoryPath / self._executableNames[self._platform]
				except KeyError:
					raise CLIAbstractionException(f"Program is not supported on platform '{self._platform}'.") from PlatformNotSupportedException(self._platform)

				if not binaryDirectoryPath.exists():
					if dryRun:
						self.LogDryRun(f"Directory check for '{binaryDirectoryPath}' failed. [SKIPPING]")
					else:
						raise CLIAbstractionException(f"Binary directory '{binaryDirectoryPath}' not found.") from FileNotFoundError(binaryDirectoryPath)
				elif not executablePath.exists():
					if dryRun:
						self.LogDryRun(f"File check for '{executablePath}' failed. [SKIPPING]")
					else:
						raise CLIAbstractionException(f"Program '{executablePath}' not found.") from FileNotFoundError(executablePath)
			else:
				raise TypeError(f"Parameter 'binaryDirectoryPath' is not of type 'Path'.")
		else:
			raise ValueError(f"Neither parameter 'executablePath' nor 'binaryDirectoryPath' was set.")

		self._executablePath = executablePath
		self.__cliParameters__ = {}

		self.__cliParameters__[self.Executable] = self.Executable(executablePath)

	def __getitem__(self, key):
		return self.__cliOptions__[key]

	def __setitem__(self, key, value):
		if key not in self.__cliOptions__:
			raise KeyError(f"Option '{key}' is not allowed on executable '{self.__class__.__name__}'")
		elif key in self.__cliParameters__:
			raise KeyError(f"Option '{key}' is already set to a value.")

		if issubclass(key, (ValuedFlagArgument, NameValuedCommandLineArgument, TupleArgument)):
			self.__cliParameters__[key] = key(value)
		else:
			self.__cliParameters__[key] = key()

	@CLIOption()
	class Executable(ExecutableArgument, executablePath=None):   # XXX: no argument here
		def __init__(self, executable: Path):
			self._executable = executable

	@property
	def Path(self) -> Path:
		return self._executablePath

	def ToArgumentList(self) -> List[str]:
		result: List[str] = []
		for key, value in self.__cliParameters__.items():
			param = value.AsArgument()
			if isinstance(param, str):
				result.append(param)
			elif isinstance(param, (Tuple, List)):
				result += param
			else:
				raise TypeError(f"")  # XXX: needs error message

		return result

	def __str__(self):
		return "[" + ", ".join([f"\"{item}\"" for item in self.ToArgumentList()]) + "]"
