
import socket
import datetime
import platform
import time
import threading
import multiprocessing

import win32api
import psutil
import uptime

import winstats

import mops.logger

"""
gather system metrics/info
"""


# the winstat module (how to get to the OS counters)
# https://pypi.python.org/pypi/winstats
# Recognizing a Processor Bottleneck:
# https://technet.microsoft.com/en-us/library/cc938609.aspx
# Identifying Potential Bottlenecks (and Thresholds):
# https://technet.microsoft.com/en-us/library/cc938549.aspx

def get_computer_name():
    return platform.node()


def ratio_to_severity_level(ratio, high_level, medium_level):
    severity_level = 'low'
    if ratio >= high_level:
        severity_level = 'high'
    elif ratio >= medium_level:
        severity_level = 'medium'
    return severity_level


class Collector(threading.Thread):
    minute = 60
    hour = minute * 60
    day = hour * 24

    def __init__(self, period_seconds):
        self.period_seconds = period_seconds
        self.metrics = {}
        self.category = None  # derived class provides this
        self.loop_event = threading.Event()
        super().__init__()

    def run(self):
        mops.logger.log.debug('run:enter:%s' % type(self).__name__)
        self.take_sample()
        while not self.loop_event.is_set():
            self.take_sample()
            self.loop_event.wait(self.period_seconds)
        mops.logger.log.debug('run:exit:%s' % type(self).__name__)

    def take_sample(self):
        raise NotImplementedError  # derived class provides this

    def get_metrics(self):
        return {self.category: self.metrics}

    def request_exit(self):
        self.loop_event.set()


class ProcessorCollector(Collector):
    def __init__(self):
        super().__init__(1)
        self.category = 'Processor'
        self.processor_queue_length_sum = 0
        self.processor_sum_sum = 0
        self.processor_max_sum = 0
        self.sample_count = 0

    def take_sample(self):
        self.sample_count += 1

        processor_count = multiprocessing.cpu_count()

        # take all data with one call
        counters = [r'\System\Processor Queue Length']
        fmts = ['double']
        for processor in range(0, processor_count):
            counters.append(r'\Processor(' + str(processor) + r')\% Processor Time')
            fmts.append('double')
        delay = int((self.period_seconds * 1000)/2)  # take the "second snapshot" in the middle of the period
        sample = winstats.get_perf_data(counters, fmts=fmts, delay=delay)

        mops.logger.log.debug('winstats.get_perf_data:%s' % str(sample))

        # when Processor Queue Length (PQL) is large, it is usually opportunity for more cores
        self.processor_queue_length_sum += sample[0]
        pql_avg = float(self.processor_queue_length_sum)/float(self.sample_count)
        pql_severity = ratio_to_severity_level(pql_avg, 1.0, 0.5)
        self.metrics['Average PQL'] = {'value': str(pql_avg), 'severity': pql_severity}

        # Sum processor activity across all processors - this is relative to 'how much of a single processor' is being
        # used.  Note that this is scaled so 1.0 means we're using one processor's worth, 2.0 is 2 processors, etc.
        self.processor_sum_sum += sum(sample[1:])/100.0
        processor_sum_avg = float(self.processor_sum_sum)/float(self.sample_count)
        self.metrics['Average Load (number of processors)'] = {'value': '{:.3}'.format(processor_sum_avg)}

        # Determine how often one processor is saturated.  Note that due to core migration, even if a single
        # thread is running continually it will appear across all core (unless it is affinitized).
        self.processor_max_sum += max(sample[1:])
        proc_avg_max = (float(self.processor_max_sum)/float(self.sample_count))/100.0
        proc_avg_max_severity = ratio_to_severity_level(proc_avg_max, 85.0, 75.0)
        self.metrics['Average Max Processor Load'] = {'value': '{:.1%}'.format(proc_avg_max), 'severity': proc_avg_max_severity}


class DiskCollector(Collector):
    def __init__(self):
        super().__init__(self.hour)
        self.category = 'Disks'

    def take_sample(self):
        disk_stats = {}
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
                disk_name = volume_name + ' (' + disk_path[0] + ')'
                disk_stats[disk_name] = {}
                # disk_stats[disk_name]['volume'] = volume_name
                disk_stats[disk_name]['used'] = str(used)
                disk_stats[disk_name]['total'] = str(total)
                used_ratio = float(used)/float(total)
                disk_stats[disk_name]['value'] = '{:.1%}'.format(used_ratio)
                disk_stats[disk_name]['severity'] = ratio_to_severity_level(used_ratio, 0.85, 0.75)
        self.metrics = disk_stats


class NetworkCollector(Collector):
    def __init__(self):
        super().__init__(self.minute)
        self.category = 'Network'

    def take_sample(self):
        self.metrics['localipv4'] = {'value': socket.gethostbyname(socket.gethostname())}


class SystemCollector(Collector):
    def __init__(self):
        super().__init__(self.hour)
        self.category = 'System'

    def take_sample(self):

        # memory
        mem = psutil.virtual_memory()
        mem_used = mem.total - mem.available
        mem_used_ratio = float(mem_used)/float(mem.total)
        if mem_used_ratio > 0.9 or mem.available <= 0.5E9:
            severity = 'high'
        elif mem_used_ratio > 0.8 or mem.available <= 1E9:
            severity = 'medium'
        else:
            severity = 'low'
        self.metrics['Memory'] = {'value': '{:.1%}'.format(mem_used_ratio), 'severity':severity, 'used': str(mem.used),
                                  'total': str(mem.total)}

        self.metrics['User'] = {'value': win32api.GetUserName()}
        self.metrics['Up time'] = {'value': str(datetime.timedelta(seconds=uptime.uptime()))}
        self.metrics['CPU count'] = {'value': str(multiprocessing.cpu_count())}
        self.metrics['Last seen'] = {'value': str(time.time())}  # client display calculates time delta from this


class AggregateCollector():
    def __init__(self):
        super().__init__()
        self.collectors = []
        self.collectors.append(SystemCollector())
        self.collectors.append(ProcessorCollector())
        self.collectors.append(DiskCollector())
        self.collectors.append(NetworkCollector())

    def start(self):
        for collector in self.collectors:
            collector.start()

    def request_exit(self):
        for collector in self.collectors:
            collector.request_exit()
        for collector in self.collectors:
            collector.join()

    def get_metrics(self):
        aggregate_metrics = {}
        for collector in self.collectors:
            aggregate_metrics.update(collector.get_metrics())
        return {'system': {get_computer_name(): aggregate_metrics}}


def main():
    import pprint

    mops.logger.init('temp')
    aggregate_collector = AggregateCollector()
    aggregate_collector.start()
    time.sleep(5)
    pprint.pprint(aggregate_collector.get_metrics())
    aggregate_collector.request_exit()

if __name__ == '__main__':
    main()
