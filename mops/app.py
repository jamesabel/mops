
# TODO: PUT THIS INTO gui_system_tray.py (and perhaps rename that back to app.py)

import sys
import threading

from PySide import QtGui

import mops.preferences
import mops.gui_systems
import mops.gui_preferences
import mops.db
import mops.system_metrics
import mops.util
import mops.logger


class SystemUpdater(threading.Thread):
    """
    runs in the background to update this computer's info
    """
    def __init__(self, update_period, verbose):
        super().__init__()
        self.update_period = update_period
        self.verbose = verbose
        self.exit_event = threading.Event()

    def run(self):
        mops.logger.log.info('starting SystemUpdater: update_period: %s' % self.update_period)
        while not self.exit_event.is_set():
            mops.logger.log.info('SystemUpdater attempting DB update')
            preferences = mops.preferences.MopsPreferences()
            endpoint, password = preferences.get_redis_login()
            if endpoint and password:
                db = mops.db.DB(endpoint, password)
                db.set(mops.system_metrics.get_metrics())
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

        if self.verbose:
            mops.logger.log.info('appdata_roaming_folder:%s', mops.util.get_appdata_roaming_folder())
            mops.logger.log.info('appdata_local_folder:%s', mops.util.get_appdata_local_folder())

        self.app = QtGui.QApplication(sys.argv)  # need this even for the GUIWizard
        self.app.setQuitOnLastWindowClosed(False)  # so popup dialogs don't close the system tray icon

        self._create_tray_icon()
        preferences = mops.preferences.MopsPreferences()
        self.system_updater = SystemUpdater(preferences.get_update_period(), self.verbose)
        self.system_updater.start()

    def exec(self):
        self.app.exec_()

    def _systems(self):
        preferences = mops.preferences.MopsPreferences()
        endpoint, password = preferences.get_redis_login()
        systems = None

        if self.test_mode:
            # use this computer's metrics twice just for testing
            cs = mops.system_metrics.get_metrics()
            computer_name = mops.system_metrics.get_computer_name()
            systems = {}
            systems[computer_name + '_a'] = cs[computer_name]
            systems[computer_name + '_b'] = cs[computer_name]
        else:
            if endpoint and password:
                db = mops.db.DB(endpoint, password)
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
        self.icon = QtGui.QIcon(QtGui.QPixmap(':mops.png'))
        self.trayIcon = QtGui.QSystemTrayIcon(self.icon)

        self.systems_action = QtGui.QAction("&Systems", self.trayIcon, triggered=self._systems)
        self.preferences_action = QtGui.QAction("&Preferences", self.trayIcon, triggered=self._preferences)
        self.about_action = QtGui.QAction("&About", self.trayIcon, triggered=self._about)
        self.quit_action = QtGui.QAction("&Quit", self.trayIcon, triggered=self._quit)

        self.trayIconMenu = QtGui.QMenu()
        self.trayIconMenu.addAction(self.systems_action)
        self.trayIconMenu.addAction(self.preferences_action)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.about_action)
        self.trayIconMenu.addAction(self.quit_action)

        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()

    def _quit(self):
        self.system_updater.request_exit()
        QtGui.qApp.quit()


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
        layout.addWidget(QtGui.QLabel('my operations tool'))

        max_width = mops.util.str_max_width(about_strings)
        for about_string in about_strings:
            line = QtGui.QLineEdit(about_string)
            line.setReadOnly(True)
            line.setMinimumWidth(max_width)
            layout.addWidget(line)

        self.show()

