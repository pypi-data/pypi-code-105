# -*- coding: utf-8 -*-
# @Time    : 2021/11/11 14:42
# @Author  : wyw
import shutil
'''
    2021-11-18 修改demo 注释说明
    2021-11-12 新增功能:
    se_single 对整个工程代码加密成单独文件可避免模块结构暴露 , 只会加密代码部分，加密后产生的代码空目录不能删除,
    1. se_project 工程加密处理:
        源码工程目录参考示例 
        /home/project
                    script
                          run.sh
                          ...
                    serving # 源码目录
                          config
                                 config.py
                                ...
                          utils
                                ...
                          runner.py #程序主入口 main()


    2. 注册运行解析器
        se_register_module(root_dir)
        root_dir 加密工程根路径 上例root_dir目录: /home/project_se
'''

#package_name 如果制作.whl , 自定义设置包，否则默认为包含代码的最近目录名
def test_se_project(src_dir = '/home/project',dst_dir = '/home/project_se' , package_name=None,ext='.pys'):
    from se_code import se_project
    #目标文件夹存在则自动删除
    dst_exists_remove = False
    #对工程代码加密成单独文件
    se_single = False
    #忽略复制文件，文件对工程运行没有用
    ignore = shutil.ignore_patterns('test','.git','.idea','setup.py')

    #package_name
    # 如果是pypi包，package_name 需要设置包名,否则可以设置None

    #加密接受规则
    rules = ['serving/utils/*', 'serving/run*', 'serving/http_client/http*']
    se_project(src_dir,
        dst_dir,
        package_name=package_name,
        ext=ext,
        dst_exists_remove=dst_exists_remove,
        se_single=se_single,
        ignore = ignore,
        rules = rules,
        key=bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
        iv=bytes([1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    )

def run():

    # 如果是pip 包加密，例如包名为 nn_serving , module_root_dir=os.path.dirname(nn_serving.__file__)
    # demo 对于此示例 /home/project_se/serving/start.py , 代码模块都在 /home/project_se/serving,  module_root_dir=/home/project_se/serving
    import sys,os
    sys.path.append('..')
    from se_code import se_register_module
    #root_dir目录下必须存在__meta__目录下必须存在__meta__.pys
    #root_dir='/home/project_se'

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    se_register_module(root_dir=root_dir)
    from serving.runner import main
    main()
