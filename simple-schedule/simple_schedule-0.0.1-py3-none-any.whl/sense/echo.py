from simple_schedule import task,ScheduleInfo

@task(id="echo",name="测试任务")
def echo(scInfo:ScheduleInfo ):
    return ""