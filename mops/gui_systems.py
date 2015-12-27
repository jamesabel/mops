
import subprocess
import datetime
import time

from PySide.QtGui import *

import mops.logger
import mops.util
import mops.system_metrics


class ConnectButton(QPushButton):
    def __init__(self, localipv4, verbose):
        self.verbose = verbose
        super().__init__('Connect (%s)' % localipv4)
        self.localipv4 = localipv4
        self.clicked.connect(self.do_connect)

    def do_connect(self):
        # http://windows.microsoft.com/en-us/windows/command-line-parameters-remote-desktop-connection#1TC=windows-7
        command_line = 'mstsc.exe'  # os.path.join('c:', os.sep, 'Windows', 'system32', 'mstsc.exe')
        command_line += ' /v:' + self.localipv4
        mops.logger.log.info(command_line)
        subprocess.Popen(command_line, shell=True)


class GUI(QDialog):
    def __init__(self, verbose):
        self.verbose = verbose
        super().__init__()

    def run(self, systems):
        def add_row(metric, value, row_number, color=None):
            group_layout.addWidget(QLabel(metric), row_number, 0)
            value_le = QLineEdit(value)
            value_le.setReadOnly(True)
            if color:
                palette = QPalette()
                palette.setColor(QPalette.Base, QColor(color))
                value_le.setPalette(palette)
            value_le.setMinimumWidth(mops.util.str_width(value))
            group_layout.addWidget(value_le, row_number, 1)

        grid_layout = QGridLayout()
        system_count = 0
        disk_counts = set()
        for system in systems:
            for metric in systems[system]:
                if type(systems[system][metric]) is not str:
                    disk_counts.add(len(systems[system][metric]))
        max_disks = max(disk_counts)

        for system in sorted(systems, key=str.lower):
            group_box = QGroupBox()
            group_layout = QGridLayout()
            row_number = 0
            localipv4 = None
            for metric in sorted(systems[system]):
                value = systems[system][metric]
                if type(value) is str:
                    if 'localipv4' in metric:
                        localipv4 = value  # for RDP connect
                    if metric == 'lastseen':
                        add_row('last seen', str(datetime.timedelta(seconds = time.time() - float(value))), row_number)
                    else:
                        add_row(metric, value, row_number)
                    row_number += 1
                else:
                    for disk in sorted(systems[system][metric], key=str.lower):
                        if 'volume' in sorted(systems[system][metric][disk]):
                            name = systems[system][metric][disk]['volume']
                            total = systems[system][metric][disk]['total']
                            used = systems[system][metric][disk]['used']
                            used_ratio = float(used)/float(total)

                            color = None
                            # uses predefined colors:
                            # https://srinikom.github.io/pyside-docs/PySide/QtGui/QColor.html#PySide.QtGui.QColor
                            if used_ratio >= 0.9:
                                color = 'red'
                            elif used_ratio >= 0.8:
                                color = 'yellow'

                            add_row(name + ' (' + disk + ':)', '{:.2%}'.format(used_ratio), row_number, color)
                            row_number += 1
                        else:
                            mops.logger.log.warn('error: %s' % disk)
                    # spaces so disks for all systems take up the same number of rows
                    for _ in range(0, max_disks - len(systems[system][metric])):
                        group_layout.addWidget(QLabel(''))
                        row_number += 1
            group_box.setTitle(system)
            group_layout.addWidget(ConnectButton(localipv4, self.verbose))
            group_box.setLayout(group_layout)
            systems_per_row = 4
            grid_layout.addWidget(group_box, system_count/systems_per_row, system_count % systems_per_row)
            system_count += 1
        self.setLayout(grid_layout)
        self.setWindowTitle("mops")
        self.show()
        self.exec_()
