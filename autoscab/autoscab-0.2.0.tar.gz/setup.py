# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoscab', 'autoscab.constants', 'autoscab.deployments', 'autoscab.identity']

package_data = \
{'': ['*'], 'autoscab': ['captchaAudio/*']}

install_requires = \
['Faker>=10.0.0,<11.0.0',
 'SpeechRecognition>=3.8.1,<4.0.0',
 'certifi>=2021.10.8,<2022.0.0',
 'charset-normalizer>=2.0.9,<3.0.0',
 'fpdf>=1.7.2,<2.0.0',
 'idna>=3.3,<4.0',
 'pandas>=1.3.5,<2.0.0',
 'pdf2image>=1.16.0,<2.0.0',
 'pydub>=0.25.1,<0.26.0',
 'requests>=2.26.0,<3.0.0',
 'selenium>=3,<4',
 'urllib3>=1.26.7,<2.0.0',
 'webdriver-manager>=3.5.2,<4.0.0']

entry_points = \
{'console_scripts': ['autoscab = autoscab.main:main']}

setup_kwargs = {
    'name': 'autoscab',
    'version': '0.2.0',
    'description': 'apply for many of the same job',
    'long_description': '# autoscab\n\n------------\n\nStill experimental! Tools for automatically applying for many of the same job.\n\n## Installation\n\nYou will need \n\n- Python 3 (most operating systems come with it preinstalled, otherwise see the [download page](https://www.python.org/downloads/))\n- pip (you should have it, otherwise type `python -m ensurepip --upgrade` into your command line/terminal)\n\nFor all of this you will need to be on your command line or terminal! \n\n- Mac: Go to "Applications," then "Utilities" then "Terminal"\n- Windows: (someone help me out here I don\'t use windows!)\n\n### From PyPI: \n\n```\npip install autoscab\n```\n\n### From GitHub:\n\nEither download the code using the green "Code" button above and to the right, and then clicking "Download Zip,"\nand unzip the files into a directory, or use `git clone https://github.com/sneakers-the-rat/autoscab.git` if you have git installed\n\nThen, opening a terminal/command prompt in that directory (use `cd` in linux/mac and `dir` in windows to change directories), type:\n\n```pip install .```\n\n## Usage\n\nTo get help, type `autoscab --help`\n\n```\n(autoscab--E_yShkX-py3.8) bash-3.2$ autoscab --help\nusage: APPLY FOR MANY OF THE SAME JOB [-h] [-n N] [--relentless] [--list] [--noheadless] [--leaveopen]\n                                      [deployment]\n\npositional arguments:\n  deployment    Which deployment to run\n\noptional arguments:\n  -h, --help    show this help message and exit\n  -n N          Apply for n jobs (default: 1)\n  --relentless  Keep applying forever\n  --list        List all available deployments and exit\n  --noheadless  Show the chromium driver as it fills in the application\n  --leaveopen   Try to leave the browser open after an application is completed\n\nIF THEY WANT SCABS, WE\'LL GIVE EM SCABS\n\n```\n\nThe basic usage is \n\n```\nautoscab <NAME_OF_DEPLOYMENT>\n```\n\nSo for example\n\n```\nautoscab fredmeyer\n```\n\nYou can then customize how many applications you want to submit with `-n`, run it indefinitely with `--relentless`,\nor show the window as the application is being submitted with `--noheadless`\n\n```angular2html\nautoscab fredmeyer --relentless --noheadless\n```\n\nor\n\n```\nautoscab fredmeyer -n 3 --leaveopen\n```\n\n## Contribution\n\n**TODO!**\n\n# Original KelloggBot Readme:\n\n# KelloggBot\n[Setup](#setup)\\\n[Usage](#usage)\n\nCredit to SeanDaBlack for the basis of the script.\n\nmain.py is selenium python bot.\nsc.js is a the base of the ios shortcut [COMING SOON]\n\n# Setup\n\nOn mac/pc:\n\n`pip install -r requirements.txt`\n\nThis will install `webdriver-manager` to automatically download the correct chrome driver. If you are having issues opening having it open chrome, check https://github.com/SergeyPirogov/webdriver_manager.\n\nPoppler must also be installed for pdf2image. Follow the instructions at https://pdf2image.readthedocs.io/en/latest/installation.html to install.\n\nIt needs to be found in your `PATH` variable.\n\n`export PATH=$PATH:$(pwd)`\n\n`python main.py` to run. It will loop until you kill the job. `ctrl + c` in your terminal to give the pro lifes a break (optional).\n\nmac:\n\nYou might also get a trust issue with the downloaded driver being unverified. To fix that, run \n\n`xattr -d com.apple.quarantine chromedriver`\n\nthis just tells the OS it\'s safe to use this driver, and Selenium will start working. See https://timonweb.com/misc/fixing-error-chromedriver-cannot-be-opened-because-the-developer-cannot-be-verified-unable-to-launch-the-chrome-browser-on-mac-os/ for more info.\n\nYou will also need to install ffmpeg if it is not already installed: [Mac installation guide](https://superuser.com/a/624562) [Windows installation guide](https://www.wikihow.com/Install-FFmpeg-on-Windows)\n\n# Usage\n```\nusage: A script to automate very legitimate applications to kellogg\'s production plants affected by union strikes\n       python3 main.py [-h] [--debug] [--mailtm]\n\noptions:\n  -h, --help  show this help message and exit\n  --debug     Puts script in a \'debug\' mode where the Chrome GUI is visible\n  --mailtm    Uses mail.tm instead of guerrilla mail by default\n\nKellogg bad | Union good | Support strike funds\n```\n',
    'author': 'sneakers-the-rat',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sneakers-the-rat/autoscab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
