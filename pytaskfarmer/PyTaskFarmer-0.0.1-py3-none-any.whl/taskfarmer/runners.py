# subprocess for execution
import subprocess
# configparser for parsing configuration files
import configparser
# glob for finding runner configurations
import glob
# importlib for loading runners from configuration files
import importlib
# mkdtemp for temporary workdirs
import tempfile
# os for environment
import os

class RunnerManager:
    """
    Loads runner definitions from INI files

    The formatting of the INI file is expected to be as follows
    ```ini
    [runnername]
    Runner = runner.python.class
    arg0 = value0
    arg1 = value1
    ```

    There can be multiple runners which are refered to by name (ie: `runnername` in 
    the above example.

    The `Runner` key is the `Runner` class to use. The remaining arguments are
    passed to the constructor.
    """
    def __init__(self):
        self.runners={
            'default': BasicRunner()
        }

    def load_directory(self, dirpath):
        """
        Loads runners in all `*.ini` files located inside `dirpath`.

        Parameters:
         - dirpath (str): Path to directory with runner configurations
        """
        for cfgpath in glob.glob(dirpath+'/*.ini'):
            self.load(cfgpath)

    def load(self, cfgpath):
        """
        Add runners defined inside `cfgpath` to manager.

        Parameters:
         - cfgpath (str): Path to INI file with runner definitions.
        """
        cfg=configparser.ConfigParser()
        cfg.optionxform = str
        cfg.read(cfgpath)
        
        for rname in cfg.sections():
            info=cfg[rname]
            if 'Runner' not in info:
                continue # this is not a runner deifnition
            parts=info.pop('Runner').split('.')
            module='.'.join(parts[:-1])
            classn=parts[-1]
            m = importlib.import_module(module)
            c = getattr(m, classn)

            self.runners[rname]=c(**info)

    def runner(self, rname):
        """
        Get runner information for runner named `rname`.
        """
        return self.runners[rname]

class Runner:
    """
    A runner is used to execute a given task.

    All runners should inhert from this class and implement the `run`
    and `terminate` functions.
    """
    def __init__(self):
        pass

    def run(self, taskid, command, logfh):
        """
        All runners should implement this function.

        Parameters:
         - taskid (int): ID of the task
         - command (str): Task command to execute.
         - logfh (file handle): Stream for saving task output.

        Returns: Return code of task (0 on success, other value on failure).
        """
        pass

    def terminate(self):
        """
        Terminate the current running command.
        """
        pass

class BasicRunner(Runner):
    """
    Simple runner that runs a command.
    """
    def __init__(self):
        super().__init__()

        self.execute=None
        
    def run(self, taskid, command, logfh):
        """
        Execute command using `subprocess.Popen`.
        """

        my_env = os.environ
        my_env['PROC_NUMBER'] = str(taskid)

        self.execute = subprocess.Popen(command.split(),stdin=None,stdout=logfh,stderr=logfh,env=my_env)
        self.execute.communicate()

        return self.execute.returncode

    def terminate(self):
        if self.execute is None:
            return
        self.execute.kill()

class ShifterRunner(Runner):
    """
    Run each task inside shifter.

    Each task to be executed in its own shifter instance. This is
    so pytaskfarmer does not have to be installed inside each
    user image.
    """

    def __init__(self, image, setup='', volumes='', modules='', tempdir=False):
        """
        Parameters:
         - image (str): Name of shfter image
         - setup (str): Setup command to run before executing task
         - volumes (str): list of volume bindings separated by space
         - modules (str): list of modules separated by space
         - tempdir (bool): each task should be run in own temporary directory
        """
        super().__init__()

        self.image=image
        self.setup=setup

        self.execute=None
        self.volumes=volumes.split()
        self.modules=modules.split()

        self.tempdir = tempdir is True or tempdir=='True'

    def run(self, taskid, command, logfh):
        """
        The `command` is executed via `shifter`.
        """

        thecommand=self.setup+' && '+command
        command=['shifter','--image',self.image]
        if self.tempdir:
            command+=['--workdir={}'.format(tempfile.mkdtemp())]
        command+=[f'-V{volume}' for volume in self.volumes]
        command+=[f'-m{module}' for module in self.modules]
        command+=['--','/bin/bash','-c',thecommand]

        myenv=os.environ.copy()
        myenv['BASH_ENV']=''

        self.execute = subprocess.Popen(command,stdin=None,stdout=logfh,stderr=logfh,env=myenv)
        self.execute.communicate()

        return self.execute.returncode

    def terminate(self):
        if self.execute is None:
            return
        self.execute.kill()
