#!/usr/bin/env python
# coding=utf-8

"""
 Copyright (C) 2010-2013, Ryan Fan <reg_info@126.com>

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Library General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
"""

import logging
import sys

if sys.version_info < (3,):
    import ConfigParser
else:
    import configparser as ConfigParser


LOG = logging.getLogger(__name__)

CONF_FILE = 'ddns.conf'
# Compaitible consideration for v0.1
SYS_CONF_FILE = '/etc/ddns.conf'


class DDNSConfig(object):
    """
    Aliyun DDNS client config class to read/save config stuff
    """

    def __init__(self):
        # default options
        self.interval = 600
        self.access_id = None
        self.access_key = None

        self.parser = ConfigParser.ConfigParser()
        if not self.parser.read(CONF_FILE):
            # Compaitible consideration for v0.1
            if not self.parser.read(SYS_CONF_FILE):
                LOG.error('Failed to read config file.')
                exit(1)

        try:
            self.access_id = self.parser.get('DEFAULT', 'access_id')
            self.access_key = self.parser.get('DEFAULT', 'access_key')
        except Exception as ex:
            LOG.error('Invalid config: %s', ex)
            exit(1)

        if not self.access_id or not self.access_key:
            LOG.error('Invalid access_id or access_key in config file.')
            exit(1)

        if self.parser.has_section('feature_public_ip_from_nic'):
            self.get_feature_public_ip_from_nic_options()
        else:
            self.pifn_enable = False

    def get_domain_record_sections(self):
        """
        Get sections other than default, which contains DomainRecord definition

        :return: section list
        """
        # filter out feature_sections
        sections = self.parser.sections()
        return [s for s in sections if not s.lower().startswith('feature_')]

    def get_option_value(self, section, option, default=None):
        """
        Get specific option value from section, default is None

        :param section: ini file section
        :param option:  init file option
        :param default: default value for option
        :return: option value
        """
        value = default
        try:
            value = self.parser.get(section, option)
        except ConfigParser.NoSectionError:
            LOG.warning('No section: %s', section)
        except ConfigParser.NoOptionError:
            LOG.warning('No option: %s in section: %s', option, section)

        return value

    def get_feature_public_ip_from_nic_options(self):
        """
        Get options about the getting ip from nic.
        """
        section_name = 'feature_public_ip_from_nic'
        try:
            enable = self.parser.getboolean(section_name, 'enable')
        except ValueError as ex:
            LOG.error('Invalid "enable" value in feature public_ip_from_nic config: %s', ex)
            exit(1)
        except ConfigParser.NoOptionError as ex:
            enable = False

        self.pifn_enable = enable
        if enable:
            try:
                self.pifn_interface = self.parser.get(section_name, 'interface')
            except ConfigParser.NoOptionError as ex:
                LOG.error('Invalid "interface" value in feature public_ip_from_nic config: %s', ex)
                exit(1)

            if self.pifn_interface == '':
                LOG.error('Empty "interface" value in feature public_ip_from_nic config')
                exit(1)
