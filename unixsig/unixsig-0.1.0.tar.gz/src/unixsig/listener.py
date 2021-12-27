# MIT License
#
# Copyright (c) 2021 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import signal


class Listener():
    """Listener Class"""

    class __Listener():
        """Listener Inner Class"""
        def __init__(self):
            self.sigs = set()

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        """Class Constructor"""
        if not Listener.instance:
            Listener.instance = Listener.__Listener()
            signal.signal(signal.SIGHUP, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGINT, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGQUIT, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGILL, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGTRAP, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGABRT, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGBUS, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGFPE, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGUSR1, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGSEGV, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGUSR2, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGPIPE, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGALRM, lambda sig, frame: Listener.instance.sigs.add(sig))
            signal.signal(signal.SIGTERM, lambda sig, frame: Listener.instance.sigs.add(sig))

    def add(self, sig):
        """
        Add a new received signal

        Args:
            sig: The signal
        """
        Listener.instance.sigs.add(sig)

    def is_received(self, sig):
        """
        Check if a signal got received

        Args:
            sig: The received signal

        Returns:
            A boolean representing if the signal got received or not
        """
        return sig in Listener.instance.sigs

    def get(self):
        """
        Gets all received signals

        Returns:
            A set of received signals
        """
        return Listener.instance.sigs

    def discard(self, sig):
        """
        Removes a received signals

        Args:
            sig: The received signal
        """
        return Listener.instance.sigs.discard(sig)

    def getpid(self):
        """
        Get Process ID

        Returns:
            The process ID
        """
        return os.getpid()
