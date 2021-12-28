import time,os
# fcntl to deal with file locks
from fcntl import flock,LOCK_EX,LOCK_NB,LOCK_UN
# hashlib to generate lock file paths
from hashlib import md5
# configparser for parsing configuration files
import configparser
# glob for finding runner configurations
import glob
# importlib for loading runners from configuration files
import importlib


# This assumes $SCRATCH points to a disk area that supports file locking
# Here is a little helper for many other file systems
if   'SCRATCH' in os.environ: lock_area = os.environ['SCRATCH']+'/' # Cori!
elif 'TMP'     in os.environ: lock_area = os.environ['TMP']+'/'
elif 'TMPDIR'  in os.environ: lock_area = os.environ['TMPDIR']+'/'
else: lock_area = None # Really didn't define anything...

class TaskListManager:
    """
    Loads tasklist definitions from INI files

    The formatting of the INI file is expected to be as follows
    ```ini
    [tasklistname]
    TaskList = task.python.class
    arg0 = value0
    arg1 = value1
    ```

    There can be multiple tasklists which are refered to by name 
    (ie: `tasklistname`) in the above example.

    The `TaskList` key is the `TaskList` class to use. The remaining
    arguments are passed to the constructor.
    """
    def __init__(self):
        self.tasklists={
            'default': {'class': ListTaskList}
        }

    def load_directory(self, dirpath):
        """
        Loads runners in all `*.ini` files located inside `dirpath`.

        Parameters:
         - dirpath (str): Path to directory with tasklist configurations
        """
        for cfgpath in glob.glob(dirpath+'/*.ini'):
            self.load(cfgpath)

    def load(self, cfgpath):
        """
        Add tasklists defined inside `cfgpath` to manager.

        Parameters:
         - cfgpath (str): Path to INI file with tasklist definitions.
        """
        cfg=configparser.ConfigParser()
        cfg.optionxform = str
        cfg.read(cfgpath)
        
        for tname in cfg.sections():
            info=cfg[tname]
            if 'TaskList' not in info:
                continue # this is not a tasklist deifnition
            parts=info.pop('TaskList').split('.')
            module='.'.join(parts[:-1])
            classn=parts[-1]
            m = importlib.import_module(module)
            c = getattr(m, classn)

            self.tasklists[tname]={'class': c, 'args':info}

    def tasklist(self, tname, tasklistpath, workdir):
        """
        Get tasklist named `tname` contaning tasks in path
        `tasklistpath`.

        Parameters:
         - tname (str): Name of task list handler to use
         - tasklistpath (str): Path to file defining tasks
         - workdir (str): Path to work directory. Must exist.
        """
        tdef=self.tasklists[tname]
        return tdef['class'](tasklistpath,workdir,**tdef.get('args', {}))

class TaskList:
    """
    Abstract definition of a task list.

    A task list keeps track of available tasks in a process-safe manner.

    A task can either be unprocessed (aka `toprocess`) or completed
    (aka `done`). It is referred to by a task ID.

    There are no official requirements on what a task is. However most runners
    expect it to be a command that can be executed.

    The path containing the definition of tasks is provided to the constructor. It
    is up to the implementation to parse it.

    A work directory is provided that stores the progress and log files for a
    given run over the tasklist.

    The `workdir` also contains a `lock` file. The `flock` status of this file 
    controls exclusive access to all work files. This is handled by the `lock`/`unlock`
    functions. If the filesystem does not support file locking, an alternate path
    can be used via a global `lock_area` variable. In this case, the `lock` path
    becomes `lock_area/md5(absolute path of workdir)_lock`.

    All functions defined in this class should be implemented in
    subclasses.
    """
    def __init__(self,path,workdir):
        """
        Parameters:
         - path (str): Path to task definition.
         - workdir (str): Path to work directory.
        """

        # Lock file handle on the task list
        self.lockfh=None

        # Paths to all necessary files
        self.workdir=workdir
        self.path=path

        if lock_area==None:
            self.path_lock =workdir+"/lock"
        else:
            abspath=os.path.abspath(workdir)
            pathhash=md5(abspath.encode()).hexdigest()
            self.path_lock =lock_area+'/'+pathhash+'_lock'

    def lock(self):
        """
        Get exclusive lock on the work directory
        """
        if self.lockfh!=None and not self.lockfh.closed:
            return # I already have lock
        self.lockfh = open( self.path_lock,'w+' )

        for i in range(10000):
            try:
                flock( self.lockfh , LOCK_EX | LOCK_NB )
                return
            except IOError: # lock not acquired
                time.sleep(0.001)

        self.lockfh.close()
        self.lockfh=None
        print(time.asctime(),'Lock error...')
        raise RuntimeError("Unable to lock after 10 seconds. Something is wrong!")

    def unlock(self):
        """
        Release lock on the work directory
        """
        if self.lockfh==None or self.lockfh.closed:
            return # No more lock
        self.lockfh.close()
        self.lockfh=None

    def get_finished(self):
        """
        Returns: List of task id's corresponding to finished tasks.
        """
        pass

    def pop_task(self):
        """
        Pop a task from the to-process list 

        Returns: task id for the removed task
        """
        pass

    def record_toprocess_task(self, taskid):
        """
        Record a task that is not processed

        Parameters:
         - taskid (int): Task ID of toprocess task
        """
        pass

    def record_done_task(self, taskid, returncode):
        """
        Record a completed task

        Parameters:
         - taskid (int): Task ID of completed task
         - returncode(int): Return code of the task to determine finished/failed
        """
        pass   

    def __getitem__(self, taskid):
        """
        Return information required to run task `taskid` by a runner.

        Parameters:
         - taskid (int): Task ID of task to look-up
        """
        pass
    
    def __len__(self):
        """
        Return number of tasks in the task list.
        """
        pass

class ListTaskList(TaskList):
    """
    A list of tasks is defined using a file containing a task per line,
    with supporting status files defined using a suffix. The task ID is
    defined as the line number (starting at 0) inside the main task file.

    Subclasses can implement the `__getitem__` function to futher modify
    the task definitions. The original line/task content is stored in
    the `tasks` member variable. By default, the `tasks[taskid]` is 
    returned unmodified.

    All supporting status files are stored inside the working directory. The
    used files are:
    - `toprocess`: List of tasks that still need to be processed. The format is
      "taskID task".
    - `finished`: List of tasks that succesfully finished (return code 0). The
      format is "taskID task".
    - `failed`: List of tasks that finished unsuccesfully (return code not 0).
      The format is "taskID task".

    The list and corresponding operations are defined in a process-safe manner using
    the supporting files to synchronize the state. This means that multiple `ListTaskLists`
    can be created for a single tasklist (even on multiple machines with a shared filesystem).
    """
    def __init__(self,path,workdir):
        """
        Parameters:
         path (str): Path to tasklist.
         workdir (str): Path to work directory.
        """
        super().__init__(path,workdir)

        # Paths to all necessary files
        self.path_toprocess=workdir+"/toprocess"
        self.path_finished =workdir+"/finished"
        self.path_failed   =workdir+"/failed"

        # Load complete list of tasks
        in_tasks = open(path,'r')
        self.tasks = [line.strip() for line in in_tasks.readlines() if not line.startswith('#') and line.strip()!='']
        in_tasks.close()

    def __len__(self):
        """
        Return length of `tasks`
        """
        return len(self.tasks)

    def get_finished(self):
        """
        Thread-safe alias for `read_finished`
        """

        self.lock()
        tasks=self.read_finished()
        self.unlock()
        return tasks

    def pop_task(self):
        """
        Pop a task from the toprocess list 

        Returns: task id for the removed task
        """
        nexttask=None

        # Get list of unfinished tasks
        self.lock()        
        tasks_toprocess=self.read_toprocess()
        if len(tasks_toprocess)>0:
            nexttask=tasks_toprocess.pop()
            self.write_toprocess(tasks_toprocess)
        self.unlock()

        return nexttask

    def __getitem__(self, taskid):
        """
        Return the contents of line `taskid`.
        """
        return self.tasks[taskid]

    def record_toprocess_task(self, taskid):
        """
        Record a task that is not processed

        Parameters:
         - taskid (int): Task ID of toprocess task
        """

        self.lock()

        # Unfinished task list
        tasks=self.read_toprocess()
        tasks.add(taskid)
        # Save
        self.write_toprocess(tasks)
        
        self.unlock()
    
    def record_done_task(self, taskid, returncode):
        """
        Record a completed task

        Parameters:
         - taskid (int): Task ID of completed task
         - returncode(int): Return code of the task to determine finished/failed
        """
        self.lock()

        # Deterine output path
        path = self.path_finished if returncode==0 else self.path_failed
        # Open the task list
        finished = open( path,'a+' )
        # Write the command on its own line
        finished.write('{} {}\n'.format(taskid, self.tasks[taskid]))
        # Close finished task list
        finished.close()

        self.unlock()

    def read_toprocess(self):
        """"
        Get set of toprocess tasks

        Warning: Not thread safe!

        Returns: set of toprocess task id's
        """

        if os.path.exists(self.path_toprocess):
            toprocess=open(self.path_toprocess)
            tasks=set([int(line.split(' ')[0]) for line in toprocess.readlines()])
            return tasks
        else: # All tasks still unprocessed
            return set(range(len(self.tasks)))

    def write_toprocess(self,tasks):
        """
        Write set of toprocess tasks

        Warning: Not thread safe!    

        Parameters:
         - tasks (set of int) List of toprocess task IDs
        """
        tasks=sorted(set(tasks)) #sort before saving, make unique
        toprocess=open(self.path_toprocess, 'w')
        for task in tasks:
            toprocess.write('{} {}\n'.format(task,self.tasks[task]))
        toprocess.close()

    def read_finished(self):
        """"
        Get list of finished tasks

        Warning: Not thread safe!

        Returns: list of finsihed task id's
        """

        if os.path.exists(self.path_finished):
            finished=open(self.path_finished)
            tasks=[int(line.split(' ')[0]) for line in finished.readlines()]
            return tasks
        else: # nothing done
            return []

