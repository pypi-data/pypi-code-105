from setuptools import setup, find_packages

install_requires = [
    "locust~=2.5.0",
    "redis-py-cluster",
    'pluggy==0.13.1',
    "urllib3",
    "loguru",
    "dingtalkchatbot",
    "allure-pytest",
    "pytest-ordering",
    "pymysql",
    "json_tools",
    "pytest~=6.2.5",
    "pako~=0.3.1",
    "websocket-client",
    "Faker",
    "dynaconf",
]

packages = find_packages("src")

long_description = "优化飞书报告展示标题可配置"

setup(name='autoTestScheme',
      version='0.0.9.2',
      url='https://gitee.com/xiongrun/auto-test-scheme',
      author='wuxing',
      description='auto test scheme',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='xr18668178362@163.com',
      install_requires=install_requires,
      project_urls={'Bug Tracker': 'https://gitee.com/xiongrun/auto-test-scheme/issues'},
      package_dir={'': 'src'},
      packages=packages,
      include_package_data=True,
      entry_points={'pytest11': ['pytest_autoTestScheme = autoTestScheme']},
      package_data={
          'demo': ['demo/*'],
          'autoTestScheme': ['allure/*'],
      },
      )
