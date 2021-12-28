# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cannon']

package_data = \
{'': ['*']}

install_requires = \
['exscript==2.6.3', 'loguru==0.5.3', 'traits==6.3.2']

setup_kwargs = {
    'name': 'cannon',
    'version': '0.0.38',
    'description': 'An SSH automation tool based on Exscript',
    'long_description': 'Introduction\n============\n\ncannon is a wrapper around exscript_ to connect with remote server or network \ndevices with ssh.\n\nExample Usage - Cisco IOS\n=========================\n\n.. code:: python\n\n    from cannon import Shell, Account\n\n    sess = Shell(\n        host=\'route-views.routeviews.org\',\n        # route-views doesn\'t need password\n        credentials=(\n            Account(user=\'rviews\', passwd=\'\'),\n        ),\n\n        log_screen=True,\n        log_file="~/mylog.txt",\n        debug=False,\n        )\n\n    sess.execute(\'term len 0\')\n\n    # relax_prompt reduces prompt matching to a minimum... relax_prompt is\n    #     useful if the prompt may change while running a series of commands.\n    sess.execute(\'show clock\', relax_prompt=True)\n\n    sess.execute(\'show version\')\n    version_text = sess.response\n\n    # template is a TextFSM template\n    values = sess.execute(\'show ip int brief\',\n        template="""Value INTF (\\S+)\\nValue IPADDR (\\S+)\\nValue STATUS (up|down|administratively down)\\nValue PROTO (up|down)\\n\\nStart\\n  ^${INTF}\\s+${IPADDR}\\s+\\w+\\s+\\w+\\s+${STATUS}\\s+${PROTO} -> Record""")\n    print("VALUES "+str(values))\n    sess.close()\n\nExample Usage - Linux\n=====================\n\n.. code:: python\n\n    from getpass import getpass, getuser\n    import sys\n    import re\n\n    from cannon import Account, Shell\n\n    """Test for auth fallback, public-key authorization and linux sudo"""\n\n    print("Test logging into linux with ssh...")\n    # Test password fallback and ssh_key authorization...\n    username = getuser()\n    acct01 = Account(username, getpass("Password for %s" % username), ssh_key=\'~/.ssh/id_rsa\')\n\n    conn = Shell(\'localhost\', credentials=(acct01,),\n        mode="linux", debug=False, log_screen=True,\n        strip_colors=True)\n\n    conn.execute(\'uname -a\', timeout=5)\n\n    ########### sudo ##########################################################\n    #\n    index = conn.execute(\'sudo uname -a\', prompts=(r"assword.+?:",))\n    print("INDEX", index)\n    conn.execute(passwd)\n\n    conn.execute(\'sudo ls /tmp\')\n    conn.execute(\'ls\')\n\n    # FIXME, interact() is broken...\n    #conn.interact()\n\n    conn.execute(\'whoami\', command_timeout=5)\n    print("WHOAMI RESULT QUOTED \'{}\'".format(conn.response))\n    conn.execute(\'uptime\', command_timeout=5)\n    print("UPTIME \'{}\'".format(conn.response))\n    conn.close()\n\n\n.. _exscript: https://pypi.python.org/pypi/exscript\n',
    'author': 'Mike Pennington',
    'author_email': 'mike@pennington.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mpenning/cannon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
