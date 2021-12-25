from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='honeypots',
    author='QeeqBox',
    author_email='gigaqeeq@gmail.com',
    description=r"21 different honeypots in a single PyPI package for monitoring network traffic, bots activities, and username \ password credentials (DNS, HTTP Proxy, HTTP, HTTPS, SSH, POP3, IMAP, STMP, VNC, SMB, SOCKS5, Redis, TELNET, Postgres, MySQL, MSSQL, Elastic, LDAP, NTP, Memcache, SNMP, and Oracle) ",
    long_description=long_description,
    version='0.35',
    license="AGPL-3.0",
    url="https://github.com/qeeqbox/honeypots",
    packages=['honeypots'],
    scripts=['honeypots/honeypots'],
    include_package_data=True,
    install_requires=[
        'pipenv',
        'twisted',
        'psutil',
        'psycopg2-binary',
        'dnspython',
        'requests',
        'impacket',
        'paramiko==2.7.1',
        'redis',
        'mysql-connector',
        'pycryptodome',
        'vncdotool',
        'service_identity',
        'requests[socks]',
        'pygments',
        'scapy',
        'netifaces',
        'elasticsearch',
        'pymssql',
        'ldap3'
    ],
    python_requires='>=3.5'
)
