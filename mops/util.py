import os

from PySide.QtGui import *

import mops.const
import mops.logger


def get_cache_file_path():
    return os.path.join(get_appdata_local_folder(), 'cache.json')


def get_appdata_roaming_folder():
    return os.path.join(__get_os_appdata_roaming_folder(), mops.const.COMPANY, mops.const.APPLICATION)


def get_appdata_local_folder():
    return os.path.join(__get_os_appdata_local_folder(), mops.const.COMPANY, mops.const.APPLICATION)


def str_width(s):
    return QFontMetrics(QFont()).width(s) * 1.05


def str_max_width(strings):
    max_width = 0
    for s in strings:
        if s:
            max_width = max(max_width, str_width(s))
    return max_width


def __get_os_appdata_roaming_folder():
    # Things stored here: preferences, etc.
    # Usually smaller files.
    #
    # I'd like to use winpaths.get_local_appdata() but it doesn't seem to work with Python 3, so I'll
    # rely on the environment variable.
    appdata_roaming_folder = os.environ['APPDATA']
    if appdata_roaming_folder is None or len(appdata_roaming_folder) < 1:
        appdata_roaming_folder = os.path.join(os.sep)  # fallback to root
        mops.logger.log.warn("os.environ['APPDATA'] not set, falling back to:%s" % appdata_roaming_folder)
    return appdata_roaming_folder


def __get_os_appdata_local_folder():
    # Things stored here: logs, etc.
    # Can be larger files.
    appdata_local_folder =  os.environ['LOCALAPPDATA']
    if appdata_local_folder is None or len(appdata_local_folder) < 1:
        appdata_local_folder = os.path.join(os.sep)  # fallback to root
    return appdata_local_folder

