from __init__ import Task,Schedule
def convert(task,*,schedule_time:int=0):
	if isinstance(task,Task):
		return Schedule(task.name,task.update,schedule_time,task.args,task.paused)
	elif isinstance(task,Schedule):
		return Task(task.name,task.func,task.args,task.paused)
	else:
		raise TypeError(f"Must be either sttask.Task or sttask.Schedule, not {type(task).__name__}")
