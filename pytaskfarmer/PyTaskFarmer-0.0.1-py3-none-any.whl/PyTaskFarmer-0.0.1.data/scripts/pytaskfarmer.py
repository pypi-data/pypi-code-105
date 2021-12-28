#!python
# Grab future to use print as a function
from __future__ import print_function

# Multiprocessing, to deal with a pool of work
from multiprocessing import Pool,current_process
# Argparse (duh), time for logging,errno for exceptions
import argparse,time,errno,sys
# copy for making static copies passed to workers
import copy
# os for OS stuff, os.path to find config
import os,os.path
# For timeline output
import json
# Needed for cleanup
import signal

from taskfarmer import task, runners

def handler(signum, frame):
    """
    Clean-up handler that terminates the worker pool when certain signals are received
    """
    print(time.asctime(),'User interrupt during excecution')
    # Terminate the worker pool
    global pool
    pool.terminate()
    pool.join()
    sys.exit(1)
        
def executor(my_input):
    """
    The executor itself. This is the main function that's doing work.

    Takes the list of tasks, pops the next one off the top.

    Returns: tuple with task ID, start time, end time
    """
    # Signal handlers
    # The big ones are handled on top
    signal.signal(signal.SIGUSR1, signal.SIG_IGN)
    signal.signal(signal.SIGINT , signal.SIG_IGN)
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    # cleanup handler on termination
    def term_handler(signum, frame):
        nonlocal taskid,tasks,runner

        print(time.asctime(),'Kill executor processing task',taskid)
        # Kill the process
        runner.terminate()
        # Update toprocess list
        tasks.record_toprocess_task(taskid)

        # Done
        sys.exit(1)
    signal.signal(signal.SIGTERM, term_handler)

    # Decode the input
    tasks    = my_input[0]
    logdir   = my_input[1]
    runner   = my_input[2]

    # Get the command we want to run
    taskid = tasks.pop_task()
    if taskid==None: # Run out of tasks
        return

    # Prepare the runner
    command = tasks[taskid]
    logfh=open(logdir+'/log_'+str(taskid),'w')

    # Start the process and wait for it to finish
    print(time.asctime(),'Executing task',taskid,':',command)    
    start_time=time.time()
    returncode=runner.run(taskid, command, logfh)
    end_time  =time.time()
    print(time.asctime(),'Completed task',taskid,':',command)

    logfh.close()

    # Register the task as complete - we do this last so that if there's a timeout
    #  the worst case is that work is finished but we didn't report back in time
    tasks.record_done_task(taskid, returncode)
    return (current_process().pid,taskid,start_time,end_time)

# This is the actual main -- the meat of the farmer itself.
if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description='Simple task queue')
    parser.add_argument('tasklist', metavar='List', type=str, help='Path to file defining the tasklist')
    parser.add_argument('--proc'    ,'-n', metavar='Processes', type=int, nargs='?', default=8, help='Number of workers')
    parser.add_argument('--timeout'      , type=int, default=None, help='End execution in timeout seconds')
    parser.add_argument('--workdir' ,'-w', required=False, default=None, help='Work directory to store progress and log files.')
    parser.add_argument('--verbose' ,'-v', type=bool, dest='verb', required=False, default=False)
    parser.add_argument('--runner'  ,'-r', default='default', help='Runner definition to use.')
    parser.add_argument('--tasklist','-t', default='default', dest='tasklisthandler', help='Runner definition to use.')
    args = parser.parse_args()

    # Tell the user what we got
    print(time.asctime(),'Working on task list',args.tasklist)

    # Prepare workdir
    workdir=args.workdir if args.workdir is not None else args.tasklist+"_workdir"

    print(time.asctime(),'Will store progress in',workdir)
    if not os.path.isdir(workdir):
        # Create it
        try:
            os.mkdir( workdir )
        except OSError as e:
            # If the error wasn't EEXIST we should raise it.
            if e.errno != errno.EEXIST: raise
        # Multiple nodes may be racing to make this directory
        # Don't test anything further in case that's problematic

    logdir=workdir+"/logs"
    print(time.asctime(),'Will store logs in',logdir)
    if not os.path.isdir(logdir):
        # Create it
        try:
            os.mkdir( logdir )
        except OSError as e:
            # If the error wasn't EEXIST we should raise it.
            if e.errno != errno.EEXIST: raise
        # Multiple nodes may be racing to make this directory
        # Don't test anything further in case that's problematic

    # Load the tasklist
    mytasklists=task.TaskListManager()
    tasklistdir=os.path.expanduser("~/.pytaskfarmer/tasklists.d")
    if os.path.exists(tasklistdir):
        mytasklists.load_directory(tasklistdir)
    mytasklists.load_directory('./')
    tasks=mytasklists.tasklist(args.tasklisthandler, args.tasklist, workdir)

    # Grab the work
    n_tasks = len(tasks)
    print(time.asctime(),'Found',n_tasks,'total tasks')

    # Load the runner
    myrunners=runners.RunnerManager()
    runnerdir=os.path.expanduser("~/.pytaskfarmer/runners.d")
    if os.path.exists(runnerdir):
        myrunners.load_directory(runnerdir)
    myrunner=myrunners.runner(args.runner)
        
    # Set up the pool
    pool = Pool(processes=args.proc)

    # Register cleanup signals
    signal.signal(signal.SIGUSR1, handler) # cori signal telling us job is about to complete
    signal.signal(signal.SIGINT , handler) # Keyboard interrupt
    if args.timeout!=None:
        signal.signal(signal.SIGALRM, handler) # alarm from timeout
        signal.alarm(args.timeout)

    # This is a bit wasteful if we run on many nodes. This sets up a single
    #  task for all the lines in the task file. If the file is being processed
    #  by many nodes, then it could be that we reach the end of the file much
    #  earlier. In such cases, this simply does a bunch of null-op work that should
    #  be fairly quick (just set up / tear down / locking overheads) and then
    #  returns, so we hope this won't waste too much time
    for taskResult in pool.imap_unordered(executor, zip(n_tasks*[copy.copy(tasks)],n_tasks*[logdir],n_tasks*[myrunner])):
        if taskResult==None:
            continue # Nothing was done

        threadid,taskid,start_time,end_time=taskResult

        #
        # Update timeline file
        tasks.lock()
        timeline_path=tasks.workdir+'/timeline.json'

        # Load existing timeline
        timeline=[]
        if os.path.exists(timeline_path):
            with open(timeline_path) as fh_timeline:
                timeline=json.load(fh_timeline)

        # Append task information
        jobtime={
            "cat": "task",
            "name": tasks.tasks[taskid],
            "pid": os.getpid(),
            "tid": threadid,
            "ts": start_time*1e6,
            "dur": (end_time-start_time)*1e6,
            "ph": "X",
            "args": {}
        }
        timeline.append(jobtime)

        # Store the timeline
        with open(timeline_path,'w') as fh_timeline:
            json.dump(timeline, fh_timeline)
        tasks.unlock()

    print(time.asctime(),'Finished working')

    # cleanup of workers    
    pool.close()
    pool.join()
