"""
Obserware
Copyright (C) 2021 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import psutil

petabyte = 1024 * 1024 * 1024 * 1024 * 1024
terabyte = 1024 * 1024 * 1024 * 1024
gigabyte = 1024 * 1024 * 1024
megabyte = 1024 * 1024
kilobyte = 1024


def format_partition_size(size):
    if size > petabyte:
        return "%.2fPB" % (size / petabyte)
    elif size > terabyte:
        return "%.2fTB" % (size / terabyte)
    elif size > gigabyte:
        return "%.2fGB" % (size / gigabyte)
    elif size > megabyte:
        return "%.2fMB" % (size / megabyte)
    elif size > kilobyte:
        return "%.2fKB" % (size / kilobyte)
    else:
        return "%.2fB" % (size)


def return_mainscreen_onetimed_statistics():
    retnlist, partlist, partqant = [], psutil.disk_partitions(all=False), 0
    for indx in partlist:
        partqant += 1
        try:
            partdiuj = psutil.disk_usage(indx.mountpoint)
            partfree, partused, partcomp, partperc = (
                partdiuj.free,
                partdiuj.used,
                partdiuj.total,
                partdiuj.percent,
            )
        except:
            partfree, partused, partcomp, partperc = 0, 0, 0, 0
        partdict = {
            "phptnumb": partqant,
            "phptdevc": indx.device,
            "phptfutl": {
                "free": format_partition_size(partfree),
                "used": format_partition_size(partused),
                "comp": format_partition_size(partcomp),
                "perc": partperc,
            },
            "phptfsys": {"mtpt": indx.mountpoint, "fsys": indx.fstype},
            "namedist": {"file": indx.maxfile, "path": indx.maxpath},
        }
        retnlist.append(partdict)
    return retnlist
