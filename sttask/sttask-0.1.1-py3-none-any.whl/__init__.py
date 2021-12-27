end=1
pause=2

class Schedule:
	"""
	Class for holding a scheduled task
	Schedule.name:   str
	Schedule.time:   int
	Schedule.func:   function
	Schedule.args:   tuple
	Schedule.paused: int*

	* while Schedule.paused is technicly an int, it is mainly used as a bool
	"""
	def __init__(self,name:str,func,time:int,args:tuple=(),paused:int=0):
		if not isinstance(name,str):
			raise TypeError(f"name should be str, not {type(name).__name__}")
		if not callable(func):
			raise TypeError("func should be callable")
		if not isinstance(args,tuple):
			raise TypeError(f"args should be tuple, not {type(args).__name__}")
		if not isinstance(time,int):
			raise TypeError(f"args should be tuple, not {type(time).__name__}")
		if paused!=0 and paused!=1:
			raise ValueError(f"paused should be 1 or 0, not {paused}")

		self.name=name
		self.time=time
		self.func=func
		self.args=args
		self.paused=paused

class TaskOwner:
	tasks=[]
	scheduled=[]

	def add(self,name:str,func,args:tuple=())->int:
		"""
		Appends a sttask.Task object to TaskOwner.tasks
		Returns the index of the task in TaskOwner.tasks
		"""
		if not isinstance(name,str):
			raise TypeError(f"name should be str, not {type(name).__name__}")
		if not callable(func):
			raise TypeError("func should be callable")
		if not isinstance(args,tuple):
			raise TypeError(f"args should be tuple, not {type(args).__name__}")
		self.tasks.append(Task(name,func,args))
		return self.grab_task(name)
	
	def task_list(self)->list:
		"""
		Returns a list of all task names
		"""
		lst=[]
		for i in self.tasks:
			lst.append(i.name)
		return lst

	def schedule_list(self)->list:
		"""
		Returns a list of all schedule names
		"""
		lst=[]
		for i in self.scheduled:
			lst.append(i.name)
		return lst

	def update(self)->None:
		"""
		Updates all the tasks, and removes time untill scheduled tasks activate.
		"""
		j=0
		for i in range(len(self.scheduled)):
			x=self.scheduled[i-j]
			if x.time==0:
				self.add(x.name,x.func,x.args)
				self.scheduled.pop(i)
				j+=1
			elif not x.paused:
				x.time-=1
				
		for i in range(len(self.tasks)):
			if self.tasks[i].paused==1:
				continue
			if(a:=self.tasks[i].update(self.tasks[i],self.tasks[i].args))==end:
				self.tasks.pop(i)
			elif a==pause:
				self.tasks[i].paused=1

	def grab_task(self,name:str)->int:
		"""
		Returns the index of a task in 'TaskOwner.tasks'
		If not found, returns -1
		"""
		if not isinstance(name,str):
			raise ValueError(f"name must be str, not {type(name).__name__}")

		for i in range(len(self.tasks)):
			if self.tasks[i].name==name:
				return i
		return -1

	def grab_schedule(self,name:str)->int:
		"""
		Returns the index of a schedule in 'TaskOwner.scheduled'
		If not found, returns -1
		"""
		if not isinstance(name,str):
			raise ValueError(f"name must be str, not {type(name).__name__}")

		for i in range(len(self.scheduled)):
			if self.scheduled[i].name==name:
				return i
		return -1

	def schedule(self,name:str,func,time:int=0,args:tuple=())->int:
		"""
		Appends a sttask.Schedule object to TaskOwner.scheduled
		Returns the index of the task in TaskOwner.scheduled
		"""
		if not isinstance(name,str):
			raise ValueError(f"name must be str, not {type(name).__name__}")
		if not callable(func):
			raise ValueError(f"func must be function, not {type(func).__name__}")
		if not isinstance(time,int):
			raise ValueError(f"time must be int, not {type(time).__name__}")
		if not isinstance(args,tuple):
			raise ValueError(f"args must be tuple, not {type(time).__name__}")

		self.scheduled.append(Schedule(name,func,time,args))

	def play(self,task:str)->None:
		"""
		Unpauses a task
		"""
		if not isinstance(task,str):
			raise ValueError(f"task must be str, not {type(task).__name__}")

		self.tasks[self.grab_task(task)].paused=0

	def pause(self,task:str)->None:
		"""
		Pauses a task
		"""
		if not isinstance(task,str):
			raise ValueError(f"task must be str, not {type(task).__name__}")

		self.tasks[self.grab_task(task)].paused=1

	def name_set(self,task:str,name:str)->None:
		"""
		Renames a task
		"""
		if not isinstance(task,str):
			raise ValueError(f"task must be str, not {type(task).__name__}")
		if not isinstance(name,str):
			raise ValueError(f"name must be str, not {type(name).__name__}")

		self.tasks[self.grab_task(task)].name=name

	def update_set(self,task:str,func)->None:
		"""
		Changes the update function for a task
		"""
		if not isinstance(task,str):
			raise ValueError(f"task must be str, not {type(task).__name__}")
		if not callable(func):
			raise ValueError(f"func must be function, not {type(func).__name__}")

		self.tasks[self.grab_task(task)].update=func

	def args_set(self,task:str,args:tuple)->None:
		"""
		Changes the arguments for a task
		"""
		if not isinstance(task,str):
			raise ValueError(f"task must be str, not {type(task).__name__}")
		if not isinstance(args,tuple):
			raise ValueError(f"args must be tuple, not {type(time).__name__}")

		self.tasks[self.grab_task(task)].args=args

	def grab_output(self,task:str):
		"""
		Returns the output value for a task
		"""
		if not isinstance(task,str):
			raise ValueError(f"task must be str, not {type(task).__name__}")

		return self.tasks[self.grab_task(task)].output

	def pop_task(self,task:str)->None:
		"""
		Removes a task by name
		"""
		if not isinstance(task,str):
			raise ValueError(f"task must be str, not {type(task).__name__}")

		del self.tasks[self.grab_task(task)]

	def play_schedule(self,schedule:str)->None:
		"""
		Unpauses a schedule
		"""
		if not isinstance(schedule,str):
			raise ValueError(f"task must be str, not {type(schedule).__name__}")

		self.scheduled[self.grab_schedule(schedule)].paused=0

	def pause_schedule(self,schedule:str)->None:
		"""
		Pauses a schedule
		"""
		if not isinstance(schedule,str):
			raise ValueError(f"task must be str, not {type(schedule).__name__}")

		self.scheduled[self.grab_schedule(schedule)].paused=1

	def name_set_schedule(self,schedule:str,name:str)->None:
		"""
		Renames a schedule
		"""
		if not isinstance(schedule,str):
			raise ValueError(f"task must be str, not {type(schedule).__name__}")
		if not isinstance(name,str):
			raise TypeError(f"name should be str, not {type(name).__name__}")

		self.scheduled[self.grab_schedule(schedule)].name=name

	def update_set_schedule(self,schedule:str,func)->None:
		"""
		Changes the update function for a schedule
		"""
		if not isinstance(schedule,str):
			raise ValueError(f"task must be str, not {type(schedule).__name__}")
		if not callable(func):
			raise TypeError("func should be callable")

		self.scheduled[self.grab_schedule(schedule)].update=func

	def args_set_schedule(self,schedule:str,args:tuple)->None:
		"""
		Sets the arguments for a schedule
		"""
		if not isinstance(schedule,str):
			raise ValueError(f"task must be str, not {type(schedule).__name__}")
		if not isinstance(args,tuple):
			raise TypeError(f"args should be tuple, not {type(args).__name__}")

		self.scheduled[self.grab_schedule(schedule)].args=args

	def pop_schedule(self,schedule:str)->None:
		"""
		Removes a schedule
		"""
		if not isinstance(schedule,str):
			raise ValueError(f"task must be str, not {type(schedule).__name__}")

		del self.scheduled[self.grab_schedule(schedule)]
	
class Task:
	"""
	Class for storing a task.

	Task.name:   str
	Task.update: function
	Task.paused: int*
	Task.args:   tuple
	Task.output: any

	* while Task.paused is technicly an int, it is mainly used as a bool
	"""
	def __init__(self,name:str,func,args:tuple,paused:int=0)->None:
		if not isinstance(name,str):
			raise TypeError(f"name should be str, not {type(name).__name__}")
		if not callable(func):
			raise TypeError("func should be callable")
		if not isinstance(args,tuple):
			raise TypeError(f"args should be tuple, not {type(args).__name__}")
		if paused!=0 and paused!=1:
			raise ValueError(f"paused should be 1 or 0, not {paused}")

		self.name=name
		self.update=func
		self.paused=paused
		self.args=args
		self.output=0
