import re
import puppy
import shutil
import os
import unittest
import ctypes, sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def exec_by_admin(file):
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file, None, 1)
    else:
        raise BaseException("python版本不受支持!")


def move_unittest_main():
    import unittest
    # 取到puppy的static目录
    puppy_path = puppy.__path__[0]
    static_path = os.path.join(puppy_path, "static")
    # 取到unittest的目录
    unittest_path = unittest.__path__[0]
    # 替换默认的main.py
    # 先备份
    tmp_file = os.path.join(unittest_path, "tmp.txt")
    try:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        with open(tmp_file, mode="w") as f:
            pass
    except:
        # 无权限，调用管理员模式
        exec_by_admin(os.path.join(static_path, "move_main.py"))
    else:
        # 有权限
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        src_main_file = os.path.join(static_path, "main.py")
        main_file = os.path.join(unittest_path, "main.py")
        new_main_file = os.path.join(unittest_path, "main.py.backup")
        if os.path.exists(new_main_file):
            os.remove(new_main_file)
        if os.path.exists(main_file):
            shutil.copy(main_file, new_main_file)
            os.remove(main_file)
        shutil.copy(src_main_file, main_file)
        print("已完成main.py文件替换")


# 取到命令
params = sys.argv[1:]
command = " ".join(params)
# 取到当前项目目录
cwd = os.path.join(os.getcwd())
# 取到puppy的static目录
puppy_path = puppy.__path__[0]
static_path = os.path.join(puppy_path, "static")
# 取到unittest的目录
unittest_path = unittest.__path__[0]

if command == "init":
    # 判断是否存在file文件夹或runner.py
    print("注意：您正在执行puppya的初始化命令，此命令会执行以下操作：")
    print("1、创建interface文件夹，并生成一个示例接口XML")
    print("2、创建flow文件夹，并生成一个示例流程XML")
    print("3、创建file/conf文件夹，并生成一个默认配置")
    print("4、创建file/xsd文件夹，并生成接口、流程、案例XML的语法约束文件")
    print("5、创建test_data文件夹，并生成一个示例案例XML")
    print("6、创建test_case模块，并生成一个示例案例XML对应的执行py文件")
    print("7、创建git版本控制忽略文件")
    print("8、创建puppy框架的自述文件")
    print("9、创建runner.py用于案例执行")
    print("10、替换Python单元测试框架UnitTest的main.py用于支持单个案例执行")
    _i = input("确认执行以上操作，请输入y:")
    if _i not in ['y', 'Y']:
        print("终止操作！")
        exit(0)
    file_path = os.path.join(cwd, "file")
    runner_path = os.path.join(cwd, "runner.py")
    if os.path.exists(file_path) or os.path.exists(runner_path):
        print("")
        _i = input("注意：当前目录不是干净的！\n继续操作将会直接覆盖原有文件!\n建议使用puppy update进行配置升级!\n如需继续请输入y:")
        if _i not in ['y', 'Y']:
            print("终止操作！")
            exit(0)
    # 将static目录里的文件拷贝到当前项目
    files = list()
    for _root, _dirs, _files in os.walk(static_path):
        for _f in _files:
            files.append(os.path.join(_root, _f).replace(static_path + "\\", ""))
    for _f in files:
        dst = os.path.join(cwd, _f)
        # 包含main.py文件将不会被拷贝
        if "main.py" in _f:
            continue
        if os.path.exists(dst):
            os.remove(dst)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        src = os.path.join(static_path, _f)
        shutil.copy(src, dst)
    # 移动main.py文件
    move_unittest_main()
    print("已完成操作！")
    print("最后：请手动安装生成在根目录的Pycharm插件，其名称为【PuppyPlugin-x.x.x-SNAPSHOT.zip】，用于支持便捷的案例编写！")
elif command == "update":
    # 从runner.py取得版本
    number_re = re.compile("\d+\.\d+\.\d+")
    runner_path = os.path.join(cwd, "runner.py")
    now_version = "0.0.0"
    if not os.path.exists(runner_path):
        print("未找到自动化测试关键性文件，请使用puppya init命令进行初始化！")
        exit(-1)
    with open(runner_path, "r", encoding="utf-8") as file:
        for line in file.readlines():
            if "__version__" in line:
                number = number_re.findall(line)
                if len(number) == 0:
                    print("版本信息已被删除，无法继续执行升级！")
                    exit(-1)
                now_version = number[0]
                break
    if puppy.to_int(now_version) > puppy.to_int(puppy.get_version()):
        print("请先使用puppya upgrade升级puppy_test框架，再执行puppya update命令，如果已经是最新的puppy_test框架，说明代码的版本信息错误")
        exit(-1)
    _i = input("以下操作将涉及到原文件的删除、修改，请勿终止此命令，否则将导致不可恢复的错误！！！\n建议提前开启Git，以恢复文件\n继续操作请输入y:")
    if _i not in ['y', 'Y']:
        print("终止操作！")
        exit(0)
    # 移动main.py文件
    move_unittest_main()
    print("当前脚本的版本是:{}".format(now_version))
    if now_version == "0.0.0":
        # 从0开始升级
        print("脚本版本更新：0.0.0->0.0.1")
        now_version = "0.0.1"
        # 删除core文件夹
        core_path = os.path.join(cwd, "core")
        if os.path.exists(core_path):
            shutil.rmtree(core_path)
        # 删除plugins文件夹
        plugins_path = os.path.join(cwd, "plugins")
        if os.path.exists(plugins_path):
            shutil.rmtree(plugins_path)
        # 修改test_case文件夹下的内容
        test_case = os.path.join(cwd, "test_case")
        if os.path.exists(test_case):
            for root, dirs, files in os.walk(test_case):
                for file in files:
                    if not file.endswith(".py"):
                        continue
                    file_name = os.path.join(root, file)
                    with open(file_name, "r+", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join(lines)
                        if "APIProcessor" not in content:
                            continue
                        content = content.replace("core", "puppy.core")
                        content = content.replace("import unittest", "import unittest, runner")
                        f.seek(0)
                        f.write(content)
        # 修改fun
        fun_path = os.path.join(cwd, "file", "func.py")
        if os.path.exists(fun_path):
            with open(fun_path, "r+", encoding="utf-8") as f:
                lines = f.readlines()
                content = "".join(lines)
                content = content.replace("from core", "from puppy.core")
                f.seek(0)
                f.write(content)
    if now_version == "0.0.1":
        print("脚本版本更新：0.0.1->0.0.2")
        now_version = "0.0.2"
    if now_version == "0.0.2":
        print("脚本版本更新：0.0.2->0.0.3")
        now_version = "0.0.3"
    # 移动文件
    # 文件检查列表
    check_file_list = [os.path.join("file", "conf", "config.cfg"),
                       os.path.join("file", "xsd", "flow.xsd"),
                       os.path.join("file", "xsd", "interface.xsd"),
                       os.path.join("file", "xsd", "scene.xsd"),
                       os.path.join("file", "func.py"),
                       "runner.py"]
    # 检查关键性文件是否存在
    for _f in check_file_list:
        now_file = os.path.join(cwd, _f)
        static_file = os.path.join(static_path, _f)
        if not os.path.exists(now_file):
            now_file_path = os.path.dirname(now_file)
            if not os.path.exists(now_file_path):
                os.makedirs(now_file_path)
            shutil.copy(static_file, now_file)
    # 替换xsd文件,runner文件
    replace_file_list = [os.path.join("file", "xsd", "flow.xsd"),
                         os.path.join("file", "xsd", "interface.xsd"),
                         os.path.join("file", "xsd", "scene.xsd"),
                         "runner.py"]
    for _f in replace_file_list:
        static_file = os.path.join(static_path, _f)
        new_file = os.path.join(cwd, _f)
        new_file_path = os.path.dirname(new_file)
        if not os.path.exists(new_file_path):
            os.makedirs(new_file_path)
        if os.path.exists(new_file):
            os.remove(new_file)
        shutil.copy(static_file, new_file)
    # 替换puppy插件
    puppy_plugin_path = None
    for root, dirs, files in os.walk(os.path.join(static_path)):
        for file in files:
            if "PuppyPlugin" in file:
                puppy_plugin_path = os.path.join(root, file)
                break
        if puppy_plugin_path:
            break
    if puppy_plugin_path:
        shutil.copy(puppy_plugin_path, cwd)
    print("已完成操作！")
    print("最后：请手动安装生成在根目录的Pycharm插件，其名称为【PuppyPlugin-x.x.x-SNAPSHOT.zip】，用于支持便捷的案例编写！")
elif command == "upgrade":
    server_version = puppy.get_server_version()
    if server_version is None:
        print("服务器不通，请确认是否位于内网！")
        exit(-1)
    if puppy.to_int(server_version) <= puppy.to_int(puppy.get_version()):
        print("没有可供更新的puppy_test框架！")
        exit(-1)
    exec_by_admin(os.path.join(static_path, "upgrade_main.py"))
else:
    server_version = puppy.get_server_version()
    if server_version is None:
        desc = "无法连接到服务器！\n    当前puppy框架版本为：{}".format(puppy.get_version())
    elif puppy.to_int(server_version) > puppy.to_int(puppy.get_version()):
        desc = "服务器有新的框架版本，请更新！\n    当前puppy框架版本为：{}，服务器的版本为：{}".format(puppy.get_version(), server_version)
    else:
        desc = "当前puppy框架版本为：{}".format(puppy.get_version())
    print('''命令输入错误：
    {}
    1、puppym init：初始化
    2、puppym update：更新脚本版本
    3、puppym upgrade：升级puppy_test框架（仅内网可用）'''.format(desc))
