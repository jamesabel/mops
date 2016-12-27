

from PyQt5.QtGui import *


def str_width(s):
    return QFontMetrics(QFont()).width(s) * 1.05


def str_max_width(strings):
    max_width = 0
    for s in strings:
        if s:
            max_width = max(max_width, str_width(s))
    return max_width


def get_cache_file_path():
    # todo: use appdirs to get the proper path
    return 'cache.tmp'
