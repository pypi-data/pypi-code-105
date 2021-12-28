#!/usr/bin/env python
# coding=utf-8

"""
 Copyright (C) 2010-2013, Ryan Fan

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
import time

from aliddns.config import DDNSConfig
from aliddns.record import DDNSDomainRecordManager
from aliddns.utils import DDNSUtils

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(name)s:%(funcName)s#%(lineno)s] %(message)s')
LOG = logging.getLogger(__name__)


def main():
    """
    Main routine
    """
    config = DDNSConfig()
    record_manager = DDNSDomainRecordManager(config)

    # get current public ip for this server
    if config.pifn_enable:
        current_public_ip = DDNSUtils.get_interface_address(config.pifn_interface)
    else:
        current_public_ip = DDNSUtils.get_current_public_ip()
    if not current_public_ip:
        LOG.error('Failed to get current public ip.')
        exit(1)

    for local_record in record_manager.local_record_list:
        started = time.time()
        dns_resolved_ip = DDNSUtils.get_dns_resolved_ip(local_record.subdomain,
                                                        local_record.domainname)
        cost_ms = (time.time() - started) * 1000
        LOG.info('DNS resolved IP for DomainRecord[%s.%s] is %s, cost: %.3fms',
                 local_record.subdomain, local_record.domainname, dns_resolved_ip, cost_ms)

        if local_record.type == 'AAAA':
            LOG.debug('Getting current IPv6 address for interface[%s]', local_record.interface)
            started = time.time()
            current_ip = DDNSUtils.get_interface_ipv6_address(local_record.interface)
            cost_ms = (time.time() - started) * 1000
            LOG.info('Current IPv6 address for interface[%s] is %s, cost: %.3fms',
                     local_record.interface, current_ip, cost_ms)
        else:
            current_ip = current_public_ip

        if current_ip == dns_resolved_ip:
            LOG.info('Skipped as no changes for DomainRecord[%s.%s/%s]',
                     local_record.subdomain, local_record.domainname, local_record.type)
            continue

        # If current public IP doesn't equal to current DNS resolved ip, only in three cases:
        # 1. The new synced IP for remote record in Aliyun doesn't take effect yet
        # 2. remote record's IP in Aliyun server has changed
        # 3. current public IP is changed
        remote_record = record_manager.fetch_remote_record(local_record)
        if not remote_record:
            LOG.error('Failed to get remote record for DomainRecord[%s.%s]',
                      local_record.subdomain, local_record.domainname)
            continue

        if current_ip == remote_record.value:
            LOG.info('Skipped as no changes for DomainRecord[%s.%s/%s]',
                     local_record.subdomain, local_record.domainname, local_record.type)
            continue

        # if we can fetch remote record and record's value doesn't equal to public IP
        sync_result = record_manager.update(remote_record, current_ip, local_record.type)

        if not sync_result:
            LOG.error('Failed to sync DomainRecord[%s.%s/%s]',
                      local_record.subdomain, local_record.domainname, local_record.type)
        else:
            LOG.info('Synced DomainRecord[%s.%s/%s]',
                     local_record.subdomain, local_record.domainname, local_record.type)


if __name__ == '__main__':
    main()
