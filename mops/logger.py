
import os
import appdirs
import logging
import logging.handlers

import mops.const
import mops.util

fh = None
ch = None
log = None
log_folder = None


def init(log_folder_param=None):
    global fh, ch, log, log_folder

    if log_folder_param:
        log_folder = log_folder_param  # mainly for testing
    else:
        log_folder = calculate_log_folder()

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log = logging.getLogger(mops.const.APPLICATION)
    
    log.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.handlers.RotatingFileHandler(os.path.join(log_folder, mops.const.LOG_FILE_NAME),
                                              maxBytes=20*1E6, backupCount=3)
    #fh = logging.FileHandler(LOG_FILE_NAME)
    fh.setLevel(logging.INFO)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)

    return log_folder


def get_log_folder():
    return log_folder


def set_file_log_level(new_level):
    fh.setLevel(new_level)


def set_console_log_level(new_level):
    ch.setLevel(new_level)

def calculate_log_folder():
    return os.path.join(appdirs.user_log_dir(mops.const.APPLICATION, mops.const.COMPANY))