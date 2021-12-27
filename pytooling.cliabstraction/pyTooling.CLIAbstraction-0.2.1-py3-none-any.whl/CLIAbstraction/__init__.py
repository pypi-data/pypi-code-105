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
# Copyright 2007-2016 Technische Universität Dresden - Germany, Chair of VLSI-Design, Diagnostics and Architecture     #
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
"""Basic abstraction layer for executables."""
__author__ =    "Patrick Lehmann"
__email__ =     "Paebbels@gmail.com"
__copyright__ = "2014-2021, Patrick Lehmann"
__license__ =   "Apache License, Version 2.0"
__version__ =   "0.2.1"
__keywords__ =  ["abstract", "executable", "cli", "cli arguments"]

from pathlib              import Path
from platform             import system
from shutil               import which as shutil_which
from typing               import Dict, Optional, ClassVar, Type, List, Tuple

from pyTooling.Decorators import export
from pyTooling.Exceptions import ExceptionBase, PlatformNotSupportedException
from pyAttributes         import Attribute

from .Argument            import (
	CommandLineArgument, ExecutableArgument,
	ValuedFlagArgument, NameValuedCommandLineArgument, TupleArgument, ValuedCommandLineArgument
)


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
	_platform:         str                                                                      #: Current platform the executable runs on (Linux, Windows, ...)
	_executableNames:  ClassVar[Dict[str, str]]                                                 #: Dictionary of platform specific executable names.
	_executablePath:   Path                                                                     #: The path to the executable (binary, script, ...).
	_dryRun:           bool                                                                     #: True, if program shall run in *dry-run mode*.
	__cliOptions__:    ClassVar[Dict[Type[CommandLineArgument], Optional[CommandLineArgument]]] #: List of all possible CLI options.
	__cliParameters__: Dict[Type[CommandLineArgument], Optional[CommandLineArgument]]           #: List of all CLI parameters (used CLI options).

	def __init_subclass__(cls, *args, **kwargs):
		"""
		Whenever a subclass is derived from :cls:``Program``, all nested classes declared within ``Program`` and which are
		marked with pyAttribute ``CLIOption`` are collected and then listed in the ``__cliOptions__`` dictionary.
		"""
		super().__init_subclass__(*args, **kwargs)

		# register all available CLI options (nested classes marked with attribute 'CLIOption')
		cls.__cliOptions__: Dict[CommandLineArgument, Optional[CommandLineArgument]] = {}
		for option in CLIOption.GetClasses(scope=cls):
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
			try:
				executablePath = Path(self._executableNames[self._platform])
			except KeyError:
				raise CLIAbstractionException(f"Program is not supported on platform '{self._platform}'.") from PlatformNotSupportedException(self._platform)

			resolvedExecutable = shutil_which(str(executablePath))
			if dryRun:
				if resolvedExecutable is None:
					pass
					# XXX: log executable not found in PATH
					# self.LogDryRun(f"Which '{executablePath}' failed. [SKIPPING]")
				else:
					fullExecutablePath = Path(resolvedExecutable)
					if not fullExecutablePath.exists():
						pass
						# XXX: log executable not found
						# self.LogDryRun(f"File check for '{fullExecutablePath}' failed. [SKIPPING]")
			else:
				if resolvedExecutable is None:
					raise CLIAbstractionException(f"Program could not be found in PATH.") from FileNotFoundError(executablePath)

				fullExecutablePath = Path(resolvedExecutable)
				if not fullExecutablePath.exists():
					raise CLIAbstractionException(f"Program '{fullExecutablePath}' not found.") from FileNotFoundError(fullExecutablePath)

			# TODO: log found executable in PATH
			# raise ValueError(f"Neither parameter 'executablePath' nor 'binaryDirectoryPath' was set.")

		self._executablePath = executablePath
		self.__cliParameters__ = {}

		self.__cliParameters__[self.Executable] = self.Executable(executablePath)

	@staticmethod
	def _NeedsParameterInitialization(key):
		return issubclass(key, (ValuedFlagArgument, ValuedCommandLineArgument, NameValuedCommandLineArgument, TupleArgument))

	def __getitem__(self, key):
		"""Access to a CLI parameter by CLI option (key must be of type :cls:`CommandLineArgument`), which is already used."""
		if not issubclass(key, CommandLineArgument):
			raise TypeError(f"")  #: needs error message

		# TODO: is nested check
		return self.__cliParameters__[key]

	def __setitem__(self, key, value):
		if key not in self.__cliOptions__:
			raise KeyError(f"Option '{key}' is not allowed on executable '{self.__class__.__name__}'")
		elif key in self.__cliParameters__:
			raise KeyError(f"Option '{key}' is already set to a value.")

		if self._NeedsParameterInitialization(key):
			self.__cliParameters__[key] = key(value)
		else:
			self.__cliParameters__[key] = key()

	@CLIOption()
	class Executable(ExecutableArgument):   # XXX: no argument here
		...

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

	def __repr__(self):
		return "[" + ", ".join([f"\"{item}\"" for item in self.ToArgumentList()]) + "]"

	def __str__(self):
		return " ".join([f"\"{item}\"" for item in self.ToArgumentList()])
