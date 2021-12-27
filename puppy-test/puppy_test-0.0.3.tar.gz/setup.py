from setuptools import find_packages, setup

setup(
    # 使用pip安装和卸载使用的名称
    name='puppy_test',
    # todo:版本号：注意同时修改puppy模块的版本号、runner文件的版本号
    version='0.0.3',
    # 作者
    author='Li Junxian',
    # 作者邮箱
    author_email='yk690520@outlook.com',
    # 自动导入模块
    packages=find_packages(),
    # 脚本
    scripts=['puppym.py'],
    # 需要附加的数据文件
    package_data={
        'puppy': ['static/*.*', 'static/.gitignore', 'static/file/*.*', 'static/flow/*.*', 'static/interface/*.*',
                  'static/file/conf/*.*','static/test_case/*.*', 'static/test_data/*.*',
                  'static/file/plugins/*.*', 'static/file/xsd/*.*']},
    # 需要安装的依赖
    install_requires=[
        'requests>=2.25.0'
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)
