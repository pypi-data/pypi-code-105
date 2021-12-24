from distutils.core import setup


setup(
    name='666',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='这个模块有点东西哦',  # 描述
    author='赵佳乐',  # 作者
    author_email='488635489@qq.com',  
    py_modules=['module_A', 'module_A2']  # 要发布的模块
)