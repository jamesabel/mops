

import pprint
import os
import subprocess

from PySide.QtGui import QGroupBox, QPushButton, QWidget, QGridLayout, QLabel, QFontMetrics, QLineEdit, QFont


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
        if self.verbose:
            print(command_line)
        subprocess.Popen(command_line, shell=True)


class GUI(QWidget):
    def __init__(self, verbose):
        self.verbose = verbose
        super().__init__()

    def run(self, computers):
        grid_layout = QGridLayout()
        if self.verbose:
            print('GUI:run():')
            pprint.pprint(computers)
        computer_count = 0
        for computer in computers:
            group_box = QGroupBox()
            group_layout = QGridLayout()
            row = 0
            localipv4 = None
            for attribute in computers[computer]:
                if 'localipv4' in attribute:
                    localipv4 = computers[computer][attribute]
                group_layout.addWidget(QLabel(attribute), row, 0)
                value = QLineEdit(computers[computer][attribute])
                value.setReadOnly(True)
                width = QFontMetrics(QFont()).width(computers[computer][attribute]) * 1.05
                value.setMinimumWidth(width)
                group_layout.addWidget(value, row, 1)
                row += 1
            group_box.setTitle(computer)
            group_layout.addWidget(ConnectButton(localipv4, self.verbose))
            group_box.setLayout(group_layout)
            grid_layout.addWidget(group_box, 0, computer_count)
            computer_count += 1
        self.setLayout(grid_layout)
        self.setWindowTitle("mops")
        self.show()





