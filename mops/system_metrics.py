
import socket
import datetime
import platform
import win32api
import psutil
import uptime
import time

import mops.logger

"""
gather system metrics/info
"""


def get_computer_name():
    return platform.node()


def get_metrics():
    """
    metrics for this system
    """
    metrics = {}
    metrics['user'] = win32api.GetUserName()
    metrics['localipv4'] = socket.gethostbyname(socket.gethostname())
    metrics['uptime'] = str(datetime.timedelta(seconds=uptime.uptime()))
    metrics['lastseen'] = str(time.time())

    metrics['disk'] = {}
    disk_partitions = psutil.disk_partitions(all=True)
    mops.logger.log.debug('disk partitions: %s' % str(disk_partitions))
    for disk in disk_partitions:
        disk_path = disk[0]
        volume_name = None
        used = 0
        total = 0
        info_ok = True
        try:
            total, used, free, percent = psutil.disk_usage(disk_path)
        except:
            info_ok = False
            mops.logger.log.debug('psutil.disk_usage(%s)' % str(disk_path))
        try:
            volume_name, serial_number, max_len, flags, fs_name = win32api.GetVolumeInformation(disk_path)
        except:
            info_ok = False
            mops.logger.log.debug('win32api.GetVolumeInformation(%s)' % str(disk_path))

        mops.logger.log.debug('disk_path: %s, volume_name: %s, used: %s, total: %s' %
                              (disk_path, volume_name, str(used), str(total)))
        if info_ok:
            disk_name = disk_path[0]
            metrics['disk'][disk_name] = {}
            metrics['disk'][disk_name]['volume'] = volume_name
            metrics['disk'][disk_name]['used'] = str(used)
            metrics['disk'][disk_name]['total'] = str(total)

    return {get_computer_name(): metrics}
