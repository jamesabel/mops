
import socket
import datetime
import platform
import collections
import win32api
import psutil
import uptime


def get_computer_name():
    return platform.node()


def get_metrics():
    metrics = collections.OrderedDict()
    def add(key, value):
        metrics[key] = value
    add('user', win32api.GetUserName())
    add('localipv4', socket.gethostbyname(socket.gethostname()))
    add('uptime', str(datetime.timedelta(seconds=uptime.uptime())))
    disks = psutil.disk_partitions(all=True)
    for disk in disks:
        disk_path = disk[0]
        try:
            total, used, free, percent = psutil.disk_usage(disk_path)
            volume_name, serial_number, max_len, flags, fs_name = win32api.GetVolumeInformation(disk_path)
        except:
            volume_name = None
            used = None
            total = None
        if volume_name:
            prefix = 'disk:' + disk_path[0:1]
            add(prefix + ':volume', volume_name)
            add(prefix + ':used', str(used))
            add(prefix + ':total', str(total))
    return metrics

def main():
    metrics = get_metrics()
    for metric in metrics:
        print(metric, metrics[metric])


if __name__ == '__main__':
    main()

