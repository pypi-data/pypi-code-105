# -*- coding: utf-8 -*-
import time
import datetime
import _thread as thr
import requests
import json
import sys
import os
from pathlib import Path

__all__ = [
    "sleep", "time_year", "time_day", "time_hour", "print_sys", "print_msg",
    "print_error", "input_time", "input_lib", "input_data", "start", "Robot",
    "remained", "revise_task_item", "print_sys"
]

current_path = os.path.dirname(os.path.abspath(__file__))
min_sec = 60
hou_sec = min_sec * 60
day_sec = hou_sec * 24
tasks = {
    "1": "定时提醒",
    "2": "",
    "3": "",
    "4": "",
    "5": "",
    "q": "退出系统",
    "i": "查询现有任务",
    "r": "修改任务",
    "d": "del task",
    "reloading": "reloading task"
}
repeat_lib = {"1": "定时", "2": "每日", "3": "工作日", "4": "延迟N分钟", "5": "Now"}
group_lib = {
    "0": {
        "1": "项目组",
        "2": "贪吃蛇测试组",
        "3": "袁少华"
    },
    "袁少华":
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cf6fe1e9-5bd9-42af-a518-4a7c3f609b79",
    "贪吃蛇测试组":
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2acaad96-591b-4176-9759-6cbba401855d",
    "项目组":
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=503a0e01-9dc6-4b98-8fc9-8980d76ac0a9"
}
models = {}
task_list = {}
task_replace = {}
debug = False
data_list = ["content", "mentioned_list", "mentioned_mobile_list"]


def time_day():
    return time.strftime('%m-%d-%H %M-%S', time.localtime())


def time_year():
    return time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())


def time_hour():
    return time.strftime('%H-%M-%S', time.localtime())


def sleep(times=None):
    if not times:
        times = 2

    for i in range(times):
        print("*" * i, end="")
        time.sleep(i)


def print_sys(tips=None):
    """
    :param tips:
    :return:
    """
    if tips:
        print(tips)
    print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])


def print_all():
    print("=" * 50, "\n欢迎使用定时任务系统,回车进入目录\n" + "=" * 50)
    input()


def print_msg(tips=None):
    if not tips:
        print("**" * 15 + "task" + "**" * 15)
    else:
        print("##" * 30 + "\n" + tips + "\n" + "##" * 30)


def print_error(tips=""):
    tips += "输入有误，请重新输入:"
    print("**" * 15 + tips + "**" * 15)


def lib_to_do_lib(dict_lib):
    libs = {}
    do_lib = {}
    if isinstance(dict_lib, (list, tuple)):
        print(dict_lib)
        for i in range(len(dict_lib)):
            libs[str(i + 1)] = dict_lib[i]
        do_lib = libs.copy()
    elif isinstance(dict_lib, dict):
        if '0' in dict_lib.keys():
            libs = dict_lib['0']
        else:
            keys_lib = list(dict_lib.keys())
            for i in range(len(keys_lib)):
                libs[str(i + 1)] = keys_lib.pop()
        do_lib = dict_lib.copy()
        for key in libs.keys():
            if libs[key] not in do_lib.keys():
                raise 'dict_lib error:%s' % str(dict_lib)
    return libs, do_lib


def len_str(ob):
    if type(ob) == str:
        return len(ob)
    else:
        return len(str(ob))


def input_lib(tips, dict_lib):
    print_msg()
    times = 1
    libs, do_lib = lib_to_do_lib(dict_lib)

    while 1:
        print(tips)
        str_len = 100 // max([len_str(ob) for ob in libs.values()]) or 1
        line_num = str_len if str_len < 5 else 5
        index_en = 1
        for key in libs.keys():
            en = ";  " if index_en % line_num != 0 else ";\n"
            index_en += 1
            if libs[key]:
                print(key, libs[key], end=en)
        a_input = input("\ntips:如果没有需要的选项，输入“add”;退出输入“q“\n请选择：")
        if a_input in libs.keys():
            return libs[a_input]
        elif a_input == "q":
            return False
        elif a_input == "add":
            if isinstance(dict_lib, list):
                print(dict_lib)
                dict_lib.append(input("输入你需要的选项："))
                libs, do_lib = lib_to_do_lib(dict_lib)
            elif isinstance(dict_lib, dict):
                key_name = input("输入你需要的选项：")
                if '0' in dict_lib.keys():
                    if key_name not in dict_lib.values():
                        dict_lib["0"][str(len(libs) + 1)] = key_name
                dict_lib[key_name] = input("输入对应参数：")
                key_name = input("输入你需要的选项：")
                if key_name not in libs.values():
                    libs["0"][str(len(libs) + 1)] = key_name
                libs[key_name] = input("输入对应参数：")
            else:
                print_error("该选择不能添加选项")
        else:
            times += 1
            print_error()
        if times >= 5:
            print("输入错误次数过多，退出")
            return False


def post_remained(name, group, data):
    headers = {'Content-Type': 'application/json'}
    session = requests.Session()
    res = session.post(url=group_lib[group],
                       data=json.dumps(data,
                                       ensure_ascii=False).encode("utf-8"),
                       headers=headers)
    print("任务%s的发送结果:%s" % (name, res.content.decode("utf-8")))
    data["content"] = "任务%s的发送结果:%s" % (name, res.content.decode("utf-8"))
    tell_me(data)


def tell_me(data):
    headers = {'Content-Type': 'application/json'}
    session = requests.Session()
    session.post(url=group_lib["3"],
                 data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
                 headers=headers)


#企业微信提醒任务
def remained(task):
    for i in range(6):
        if i == 5:
            print_error("已经输入5次，退回主系统")
        try:
            print_msg("微信定时提醒")
            name = input("请输入提醒的主题：")
            repeat = input_lib("请输入人物信息，是否每天重复：", repeat_lib)
            if not repeat: break
            time_remained = input_time("请输入提示时间：", repeat)
            if not time_remained: break
            group = input_lib("请选择发送的群：", group_lib["0"], group_lib)
            if not group: break
            data = input_data()
            print_msg("任务(%s)内容确认：\n%s发送给%s%s,发送时间为%s" %
                      (name, repeat, group, str(data), time_remained))
            in_data = input(
                "waiting for start task,Please press enter.replace,press (N)! "
            )
            if in_data: continue
            task.add(name, group, data, repeat, time_remained, write=True)
            time.sleep(2)
        except ValueError:
            print_error()
        else:
            return [name, group, data, repeat, time_remained]


#输入提醒时间
def input_time(tips, rep="定时"):
    print(rep)
    print(tips)
    it_in = datetime.datetime.strptime(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        '%Y-%m-%d %H:%M:%S')
    if rep == "Now": return it_in
    if rep == "延迟N分钟":
        for ij in range(5):
            try:
                mi = int(input("请输入延迟的时长，单位分钟："))
            except ValueError:
                print("Unexpected error:",
                      sys.exc_info()[0],
                      sys.exc_info()[1])
                mi = 88888
            else:
                if mi < day_sec / 60:
                    return datetime.timedelta(seconds=mi * min_sec) + it_in
    for ii in range(5):
        for ij in range(5):
            try:
                ho, mi = map(
                    int,
                    input(tips + "请输入提示时间：（格式：H：M）\n（当前时间为%s）" %
                          time.strftime("%y-%m-%d %H:%M:%S", time.localtime())
                          ).split(":"))
            except ValueError:
                print("Unexpected error:",
                      sys.exc_info()[0],
                      sys.exc_info()[1])
                ho, mi = 88888, 8888
            else:
                break
        if ho >= 24 or mi > 59:
            print_error()
            continue
        else:
            if ho * hou_sec + mi * min_sec - (
                    3600 * int(time.strftime("%H", time.localtime())) +
                    int(time.strftime("%M", time.localtime())) * 60 +
                    int(time.strftime("%S", time.localtime()))) <= 0:
                print("今天时间已过，明天开始第一次提醒!")
                it_in = datetime.timedelta(
                    seconds=ho * hou_sec + mi * min_sec +
                    day_sec) + datetime.datetime.strptime(
                        time.strftime("%Y-%m-%d", time.localtime()),
                        '%Y-%m-%d')
            else:
                it_in = datetime.timedelta(
                    seconds=ho * hou_sec +
                    mi * min_sec) + datetime.datetime.strptime(
                        time.strftime("%Y-%m-%d", time.localtime()),
                        '%Y-%m-%d')
            while True:
                act_time = input("提醒时间为：%s\n确认请输入Y，修改日期请输入N,重新输入时间输入q：" %
                                 it_in)
                if act_time in ("Y", "y", ""):
                    return it_in
                elif act_time in ("n", "N"):
                    while True:
                        try:
                            m_day = input(tips + "日期（格式：m-d）：")
                            it_in = datetime.timedelta(
                                seconds=ho * hou_sec +
                                mi * min_sec) + datetime.datetime.strptime(
                                    (time.strftime("%Y-", time.localtime()) +
                                     m_day), '%Y-%m-%d')
                        except ValueError:
                            print("Unexpected error:",
                                  sys.exc_info()[0],
                                  sys.exc_info()[1])
                        else:
                            break
                    return it_in
                elif act_time in ["q", "Q"]:
                    it_in = 0
                    break
        if ii == 4:
            print("输入错误次数过多")
    return it_in


# 输入提醒内容
def input_data():
    data = {}
    while True:
        try:
            in_put = input("请输入提示内容:")
            if in_put:
                data["msgtype"] = "text"
                data["text"] = {}
                data["text"]["content"] = in_put
                in_put = input("请选择@的人员：（没有直接回车）")
                if in_put:
                    data["text"]["mentioned_list"] = in_put
                break
        except ValueError:
            print_sys()
        if len(data) > 1:
            break
    return data


def data_str(str1):
    data = {}
    if isinstance(str1, str):
        str_lib = str1.replace("\'", "\"").split("\"")
        if "text" in str_lib:
            data["msgtype"] = "text"
            data["text"] = {}
            if "content" in str_lib:
                data["text"]["content"] = str_lib[str_lib.index("content") + 2]
            if "mentioned_list" in str_lib:
                data["text"]["mentioned_list"] = str_lib[
                    str_lib.index("mentioned_list") + 2]
            return data
        else:
            data["msgtype"] = "text"
            data["text"] = {}
            data["text"]["content"] = str1
            return data
    else:
        print("data输入不是字符串：", type(str1), str1)
        return False


def revise_task_item(item):
    if isinstance(item, str):
        if item in repeat_lib.values():
            repeat = input_lib("请输入人物信息，是否每天重复：", repeat_lib)
            return repeat
        elif item in group_lib.keys():
            group = input_lib("请选择发送的群：", group_lib["0"], group_lib)
            return group
        else:
            name = input("请输入提醒的主题：")
            return name
    elif isinstance(item, dict):
        data = input_data()
        return data
    elif isinstance(item, datetime.datetime):
        time_remained = input_time("请输入提示时间：")
        return time_remained
    else:
        print_error()
        return False


class Reminder:
    """定时提醒"""
    def __init__(self, name):
        self.name = name
        self.task_list = {}

    def add(self,
            name,
            group=group_lib["袁少华"],
            data=None,
            repeat=repeat_lib["1"],
            first_time=None,
            write=None):
        print("添加任务")
        #print(name, group, data, repeat, first_time)
        if first_time is None:
            if repeat == "Now":
                remained_time = datetime.datetime.now()
                Robot(remained_time, name, group, data, repeat,
                      first_time).robot_post()
            else:
                #print(name,group,data,repeat,first_time)
                print_error("缺少提示时间")
        else:
            if first_time in self.task_list.keys():
                if [name, group, data, repeat, first_time,
                        True] == self.task_list[first_time]:
                    print_error("任务重复")
                    return False
                else:
                    while first_time in self.task_list.keys():
                        first_time += datetime.timedelta(minutes=1)
            self.task_list[first_time] = [
                name, group, data, repeat, first_time, True
            ]
            if (time.mktime(first_time.timetuple()) - int(time.time()) >=
                    0) and (time.mktime(first_time.timetuple()) -
                            int(time.time()) < 5 * min_sec):
                self.do_task(first_time)
            if time.mktime(first_time.timetuple()) - int(time.time()) < 0:
                self.replace_task(first_time)
        if write: self.write()

    def write(self):
        print("更新任务备份")
        path = current_path
        files = open(path + "/task_list.txt", "w")
        print(self.task_list)
        files.writelines(json.dumps(self.task_list))
        # for key in sorted(self.task_list.keys()):
        #     print(key,self.task_list[key])
        #     for i in range(len(self.task_list[key])):
        #         files.writelines(str(self.task_list[key][i]))
        #         if i == len(self.task_list[key])-1:
        #             files.writelines("\n")
        #         else:
        #             files.writelines("+")

    def read(self):
        print("read task")
        try:
            path = current_path
            my_file = Path(path + "/task_list.txt")
            print_msg("从文件%s中提取任务" % path + "task_list.txt")
            if my_file.exists():
                file = open(path + "/task_list.txt", "r")
                print_msg("从文件%s中提取任务" % path + "/task_list.txt")
                t_list = json.loads(file.readlines()[0])
                if len(t_list) == 0:
                    print_msg("没有任务存档！")
                else:
                    for ta in t_list["0"].value():
                        if ta in self.task_list[0].value():
                            continue
                        else:
                            self.add(t_list[ta])

                # for task in file.readlines():
                #     name, group, data, repeat, remained_time,flag= task.split("+")
                #     #print(name, group, data, repeat, remained_time,flag)
                #     if "True" in flag:
                #         remained_time = remained_time.replace(" datetime.datetime","")
                #         remained_time = datetime.datetime.strptime(remained_time,"%Y-%m-%d %H:%M:%S")
                #         self.add(name.replace("'",""),group.replace("'",""),data_str(data),repeat.replace("'",""),remained_time)
            else:
                print_msg("没有任务存档！")
        except TypeError:
            print_sys()
        self.print()
        self.write()

    def print(self):
        str1 = "当前任务列表如下：\n"
        tails = "****details*****" * 3 + "\n"
        key_lib = self.keys()
        task_l = {"0": {}}
        if len(key_lib) == 0:
            print_msg("当前没有任务")
            return
        for i in range(len(key_lib)):
            str1 += "%d、%s\n" % (i + 1, self.task_list[key_lib[i]][0])
            task_l["0"][str(i + 1)] = key_lib[i]
            #task_l[str(i+1)]=self.task_list[key_lib[i]][4]
            tails += "%d、%s\n%s发送给%s,信息内容：\n%s\n第一次发送发送时间%s\n" % (
                i + 1, self.task_list[key_lib[i]][0],
                self.task_list[key_lib[i]][3], self.task_list[key_lib[i]][1],
                self.task_list[key_lib[i]][2], self.task_list[key_lib[i]][4])
        print_msg(str1 + tails)
        return task_l

    def replace_task(self, key):
        print_msg("检测或更新任务%s" % self.task_list[key][0])
        if time.mktime(key.timetuple()) - int(time.time()) > 0:
            print_error("提示时间未到")
            return False
        elif self.task_list[key][3] == "每日":
            self.task_list[key][4] += datetime.timedelta(days=1)
            self.add(self.task_list[key][0], self.task_list[key][1],
                     self.task_list[key][2], self.task_list[key][3],
                     self.task_list[key][4])
        elif self.task_list[key][3] == "工作日":
            if int(time.strftime("%w", time.localtime())) < 5:
                self.task_list[key][4] += datetime.timedelta(days=1)
                self.add(self.task_list[key][0], self.task_list[key][1],
                         self.task_list[key][2], self.task_list[key][3],
                         self.task_list[key][4])
            else:
                self.task_list[key][4] += datetime.timedelta(
                    days=8 - int(time.strftime("%w", time.localtime())))
                self.add(self.task_list[key][0], self.task_list[key][1],
                         self.task_list[key][2], self.task_list[key][3],
                         self.task_list[key][4])
        elif self.task_list[key][3] in (repeat_lib["5"], repeat_lib["4"]):
            time_abs = time.mktime(key.timetuple()) - int(time.time())
            if time_abs < 10 * min_sec:
                if time_abs < -min_sec * 2:
                    self.task_list[key][2]["text"][
                        "content"] += "\n(补发" + ",正确时间为：%s)" % self.task_list[
                            key][4]
                    self.task_list[key][4] = None
                elif time_abs < 0:
                    self.task_list[key][4] = None
                self.do_task(key, False)
        else:
            print_msg("重复类型错误，任务为%s" % str(self.task_list[key]))
        del self.task_list[key]

    def delay_replace(self, key, time_delay):
        time.sleep(time_delay)
        if self.task_list[key][3] in (repeat_lib["2"], repeat_lib["3"]):
            self.replace_task(key)
        else:
            del self.task_list[key]

    def do_task(self, key, replace=True):
        thr.start_new_thread(
            Robot(key, self.task_list[key][0], self.task_list[key][1],
                  self.task_list[key][2], repeat_lib["1"],
                  self.task_list[key][4]).robot_post, ())
        if replace:
            thr.start_new_thread(
                self.delay_replace,
                (key, time.mktime(key.timetuple()) - int(time.time())))

    def keys(self):
        return sorted(self.task_list.keys())

    def delete(self):
        print_msg("开始删除任务程序,请选择任务")
        if len(self.task_list) >= 1:
            task_replace.clear()
            task_r = self.print()
            for i in range(5):
                try:
                    in_data = input_lib("选择要删除的任务key：", task_r["0"])
                    if in_data in self.task_list.keys():
                        str_d = "删除任务为\n%s\n%s发送给%s,信息内容：\n%s\n第一次发送发送时间%s\n确认请按回车：重现选择输入N" % (
                            self.task_list[in_data][0],
                            self.task_list[in_data][3],
                            self.task_list[in_data][1],
                            self.task_list[in_data][2],
                            self.task_list[in_data][4])
                        print_msg(str_d)
                        if input():
                            if i == 4:
                                print_error("输入次数过多")
                            continue
                        else:
                            del self.task_list[in_data]
                            print_msg("删除成功")
                            self.write()
                            sleep()
                            return True
                    elif in_data == "q":
                        print_msg("已取消删除操作")
                        return False
                    else:
                        print_error()
                except ValueError:
                    print_sys()
                    print_error()
        else:
            print_msg("当前没有待执行任务可删除")
        sleep()

    def replace_item(self, key):
        items = {}
        for i in range(len(self.task_list[key])):
            items[str(i + 1)] = self.task_list[key][i]
        item = input_lib("请选择修改的任务项：", items)
        if item:
            for item_key in items.keys():
                if items[item_key] == item:
                    in_data = revise_task_item(item)
                    if in_data:
                        self.task_list[key][int(item_key) - 1] = in_data
                        return True
                    else:
                        print_error()
                        return False
        else:
            return False

    def revise(self):
        print_msg("修改任务%s" % self.name)
        if len(self.task_list) >= 1:
            task_replace.clear()
            task_r = self.print()
            for i in range(5):
                try:
                    in_data = input_lib("选择要修改的任务key：", task_r["0"])
                    if not in_data:
                        print_msg("已取消删除操作")
                        return False
                    elif in_data in self.task_list.keys():
                        str_d = "修改的任务为\n%s\n%s发送给%s,信息内容：\n%s\n第一次发送发送时间%s\n确认请按回车：重现选择输入N" % (
                            self.task_list[in_data][0],
                            self.task_list[in_data][3],
                            self.task_list[in_data][1],
                            self.task_list[in_data][2],
                            self.task_list[in_data][4])
                        print_msg(str_d)
                        print("执行修改任务")
                        if not self.replace_item(in_data):
                            if i == 4:
                                print_error("输入次数过多")
                                return False
                            continue
                        else:
                            print_msg("修改成功")
                            self.write()
                            sleep()
                            return True
                    else:
                        print_error()
                except ValueError:
                    print_sys()
                    print_error()
        else:
            print_msg("当前没有待执行任务")
            sleep()

    def liston(self):
        print("开启任务进度监控进程")
        pre = time.mktime((2009, 2, 17, 17, 3, 38, 1, 48, 0))
        while True:
            print("*", end="")
            try:
                if int(time.time()) - pre > hou_sec / 2:
                    print_msg("检测更新任务")
                    self.read()
                pre = int(time.time())
                for key in sorted(self.task_list.keys()):
                    time_abs = time.mktime(key.timetuple()) - int(time.time())
                    if time_abs < 0:
                        # if abs(time_abs) < 5 * min_sec:
                        #     self.do_task(key)
                        # else:
                        self.replace_task(key)
                        print_error("task time has passed, task reset!")
                    elif time_abs <= 5 * min_sec:
                        self.do_task(key)
                    else:
                        break
                if debug:
                    self.read()
                    self.write()
                    print_msg("Exit task system!")
                    break
                time.sleep(min_sec * 5)
            except ValueError:
                print_sys()


class Robot:
    """微信提醒机器人"""
    '''
    微信提醒机器人
    'User-Agent':'PostmanRuntime/7.22.0',
    'Accept':'*/*',
    'Cache-Control':'no-cache',
    'Postman-Token':'167f7808-6f13-490c-a5c3-07504a3f85c8',
    'Host':'qyapi.weixin.qq.com',
    'Accept-Encoding':'gzip, deflate, br',
    'Content-Length':'103',
    'Connection':'keep-alive'
    '''
    def __init__(self,
                 key,
                 name,
                 group=None,
                 data=None,
                 repeat="",
                 first_time=None):
        self.key = key
        self.name = name
        self.data = data
        self.group = group
        self.repeat = repeat
        if first_time is None:
            self.remained_time = datetime.datetime.now()
            self.delay_sec = 1

        else:

            self.delay_sec = time.mktime(first_time.timetuple()) - int(
                time.time())

            if self.delay_sec < 0:
                self.remained_time = first_time + datetime.timedelta(days=1)
                self.delay_sec += day_sec

                print("任务(%s)时间已过，更新时间为：\n%s" %
                      (self.name, self.remained_time))
            else:
                self.remained_time = first_time
        self.all = {
            0: {
                "1": "任务名字",
                "2": "提示信息",
                "3": "提醒对象",
                "4": "是否重复",
                "5": "提醒时间"
            },
            "任务名字": self.name,
            "提示信息": self.data,
            "提醒对象": self.group,
            "是否重复": self.repeat,
            "提醒时间": self.remained_time
        }

    def del_task(self, ):
        if self.key in task_list.keys():
            self.remained_time = datetime.time()
            del task_list[self.key]
            self.print_task()
            print_msg("task over！")

    def print_task(self, tips=""):
        print_msg("任务名字：(%s)\n%s发送给%s,信息内容：\n%s\n第一次发送%s秒后开始，发送时间%s\n%s" %
                  (self.name, self.repeat, self.group, self.data,
                   self.delay_sec, self.remained_time, tips))

    def replace(self):
        while True:
            try:
                in_data = input_lib("请选择要修改的内容：", self.all[0])
                if in_data == "提醒时间":
                    time_remained = input_time("请输入提示时间：",
                                               rep=str(self.repeat))
                    if time_remained == "q": break
                    else:
                        self.remained_time = time_remained
                        self.delay_sec = time.mktime(
                            self.remained_time.timetuple()) - int(time.time())
                        thr.start_new_thread(self.robot_post, ())
                        print_msg("提示:提醒时间修改完成！")
                if in_data == "任务名字":
                    self.name = input("请输入提醒的主题：")
                    print("%s修改完毕" % in_data)
                if in_data == "提醒对象":
                    self.group = input_lib("请选择发送的群：", group_lib["0"])
                    print("%s修改完毕" % in_data)
                if in_data == "是否重复":
                    self.repeat = input_lib("请输入人物信息，是否每天重复：", repeat_lib)
                    print("%s修改完毕" % in_data)
                if in_data == "提示信息":
                    self.data = input_data()
                    print("%s修改完毕" % in_data)
                else:
                    print_error()
            except ValueError:
                print("Unexpected error:",
                      sys.exc_info()[0],
                      sys.exc_info()[1])
            else:
                break
        print_msg("修改完毕，结果如下：")
        self.print_task()

    def robot_post(self):
        self.print_task("任务开始")
        time.sleep(self.delay_sec)
        headers = {'Content-Type': 'application/json'}
        while True:
            if abs(
                    time.mktime(self.remained_time.timetuple()) -
                    int(time.time())) > 120:
                print_msg("Task has been modified")
                break
            session = requests.Session()
            res = session.post(
                url=group_lib[self.group],
                data=json.dumps(self.data, ensure_ascii=False).encode("utf-8"),
                headers=headers)
            print("任务%s的发送结果:%s" % (self.name, res.content.decode("utf-8")))
            if self.repeat == "每日":
                self.remained_time += datetime.timedelta(days=1)
                self.delay_sec = day_sec

                time.sleep(self.delay_sec)
            elif self.repeat == "工作日":
                if int(time.strftime("%w", time.localtime())) <= 5:
                    self.remained_time += datetime.timedelta(days=1)
                    self.delay_sec = day_sec

                    time.sleep(self.delay_sec)
                else:
                    self.remained_time += datetime.timedelta(days=3)
                    self.delay_sec = day_sec * 3

                    time.sleep(self.delay_sec)
            else:
                self.del_task()
                print("重复状态:%s,task over" % self.repeat)
                break


def start():
    ta = Reminder("task")
    thr.start_new_thread(ta.liston, ())
    sleep()
    while 1:
        print_all()
        qu = input_lib("请选择任务：", tasks)
        if qu == "退出系统":
            global debug
            debug = True
            ta.liston()
            break
        elif qu == "定时提醒":
            remained(ta)
        elif qu == "查询现有任务":
            ta.print()
            sleep()
        elif qu == "修改任务":
            ta.revise()
        elif qu == "del task":
            ta.delete()
            sleep()
        elif qu == "reloading task":
            try:
                ta.read()
                sleep(3)
            except ValueError:
                print_sys()
        else:
            print_error("选择任务不存在")
            sleep()


class Task:
    task_Count = 0

    def __init__(self, name):
        self.name = name
        Task.task_Count += 1

    # 选择任务
    def start(self):
        print(self.name)
        while 1:
            print_all()
            qu = input_lib("请选择任务：", tasks)
            if qu == "退出":
                break
            elif qu == "定时提醒":
                print_msg("remained()")
            elif qu == "查询现有任务":
                var = vars().copy()
                for key in var.values():
                    if isinstance(var[key], ()):
                        print(key, var[key])
            else:
                print("选择任务不存在")


def test():
    # createVar = globals()
    global debug
    debug = True
    print(debug)
    aa = Reminder("test")
    print_msg()
    for i in range(1):
        print(i)
        #aa.add(i,"test",data = input_data(),first_time = input_time("test"))

    #aa.write()
    #aa.read()
    aa.liston()


if __name__ == "__main__":
    print_msg()
    #test()
    start()
