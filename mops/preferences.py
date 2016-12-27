
import os
import configparser
import appdirs

import mops.util
import mops.logger
import mops.const


class MopsPreferences:
    """
    read/write to preferences file
    """
    def __init__(self, preferences_folder_path = None):
        if not preferences_folder_path:
            preferences_folder_path = appdirs.user_config_dir(mops.const.APPLICATION, mops.const.COMPANY)
        if not os.path.exists(preferences_folder_path):
            os.makedirs(preferences_folder_path)
        self._preferences_file_path = os.path.join(preferences_folder_path, 'preferences.ini')
        mops.logger.log.info('preferences_file_path: %s' % self._preferences_file_path)
        self._preferences = configparser.ConfigParser()
        self._preferences.read(self._preferences_file_path)

    def _write(self):
        with open(self._preferences_file_path, 'w') as preferences_file:
            self._preferences.write(preferences_file)

    def clear(self):
        self._preferences.clear()
        self._write()

    def get_preferences_file_path(self):
        return self._preferences_file_path

    def set_redis_login(self, endpoint, password):
        self._preferences['redis'] = {'endpoint': endpoint, 'password': password}
        self._write()

    def get_redis_login(self):
        endpoint = None
        password = None
        if 'redis' in self._preferences:
            redis = self._preferences['redis']
            if 'endpoint' in redis:
                endpoint = redis['endpoint']
            if 'password' in redis:
                password = redis['password']
        return endpoint, password

    def set_run_on_startup(self, state):
        self._preferences['preferences'] = {'runonstartup': state}
        self._write()

    def set_update_period(self, period):
        self._preferences['preferences'] = {'updateperiod': period}

    def get_update_period(self):
        update_period = 24 * 60 * 60  # default
        if 'preferences' in self._preferences:
            p = self._preferences['preferences']
            if 'updateperiod' in p:
                update_period = p['updateperiod']
        return update_period

    def get_run_on_startup(self):
        state = None
        if 'preferences' in self._preferences:
            preferences = self._preferences['preferences']
            if 'runonstartup' in preferences:
                state = bool(preferences['runonstartup'])
        return state

