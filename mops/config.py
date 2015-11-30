
import os
import configparser

company = 'abel'
application = 'mops'


class MopsConfig:
    def __init__(self):
        config_file_folder = os.path.join(os.getenv('APPDATA'), company, application)
        if not os.path.exists(config_file_folder):
            os.makedirs(config_file_folder)
        self.config_file_path = os.path.join(config_file_folder, 'config.ini')

    def get_config_file_path(self):
        return self.config_file_path

    def set_redis_login(self, endpoint, password):
        config = configparser.ConfigParser()
        config['redis'] = {'endpoint': endpoint, 'password': password}
        with open(self.config_file_path, 'w') as configfile:
            config.write(configfile)

    def get_redis_login(self):
        config = configparser.ConfigParser()
        config.read(self.config_file_path)
        redis_config = config['redis']
        return redis_config['endpoint'], redis_config['password']