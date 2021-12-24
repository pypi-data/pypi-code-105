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
This module contains all possible command line option and parameter forms.
"""
from pathlib import Path
from typing import ClassVar, Optional, List, Union, Iterable

from pyTooling.Decorators import export


@export
class CommandLineArgument():
	"""Base-class (and meta-class) for all *Arguments* classes."""

	_pattern: ClassVar[str]

	def __init_subclass__(cls, *args, pattern: str = None, **kwargs):
		super().__init_subclass__(*args, **kwargs)
		cls._pattern = pattern

	# def __new__(mcls, name, bases, nmspc):
	# 	print("CommandLineArgument.new: %s - %s" % (name, nmspc))
	# 	return super(CommandLineArgument, mcls).__new__(mcls, name, bases, nmspc)

	def AsArgument(self) -> Union[str, Iterable[str]]:
		raise NotImplementedError(f"")  # XXX: add message here

	def __str__(self) -> str:
		raise NotImplementedError(f"")  # XXX: add message here


@export
class ExecutableArgument(CommandLineArgument):
	"""Represents the executable."""

	_executable: ClassVar[Path]

	def __init_subclass__(cls, *args, executablePath: Path, **kwargs):
		super().__init_subclass__(*args, **kwargs)
		cls._executable = executablePath

	@property
	def Value(self) -> Path:
		return self._executable

	@Value.setter
	def Value(self, value: Path):
		if isinstance(value, Path):
			self._executable = value
		else:
			raise TypeError("Parameter 'value' is not of type 'Path'.")

	@property
	def Executable(self) -> Path:
		return self._executable

	@Executable.setter
	def Executable(self, value):
		if isinstance(value, Path):
			self._executable = value
		else:
			raise TypeError("Parameter 'value' is not of type 'Path'.")

	def AsArgument(self) -> Union[str, Iterable[str]]:
		return f"{self._executable}"

	def __str__(self):
		return f"\"{self.AsArgument()}\""


@export
class NamedCommandLineArgument(CommandLineArgument, pattern="{0}"):
	"""Base class for all command line arguments with a name."""
	_name: ClassVar[str]

	def __init_subclass__(cls, *args, name: str = None, pattern: str = "{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)
		cls._name = name

	@property
	def Name(self) -> str:
		if self._name is None:
			raise ValueError(f"")  # XXX: add message

		return self._name

	def AsArgument(self) -> Union[str, Iterable[str]]:
		if self._name is None:
			raise ValueError(f"")  # XXX: add message

		return self._pattern.format(self._name)

	def __str__(self):
		return f"\"{self.AsArgument()}\""


@export
class ValuedCommandLineArgument(CommandLineArgument):
	"""Base class for all command line arguments with a value."""
	_value: str

	def __init__(self, value: str):
		if value is None:
			raise ValueError(f"")  # XXX: add message

		self._value = value

	@property
	def Value(self) -> str:
		return self._value

	@Value.setter
	def Value(self, value: str) -> None:
		if value is None:
			raise ValueError(f"")  # XXX: add message

		self._value = value

	def AsArgument(self) -> Union[str, Iterable[str]]:
		if self._name is None:
			raise ValueError(f"")  # XXX: add message

		return self._pattern.format(self._value)

	def __str__(self):
		return f"\"{self.AsArgument()}\""


class NameValuedCommandLineArgument(NamedCommandLineArgument):
	"""Base class for all command line arguments with a name."""
	_value: str

	# def __init_subclass__(cls, *args, name: str = None, **kwargs):
	# 	super().__init_subclass__(*args, **kwargs)
	# 	cls._name = name

	def __init__(self, value: str):
		if value is None:
			raise ValueError(f"")  # XXX: add message

		self._value = value

	@property
	def Value(self) -> str:
		return self._value

	@Value.setter
	def Value(self, value: str) -> None:
		if value is None:
			raise ValueError(f"")  # XXX: add message

		self._value = value

	def AsArgument(self) -> Union[str, Iterable[str]]:
		if self._name is None:
			raise ValueError(f"")  # XXX: add message

		return self._pattern.format(self._name, self._value)

	def __str__(self):
		return f"\"{self.AsArgument()}\""


class NamedTupledCommandLineArgument(NamedCommandLineArgument):
	"""Base class for all command line arguments with a name."""
	_valuePattern: ClassVar[str]
	_value: str

	def __init_subclass__(cls, *args, valuePattern: str="{0}", **kwargs):
		super().__init_subclass__(*args, **kwargs)
		cls._valuePattern = valuePattern

	def __init__(self, value: str):
		if value is None:
			raise ValueError(f"")  # XXX: add message

		self._value = value

	@property
	def ValuePattern(self) -> str:
		if self._valuePattern is None:
			raise ValueError(f"")  # XXX: add message

		return self._valuePattern

	@property
	def Value(self) -> str:
		return self._value

	@Value.setter
	def Value(self, value: str) -> None:
		if value is None:
			raise ValueError(f"")  # XXX: add message

		self._value = value

	def AsArgument(self) -> Union[str, Iterable[str]]:
		if self._name is None:
			raise ValueError(f"")  # XXX: add message

		return (
			self._pattern.format(self._name),
			self._valuePattern.format(self._value)
		)

	def __str__(self):
		return ", ".join([f"\"{item}\"" for item in self.AsArgument()])


@export
class CommandArgument(NamedCommandLineArgument):
	"""Represents a command name.

	It is usually used to select a sub parser in a CLI argument parser or to hand
	over all following parameters to a separate tool. An example for a command is
	'checkout' in ``git.exe checkout``, which calls ``git-checkout.exe``.
	"""


@export
class ShortCommandArgument(CommandArgument, pattern="-{0}"):
	"""Represents a command name with a single dash."""

	def __init_subclass__(cls, *args, pattern="-{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class LongCommandArgument(CommandArgument, pattern="--{0}"):
	"""Represents a command name with a double dash."""

	def __init_subclass__(cls, *args, pattern="--{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class WindowsCommandArgument(CommandArgument, pattern="/{0}"):
	"""Represents a command name with a single slash."""

	def __init_subclass__(cls, *args, pattern="/{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class StringArgument(ValuedCommandLineArgument, pattern="{0}"):
	"""Represents a simple string argument."""

	def __init_subclass__(cls, *args, pattern="{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


# @export
# class StringListArgument(CommandLineArgument):
# 	"""Represents a list of string arguments."""
# 	_pattern =  "{0}"
#
# 	@property
# 	def Value(self):
# 		return self._value
#
# 	@Value.setter
# 	def Value(self, value):
# 		if (value is None):           self._value = None
# 		elif isinstance(value, (tuple, list)):
# 			self._value = []
# 			try:
# 				for item in value:        self._value.append(str(item))
# 			except TypeError as ex:     raise ValueError("Item '{0}' in parameter 'value' cannot be converted to type str.".format(item)) from ex
# 		else:                         raise ValueError("Parameter 'value' is no list or tuple.")
#
# 	def __str__(self):
# 		if (self._value is None):     return ""
# 		elif self._value:             return " ".join([self._pattern.format(item) for item in self._value])
# 		else:                         return ""
#
# 	def AsArgument(self):
# 		if (self._value is None):      return None
# 		elif self._value:              return [self._pattern.format(item) for item in self._value]
# 		else:                          return None


# @export
# class PathArgument(CommandLineArgument):
# 	"""Represents a path argument.
#
# 	The output format can be forced to the POSIX format with :py:data:`_PosixFormat`.
# 	"""
# 	_PosixFormat = False
#
# 	@property
# 	def Value(self):
# 		return self._value
#
# 	@Value.setter
# 	def Value(self, value):
# 		if (value is None):              self._value = None
# 		elif isinstance(value, Path):    self._value = value
# 		else:                            raise ValueError("Parameter 'value' is not of type Path.")
#
# 	def __str__(self):
# 		if (self._value is None):        return ""
# 		elif (self._PosixFormat):        return "\"" + self._value.as_posix() + "\""
# 		else:                            return "\"" + str(self._value) + "\""
#
# 	def AsArgument(self):
# 		if (self._value is None):        return None
# 		elif (self._PosixFormat):        return self._value.as_posix()
# 		else:                            return str(self._value)


@export
class FlagArgument(NamedCommandLineArgument):
	"""Base class for all FlagArgument classes, which represents a simple flag argument.

	A simple flag is a single boolean value (absent/present or off/on) with no data.
	"""


@export
class ShortFlagArgument(FlagArgument, pattern="-{0}"):
	"""Represents a flag argument with a single dash.

	Example: ``-optimize``
	"""
	def __init_subclass__(cls, *args, pattern="-{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class LongFlagArgument(FlagArgument, pattern="--{0}"):
	"""Represents a flag argument with a double dash.

	Example: ``--optimize``
	"""
	def __init_subclass__(cls, *args, pattern="--{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class WindowsFlagArgument(FlagArgument, pattern="/{0}"):
	"""Represents a flag argument with a single slash.

	Example: ``/optimize``
	"""
	def __init_subclass__(cls, *args, pattern="/{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class ValuedFlagArgument(NameValuedCommandLineArgument, pattern="{0}={1}"):
	"""Class and base class for all ValuedFlagArgument classes, which represents a flag argument with data.

	A valued flag is a flag name followed by a value. The default delimiter sign is equal (``=``). Name and
	value are passed as one arguments to the executable even if the delimiter sign is a whitespace character.

	Example: ``width=100``
	"""
	def __init_subclass__(cls, *args, pattern="{0}={1}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class ShortValuedFlagArgument(ValuedFlagArgument, pattern="-{0}={1}"):
	"""Represents a :py:class:`ValuedFlagArgument` with a single dash.

	Example: ``-optimizer=on``
	"""
	def __init_subclass__(cls, *args, pattern="-{0}={1}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class LongValuedFlagArgument(ValuedFlagArgument, pattern="--{0}={1}"):
	"""Represents a :py:class:`ValuedFlagArgument` with a double dash.

	Example: ``--optimizer=on``
	"""
	def __init_subclass__(cls, *args, pattern="--{0}={1}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class WindowsValuedFlagArgument(ValuedFlagArgument, pattern="/{0}:{1}"):
	"""Represents a :py:class:`ValuedFlagArgument` with a single slash.

	Example: ``/optimizer:on``
	"""
	def __init_subclass__(cls, *args, pattern="/{0}:{1}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class OptionalValuedFlagArgument(NameValuedCommandLineArgument):
	"""Class and base class for all OptionalValuedFlagArgument classes, which represents a flag argument with data.

	An optional valued flag is a flag name followed by a value. The default delimiter sign is equal (``=``).
	Name and value are passed as one arguments to the executable even if the delimiter sign is a whitespace
	character. If the value is None, no delimiter sign and value is passed.

	Example: ``width=100``
	"""
	_patternWithValue: ClassVar[str]

	def __init_subclass__(cls, *args, patternWithValue: str = "{0}={1}", **kwargs):
		super().__init_subclass__(*args, **kwargs)
		cls._patternWithValue = patternWithValue

	def __init__(self, value: str = None):
		self._value = value

	@property
	def Value(self) -> Optional[str]:
		return self._value

	@Value.setter
	def Value(self, value: str = None) -> None:
		self._value = value

	def AsArgument(self) -> Union[str, Iterable[str]]:
		if self._name is None:
			raise ValueError(f"")  # XXX: add message

		pattern = self._pattern if self._value is None else self._patternWithValue
		return pattern.format(self._name, self._value)

	def __str__(self):
		return f"\"{self.AsArgument()}\""


@export
class ShortOptionalValuedFlagArgument(OptionalValuedFlagArgument, pattern="-{0}", patternWithValue="-{0}={1}"):
	"""Represents a :py:class:`OptionalValuedFlagArgument` with a single dash.

	Example: ``-optimizer=on``
	"""
	def __init_subclass__(cls, *args, pattern="-{0}", patternWithValue="-{0}={1}", **kwargs):
		kwargs["pattern"] = pattern
		kwargs["patternWithValue"] = patternWithValue
		super().__init_subclass__(*args, **kwargs)


@export
class LongOptionalValuedFlagArgument(OptionalValuedFlagArgument, pattern="--{0}", patternWithValue="--{0}={1}"):
	"""Represents a :py:class:`OptionalValuedFlagArgument` with a double dash.

	Example: ``--optimizer=on``
	"""
	def __init_subclass__(cls, *args, pattern="--{0}", patternWithValue="--{0}={1}", **kwargs):
		kwargs["pattern"] = pattern
		kwargs["patternWithValue"] = patternWithValue
		super().__init_subclass__(*args, **kwargs)


@export
class WindowsOptionalValuedFlagArgument(OptionalValuedFlagArgument, pattern="/{0}", patternWithValue="/{0}:{1}"):
	"""Represents a :py:class:`OptionalValuedFlagArgument` with a single slash.

	Example: ``/optimizer:on``
	"""
	def __init_subclass__(cls, *args, pattern="/{0}", patternWithValue="/{0}:{1}", **kwargs):
		kwargs["pattern"] = pattern
		kwargs["patternWithValue"] = patternWithValue
		super().__init_subclass__(*args, **kwargs)


# @export
# class ValuedFlagListArgument(NamedCommandLineArgument):
# 	"""Class and base class for all ValuedFlagListArgument classes, which represents a list of :py:class:`ValuedFlagArgument` instances.
#
# 	Each list item gets translated into a :py:class:`ValuedFlagArgument`, with the same flag name, but differing values. Each
# 	:py:class:`ValuedFlagArgument` is passed as a single argument to the executable, even if the delimiter sign is a whitespace
# 	character.
#
# 	Example: ``file=file1.txt file=file2.txt``
# 	"""
# 	_pattern = "{0}={1}"
#
# 	@property
# 	def Value(self):
# 		return self._value
#
# 	@Value.setter
# 	def Value(self, value):
# 		if (value is None):                    self._value = None
# 		elif isinstance(value, (tuple,list)):  self._value = value
# 		else:                                  raise ValueError("Parameter 'value' is not of type tuple or list.")
#
# 	def __str__(self):
# 		if (self._value is None):     return ""
# 		elif (len(self._value) > 0):  return " ".join([self._pattern.format(self._name, item) for item in self._value])
# 		else:                         return ""
#
# 	def AsArgument(self):
# 		if (self._value is None):     return None
# 		elif (len(self._value) > 0):  return [self._pattern.format(self._name, item) for item in self._value]
# 		else:                         return None


# @export
# class ShortValuedFlagListArgument(ValuedFlagListArgument):
# 	"""Represents a :py:class:`ValuedFlagListArgument` with a single dash.
#
# 	Example: ``-file=file1.txt -file=file2.txt``
# 	"""
# 	_pattern = "-{0}={1}"
#
#
# @export
# class LongValuedFlagListArgument(ValuedFlagListArgument):
# 	"""Represents a :py:class:`ValuedFlagListArgument` with a double dash.
#
# 	Example: ``--file=file1.txt --file=file2.txt``
# 	"""
# 	_pattern = "--{0}={1}"
#
#
# @export
# class WindowsValuedFlagListArgument(ValuedFlagListArgument):
# 	"""Represents a :py:class:`ValuedFlagListArgument` with a single slash.
#
# 	Example: ``/file:file1.txt /file:file2.txt``
# 	"""
# 	_pattern = "/{0}:{1}"

# XXX: delimiter argument "--"

@export
class TupleArgument(NamedCommandLineArgument):
	"""Class and base class for all TupleArgument classes, which represents a switch with separate data.

	A tuple switch is a command line argument followed by a separate value. Name and value are passed as
	two arguments to the executable.

	Example: ``width 100``
	"""
	_valuePattern: ClassVar[str]
	_value: str

	def __init_subclass__(cls, *args, valuePattern: str = "{0}", **kwargs):
		super().__init_subclass__(*args, **kwargs)
		cls._valuePattern = valuePattern

	def __init__(self, value: str):
		if value is None:
			raise ValueError(f"")  # XXX: add message

		self._value = value

	@property
	def Value(self) -> str:
		return self._value

	@Value.setter
	def Value(self, value: str) -> None:
		if value is None:
			raise ValueError(f"")  # XXX: add message

		self._value = value


@export
class ShortTupleArgument(TupleArgument, pattern="-{0}"):
	"""Represents a :py:class:`TupleArgument` with a single dash in front of the switch name.

	Example: ``-file file1.txt``
	"""
	def __init_subclass__(cls, *args, pattern="-{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)

@export
class LongTupleArgument(TupleArgument, pattern="--{0}"):
	"""Represents a :py:class:`TupleArgument` with a double dash in front of the switch name.

	Example: ``--file file1.txt``
	"""
	def __init_subclass__(cls, *args, pattern="--{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)


@export
class WindowsTupleArgument(TupleArgument, pattern="/{0}"):
	"""Represents a :py:class:`TupleArgument` with a single slash in front of the switch name.

	Example: ``/file file1.txt``
	"""
	def __init_subclass__(cls, *args, pattern="/{0}", **kwargs):
		kwargs["pattern"] = pattern
		super().__init_subclass__(*args, **kwargs)
