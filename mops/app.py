
# TODO: PUT THIS INTO gui_system_tray.py (and perhaps rename that back to app.py)

import sys

from PySide import QtGui
from PySide import QtCore

import mops.preferences
import mops.gui_systems
import mops.gui_preferences
import mops.db
import mops.system_metrics
import mops.util


class App:
    def __init__(self, test_mode, verbose):
        super().__init__()
        self.test_mode = test_mode
        self.verbose = verbose

        self.app = QtGui.QApplication(sys.argv)  # need this even for the GUIWizard
        self.app.setQuitOnLastWindowClosed(False)  # so popup dialogs don't close the system tray icon

        self._create_tray_icon()

    def exec(self):
        self.app.exec_()

    def _systems(self):
        preferences = mops.preferences.MopsPreferences()
        endpoint, password = preferences.get_redis_login()

        if self.test_mode:
            # use this computer's metrics twice just for testing
            computers = {mops.system_metrics.get_computer_name() + '_a': mops.system_metrics.get_metrics(),
                         mops.system_metrics.get_computer_name() + '_b': mops.system_metrics.get_metrics()}
            db = None
        else:
            if endpoint is None or password is None:
                self._preferences()
                endpoint, password = preferences.get_redis_login()
            db = mops.db.DB(endpoint, password, self.verbose)
            db.set(mops.system_metrics.get_computer_name(), mops.system_metrics.get_metrics())
            computers = db.get()

        if self.verbose and db:
            db.dump()
        g = mops.gui_systems.GUI(self.verbose)
        g.run(computers)

    def _preferences(self):
        gui_config = mops.gui_preferences.GUIPreferences()
        gui_config.show()
        gui_config.exec_()

    def _about(self):
        about = About()
        about.exec_()

    def _create_tray_icon(self):
        self.icon = QtGui.QIcon('mops.ico')
        self.trayIcon = QtGui.QSystemTrayIcon(self.icon)

        self.systems_action = QtGui.QAction("&Systems", self.trayIcon, triggered=self._systems)
        self.preferences_action = QtGui.QAction("&Preferences", self.trayIcon, triggered=self._preferences)
        self.about_action = QtGui.QAction("&About", self.trayIcon, triggered=self._about)
        self.quit_action = QtGui.QAction("&Quit", self.trayIcon, triggered=QtGui.qApp.quit)

        self.trayIconMenu = QtGui.QMenu()
        self.trayIconMenu.addAction(self.systems_action)
        self.trayIconMenu.addAction(self.preferences_action)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.about_action)
        self.trayIconMenu.addAction(self.quit_action)

        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()


class About(QtGui.QDialog):
    """
    Make an about box that the user can copy the text from
    """

    def __init__(self):
        super().__init__()
        about_strings = ['www.abel.co', 'http://github.com/jamesabel/mops']
        self.setWindowTitle('mops')

        layout = QtGui.QVBoxLayout(self)
        self.setLayout(layout)

        layout.addWidget(QtGui.QLabel('mops'))
        layout.addWidget(QtGui.QLabel('mini operations tools'))

        max_width = mops.util.str_max_width(about_strings)
        for about_string in about_strings:
            line = QtGui.QLineEdit(about_string)
            line.setReadOnly(True)
            line.setMinimumWidth(max_width)
            layout.addWidget(line)

        self.show()

