
import os
import configparser

company = 'abel'
application = 'mops'


class MopsConfig:
    def __init__(self, config_folder_path = None):
        if not config_folder_path:
            config_folder_path = os.path.join(os.getenv('APPDATA'), company, application)
        if not os.path.exists(config_folder_path):
            os.makedirs(config_folder_path)
        self._config_file_path = os.path.join(config_folder_path, 'config.ini')
        self._config = configparser.ConfigParser()

    def _write(self):
        with open(self._config_file_path, 'w') as configfile:
            self._config.write(configfile)

    def clear(self):
        self._config.clear()
        self._write()

    def get_config_file_path(self):
        return self._config_file_path

    def set_redis_login(self, endpoint, password):
        self._config['redis'] = {'endpoint': endpoint, 'password': password}
        self._write()

    def get_redis_login(self):
        endpoint = None
        password = None
        if 'redis' in self._config:
            redis = self._config['redis']
            if 'endpoint' in redis:
                endpoint = redis['endpoint']
            if 'password' in redis:
                password = redis['password']
        return endpoint, password

    def set_run_on_windows_startup(self, state):
        self._config['preferences'] = {'runonstartup': state}
        self._write()

    def get_run_on_windows_startup(self):
        state = None
        if 'preferences' in self._config:
            preferences = self._config['preferences']
            if 'runonstartup' in preferences:
                state = preferences['runonstartup']
        return state


def _test():
    c = MopsConfig('temp')
    print(os.path.abspath(c.get_config_file_path()))
    c.clear()
    print(c.get_redis_login())
    print(c.get_run_on_windows_startup())
    c.set_redis_login('my_endpoint', 'my_password')
    c.set_run_on_windows_startup(True)
    print(c.get_redis_login())
    print(c.get_run_on_windows_startup())

if __name__ == '__main__':
    _test()