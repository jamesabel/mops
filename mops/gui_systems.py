
import subprocess
import time
import datetime

from PySide.QtGui import *

import mops.logger
import mops.util
import mops.system_metrics


def component_color(component):
    color = None
    if 'severity' in component:
        if component['severity'] == 'high':
            color = 'red'
        elif component['severity'] == 'medium':
            color = 'yellow'
    return color

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

    def run(self, systems_input):
        if 'system' in systems_input:
            systems = systems_input['system']
            system_count = 0
            disk_counts = set()
            for system in systems:
                for metric in systems[system]:
                    if type(systems[system][metric]) is not str:
                        disk_counts.add(len(systems[system][metric]))
            max_disks = max(disk_counts)

            top_level_layout = QGridLayout()
            for system in sorted(systems, key=str.lower):
                system_box = QGroupBox()
                system_layout = QGridLayout()
                row_number = 0
                localipv4 = None
                for category in sorted(systems[system], key=str.lower):
                    category_box = QGroupBox()
                    category_layout = QGridLayout()
                    category_box.setTitle(category)
                    category_box.setLayout(category_layout)
                    for component in sorted(systems[system][category], key=str.lower):
                        if type(systems[system][category]) is dict:
                            if type(systems[system][category][component]) is dict:
                                if 'value' in systems[system][category][component]:
                                    value = systems[system][category][component]['value']
                                    color = component_color(systems[system][category][component])
                                    if 'Network' in category and 'localipv4' in component:
                                        localipv4 = value  # for RDP connect
                                    if 'last seen' in component.lower():
                                        value = time_to_str(value)
                                    category_layout.addWidget(QLabel(component), row_number, 0)
                                    value_le = QLineEdit(value)
                                    value_le.setReadOnly(True)
                                    if color:
                                        palette = QPalette()
                                        palette.setColor(QPalette.Base, QColor(color))
                                        value_le.setPalette(palette)
                                    value_le.setMinimumWidth(mops.util.str_width(value))
                                    category_layout.addWidget(value_le, row_number, 1)
                                    row_number += 1
                                else:
                                    mops.logger.log.error('no value in: %s' % str(systems[system][category][component]))
                            else:
                                mops.logger.log.error('unexpected component: %s' % str(systems[system][category][component]))
                        else:
                            mops.logger.log.error('unexpected category: %s' % str(systems[system][category]))
                    system_layout.addWidget(category_box)
                system_box.setTitle(system)
                system_layout.addWidget(ConnectButton(localipv4, self.verbose))
                system_box.setLayout(system_layout)
                systems_per_row = 4
                top_level_layout.addWidget(system_box, system_count/systems_per_row, system_count % systems_per_row)
                system_count += 1
            self.setLayout(top_level_layout)
            self.setWindowTitle("Last DB update %s" % time_to_str(systems_input['timestamp']))
            self.show()
            self.exec_()
        else:
            mops.logger.log.error('system not found')


def time_to_str(tv):
    t = time.gmtime(int(float(tv)))
    dt = datetime.datetime(year=t.tm_year, month=t.tm_mon, day=t.tm_mday, hour=t.tm_hour, minute=t.tm_min, second=t.tm_sec)
    dtn = datetime.datetime.utcnow()
    s = "%s (%s ago)" % (time.strftime("%c", t), str(dtn - dt))
    return s