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
from subprocess           import Popen				as Subprocess_Popen
from subprocess           import PIPE					as Subprocess_Pipe
from subprocess           import STDOUT				as Subprocess_StdOut

from pyTooling.Decorators import export

from . import CLIAbstractionException, DryRunException, Program


@export
class Environment:
	def __init__(self):
		self.Variables = {}


@export
class Executable(Program):  # (ILogable):
	"""Represent an executable."""
	_pyIPCMI_BOUNDARY = "====== pyIPCMI BOUNDARY ======"

	def __init__(self, environment: Environment = None):

		self._process =  None
		self._iterator = None

	def StartProcess(self, parameterList):
		# start child process
		# parameterList.insert(0, str(self._executablePath))
		if (not self._dryRun):
			if (self._environment is not None):
				envVariables = self._environment.Variables
			else:
				envVariables = None

			try:
				self._process = Subprocess_Popen(
					parameterList,
					stdin=Subprocess_Pipe,
					stdout=Subprocess_Pipe,
					stderr=Subprocess_StdOut,
					env=envVariables,
					universal_newlines=True,
					bufsize=256
				)
			except OSError as ex:
				raise CLIAbstractionException(f"Error while accessing '{self._executablePath}'.") from ex
		else:
			self.LogDryRun("Start process: {0}".format(" ".join(parameterList)))

	def Send(self, line, end="\n"):
		self._process.stdin.write(line + end)
		self._process.stdin.flush()

	def SendBoundary(self):
		self.Send("puts \"{0}\"".format(self._pyIPCMI_BOUNDARY))

	def Terminate(self):
		self._process.terminate()

	def GetReader(self):
		if (not self._dryRun):
			try:
				for line in iter(self._process.stdout.readline, ""):
					yield line[:-1]
			except Exception as ex:
				raise ex
			# finally:
				# self._process.terminate()
		else:
			raise DryRunException()  # XXX: needs a message

	def ReadUntilBoundary(self, indent=0):
		__indent = "  " * indent
		if (self._iterator is None):
			self._iterator = iter(self.GetReader())

		for line in self._iterator:
			print(__indent + line)
			if (self._pyIPCMI_BOUNDARY in line):
				break
		self.LogDebug("Quartus II is ready")
