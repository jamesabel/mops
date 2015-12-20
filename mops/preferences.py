
import os
import configparser

import mops.const


class MopsPreferences:
    def __init__(self, preferences_folder_path = None):
        if not preferences_folder_path:
            preferences_folder_path = os.path.join(os.getenv('APPDATA'), mops.const.company, mops.const.application)
        if not os.path.exists(preferences_folder_path):
            os.makedirs(preferences_folder_path)
        self._preferences_file_path = os.path.join(preferences_folder_path, 'preferences.ini')
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
        print(dir(self._preferences))
        if 'redis' in self._preferences:
            redis = self._preferences['redis']
            if 'endpoint' in redis:
                endpoint = redis['endpoint']
            if 'password' in redis:
                password = redis['password']
        return endpoint, password

    def set_run_on_windows_startup(self, state):
        self._preferences['preferences'] = {'runonstartup': state}
        self._write()

    def get_run_on_windows_startup(self):
        state = None
        if 'preferences' in self._preferences:
            preferences = self._preferences['preferences']
            if 'runonstartup' in preferences:
                state = preferences['runonstartup']
        return state


def _test():
    c = MopsPreferences('temp')
    print(os.path.abspath(c.get_preferences_file_path()))
    c.clear()
    print(c.get_redis_login())
    print(c.get_run_on_windows_startup())
    c.set_redis_login('my_endpoint', 'my_password')
    c.set_run_on_windows_startup(True)
    print(c.get_redis_login())
    print(c.get_run_on_windows_startup())

if __name__ == '__main__':
    _test()