
import socket
import datetime
import platform
import collections
import win32api
import psutil
import uptime

"""
gather system metrics/info
"""


def get_computer_name():
    return platform.node()


def get_metrics():
    """
    metrics for this computer
    """
    metrics = {}
    metrics['user'] = win32api.GetUserName()
    metrics['localipv4'] = socket.gethostbyname(socket.gethostname())
    metrics['uptime'] = str(datetime.timedelta(seconds=uptime.uptime()))

    metrics['disk'] = {}
    for disk in psutil.disk_partitions(all=True):
        disk_path = disk[0]
        try:
            total, used, free, percent = psutil.disk_usage(disk_path)
            volume_name, serial_number, max_len, flags, fs_name = win32api.GetVolumeInformation(disk_path)
        except:
            volume_name = None
            used = None
            total = None
        if volume_name:
            disk_name = disk_path[0]
            metrics['disk'][disk_name] = {}
            metrics['disk'][disk_name]['volume'] = volume_name
            metrics['disk'][disk_name]['used'] = str(used)
            metrics['disk'][disk_name]['total'] = str(total)
    return {platform.node(): metrics}
