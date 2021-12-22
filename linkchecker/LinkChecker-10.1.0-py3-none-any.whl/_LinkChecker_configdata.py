# -*- coding: iso-8859-1 -*-
# this file is automatically created by setup.py
install_purelib = '/'
install_platlib = '/LinkChecker-10.1.0.data/platlib'
install_lib = '/'
install_headers = '/LinkChecker-10.1.0.data/headers'
install_scripts = '/LinkChecker-10.1.0.data/scripts'
config_dir = '/LinkChecker-10.1.0.data/data/share/linkchecker'
install_data = '/LinkChecker-10.1.0.data/data'
name = 'LinkChecker'
version = '10.1.0'
author = 'LinkChecker Authors'
author_email = 'UNKNOWN'
maintainer = 'LinkChecker Authors'
maintainer_email = 'UNKNOWN'
url = 'https://linkchecker.github.io/linkchecker/'
license = 'GPL'
description = 'check links in web documents or full websites'
long_description = 'LinkChecker\n============\n\n|Build Status|_ |License|_\n\n.. |Build Status| image:: https://github.com/linkchecker/linkchecker/actions/workflows/build.yml/badge.svg?branch=master\n.. _Build Status: https://github.com/linkchecker/linkchecker/actions/workflows/build.yml\n.. |License| image:: https://img.shields.io/badge/license-GPL2-d49a6a.svg\n.. _License: https://opensource.org/licenses/GPL-2.0\n\nCheck for broken links in web sites.\n\nFeatures\n---------\n\n- recursive and multithreaded checking and site crawling\n- output in colored or normal text, HTML, SQL, CSV, XML or a sitemap graph in different formats\n- HTTP/1.1, HTTPS, FTP, mailto:, news:, nntp:, Telnet and local file links support\n- restrict link checking with regular expression filters for URLs\n- proxy support\n- username/password authorization for HTTP, FTP and Telnet\n- honors robots.txt exclusion protocol\n- Cookie support\n- HTML5 support\n- a command line and web interface\n- various check plugins available\n\nInstallation\n-------------\n\nPython 3.6 or later is needed. Using pip to install LinkChecker:\n\n``pip3 install linkchecker``\n\nThe version in the pip repository may be old, to find out how to get the latest\ncode, plus platform-specific information and other advice see `doc/install.txt`_\nin the source code archive.\n\n.. _doc/install.txt: doc/install.txt\n\n\nUsage\n------\nExecute ``linkchecker https://www.example.com``.\nFor other options see ``linkchecker --help``, and for more information the\nmanual pages `linkchecker(1)`_ and `linkcheckerrc(5)`_.\n\n.. _linkchecker(1): https://linkchecker.github.io/linkchecker/man/linkchecker.html\n\n.. _linkcheckerrc(5): https://linkchecker.github.io/linkchecker/man/linkcheckerrc.html\n\nDocker usage\n-------------\n\nIf you do not want to install any additional libraries/dependencies you can use\nthe Docker image which is published on GitHub Packages.\n\nExample for external web site check::\n\n  docker run --rm -it -u $(id -u):$(id -g) ghcr.io/linkchecker/linkchecker:latest --verbose https://www.example.com\n\nLocal HTML file check::\n\n  docker run --rm -it -u $(id -u):$(id -g) -v "$PWD":/mnt ghcr.io/linkchecker/linkchecker:latest --verbose index.html\n\nIn addition to the rolling latest image, uniquely tagged images can also be found\non the `packages`_ page.\n\n.. _packages: https://github.com/linkchecker/linkchecker/pkgs/container/linkchecker\n'
keywords = ['link', 'url', 'site', 'checking', 'crawling', 'verification', 'validation']
platforms = ['UNKNOWN']
fullname = 'LinkChecker-10.1.0'
contact = 'LinkChecker Authors'
contact_email = 'UNKNOWN'
release_date = "2021-12-22"
portable = 0
