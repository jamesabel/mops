
import sys
import threading
import time

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QSystemTrayIcon, QAction, QMenu, QLabel, QVBoxLayout, QLineEdit

import mops.preferences
import mops.gui_systems
import mops.gui_preferences
import mops.server_db
import mops.system_metrics
import mops.util
import mops.logger
import mops.const


class SystemUpdater(threading.Thread):
    """
    runs in the background to update this computer's info
    """
    def __init__(self, update_period, system_metrics, verbose):
        super().__init__()
        self.update_period = update_period
        self.system_metrics = system_metrics
        self.verbose = verbose
        self.exit_event = threading.Event()

    def run(self):
        time.sleep(5)  # todo: implement an event in system_metrics that we can wait on until all system metrics filled in
        mops.logger.log.info('starting SystemUpdater: update_period: %s' % self.update_period)
        while not self.exit_event.is_set():
            mops.logger.log.info('SystemUpdater attempting DB update')
            preferences = mops.preferences.MopsPreferences()
            endpoint, password = preferences.get_redis_login()
            if endpoint and password:
                db = mops.server_db.ServerDB(endpoint, password)
                db.set(self.system_metrics.get_metrics())
            mops.logger.log.info('SystemUpdater waiting for %s seconds' % self.update_period)
            self.exit_event.wait(self.update_period)
        mops.logger.log.info('SystemUpdater leaving run()')

    def request_exit(self):
        self.exit_event.set()
        self.exit_event.wait(60)
        if not self.exit_event.is_set():
            mops.logger.log.warn('exit_event still set')


class App:
    def __init__(self, test_mode, verbose):
        super().__init__()
        self.test_mode = test_mode
        self.verbose = verbose

        self.app = QApplication(sys.argv)  # need this even for the GUIWizard
        self.app.setQuitOnLastWindowClosed(False)  # so popup dialogs don't close the system tray icon

        self.system_metrics = mops.system_metrics.AggregateCollector()
        self.system_metrics.start()

        self._create_tray_icon()
        preferences = mops.preferences.MopsPreferences()
        if self.test_mode:
            self.system_updater = None
        else:
            self.system_updater = SystemUpdater(preferences.get_update_period(), self.system_metrics, self.verbose)
            self.system_updater.start()

    def exec(self):
        self.app.exec_()

    def _systems(self):
        preferences = mops.preferences.MopsPreferences()
        endpoint, password = preferences.get_redis_login()
        systems = None

        if self.test_mode:
            # use this computer's metrics twice just for testing
            systems = self.system_metrics.get_metrics()
            computer_name = mops.system_metrics.get_computer_name()
            systems['system'][computer_name + '_a'] = systems['system'][computer_name].copy()
            systems['system'][computer_name + '_b'] = systems['system'][computer_name].copy()
        else:
            if endpoint and password:
                db = mops.server_db.ServerDB(endpoint, password)
                systems = db.get()
            else:
                mops.logger.log.warn('redis login not set')  # todo: pop up a GUI warning message

        if systems:
            g = mops.gui_systems.GUI(self.verbose)
            g.run(systems)

    def _preferences(self):
        gui_config = mops.gui_preferences.GUIPreferences()
        gui_config.show()
        gui_config.exec_()

    def _about(self):
        about = About()
        about.exec_()

    def _create_tray_icon(self):
        import mops.icons
        self.icon = QIcon(QPixmap(':mops.png'))
        self.trayIcon = QSystemTrayIcon(self.icon)

        self.systems_action = QAction("&Systems", self.trayIcon, triggered=self._systems)
        self.preferences_action = QAction("&Preferences", self.trayIcon, triggered=self._preferences)
        self.about_action = QAction("&About", self.trayIcon, triggered=self._about)
        self.quit_action = QAction("&Quit", self.trayIcon, triggered=self._quit)

        self.trayIconMenu = QMenu()
        self.trayIconMenu.addAction(self.systems_action)
        self.trayIconMenu.addAction(self.preferences_action)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.about_action)
        self.trayIconMenu.addAction(self.quit_action)

        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()

    def _quit(self):
        if self.system_updater:
            self.system_updater.request_exit()
            self.system_updater.join(mops.const.TIMEOUT)
        self.system_metrics.request_exit()
        self.app.quit()


class About(QDialog):
    """
    Make an about box that the user can copy the text from
    """

    def __init__(self):
        super().__init__()
        about_strings = ['www.abel.co', 'http://github.com/jamesabel/mops']
        self.setWindowTitle('mops')

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        layout.addWidget(QLabel('mops'))
        layout.addWidget(QLabel('my operations tool'))

        max_width = mops.util.str_max_width(about_strings)
        for about_string in about_strings:
            line = QLineEdit(about_string)
            line.setReadOnly(True)
            line.setMinimumWidth(max_width)
            layout.addWidget(line)

        self.show()

