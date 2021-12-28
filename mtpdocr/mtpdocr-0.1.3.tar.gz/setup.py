from setuptools import setup, find_packages
VERSION = '0.1.3'

setup(name='mtpdocr',
      version=VERSION,
      description="OCR",
      long_description='just enjoy',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python OCR base on paddleOCR',
      author='allen',
      author_email='310315734@qq.com',
      url='https://github.com/AllenCall/paddleOCRDemo',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      # dependency_links=[
      #     "https://mirror.baidu.com/pypi/simple",
      #     "https://pypi.python.org/simple"
      # ],
      install_requires=[
        'paddleocr == 2.2',
        'paddlepaddle',
      ],
      entry_points={
        'console_scripts':[
            'mtpdocr = OCR.getCor:getCor'
        ]
      },
)