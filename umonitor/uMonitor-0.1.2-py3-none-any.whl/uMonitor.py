import time
import json
import argparse
import os
from subprocess import Popen, PIPE
import sys
import signal 
import copy
import re

class uMonitor:
    """ Runs and monitors child processes according given a json config."""

    def __init__(self, config):
        '''Init the monitor config.
        Args:
            config: str
            Path to json config for the current uMonitor process.
        '''
        self.processes = dict()
        with open(config) as cfg_file:
            try:
                content = cfg_file.read()
                content = self._substitute_variables(content)
                self.config  = json.loads(content)
            except Exception as e:
                print("Unable to parse config: ", e.args)
                exit(1)

    def __del__(self):
        '''Correctly kill child processes when used
        as a python context manager.
        '''
        self._kill()

    def __enter__(self):
        '''When the object is used as a context manager, 
        this method will be called. No need for extra logic here.
        '''
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
         self._kill()

    def _kill(self):
        ''' Kill child processes.
        '''
        for proc_tup, service in self.processes.items():
            proc = service.get("proc")
            if proc:
                proc.kill()
                proc.communicate()
                print("Killed: {}".format(proc_tup))
        self.processes = dict()

    def _substitute_variables(self, expression):
        '''Find sentences like ${varname},
        and substitute it with environment variable
        varname value.
        args:
        expression: str
            expression to substitute in.
        '''
        variables = set(re.findall(
                r"(?<=\${)[^}]*(?=})",
                expression
                ))
        for var in variables:
            expression = re.sub(
                "\$\{"+var+"\}", 
                os.environ.get(var, ""), 
                expression)
        return expression

    def _service_vars(self, service):
        '''Join variables provided in service with 
        the corresponding environment variables.
        args:
        service: dict
            A dictionary-like object, containing "env" key.
            Watch for any "service" object in the config_example.
        '''
        osenv = copy.copy(os.environ)
        for k, v in service.get("env", dict()).items():
            usrval = ":".join(v)
            osval = osenv.get(k, "")
            osenv[k] = ":".join(filter(len, [usrval, osval]))
        return osenv

    def _service_to_tup(self, service):
        '''Map service dictionary to a tuple.
        This tuple is then used as a hashable object
        to access this service at runtime.
        '''
        program = self.config["interpreters"].get(
            service["program"],
            service["program"]
            )
        return (program,)+tuple(service["args"])

    def _add_process(self, service):
        ''' Creates a process, for a given service
        specification. The executable is being mapped 
        from the "interpreters" json section. 
        Child process environment is also changed to 
        what user provided through the json config.
        '''
        service_tuple = self._service_to_tup(service)
        self.processes[service_tuple] = service
        ser_env = self._service_vars(service)
        proc = Popen(
                    service_tuple, 
                    cwd = service.get("cwd", os.getcwd()),
                    env=ser_env ,
                    stdin=PIPE, 
                    stdout=PIPE,
                    stderr=PIPE
                )
        service["proc"] = proc 
        print("Started: {}".format(service_tuple))

    def _launch_services(self):
        '''Creates child process for all the 
        given services. Services should be described
        in the __init__ config.
        '''
        services = self.config["services"]
        for service in services:
            self._add_process(service)

    def run(self):
        '''The only method, user supposed to run.
        Will create the child processes and monitor their
        execution.
        '''
        self._launch_services()
        while True:
            time.sleep(1)
            for ser_tup, service in self.processes.items():
                proc = service.get("proc")
                if (not proc) or (proc.poll() != None): 
                    if service.get("persist", False):
                        self._add_process(service)
                    else:
                        self.processes[ser_tup]["proc"] = None
                        print("Terminated: ", ser_tup)
            self.processes = dict(filter(
                lambda kv: kv[1]["proc"],  
                self.processes.items()
                ))
                       


