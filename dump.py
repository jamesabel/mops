
# dumps the user's redis database

import pprint
import os
import logging

import mops.logger
import mops.preferences
import mops.db


def main():
    out_folder = os.path.join('temp', 'dump')
    out_file_name = 'dump.txt'

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    mops.logger.init(out_folder)
    mops.logger.set_file_log_level(logging.DEBUG)

    pref = mops.preferences.MopsPreferences()
    print('preferences file path: %s' % pref.get_preferences_file_path())
    endpoint, password = pref.get_redis_login()
    db = mops.db.DB(endpoint, password, info_type='*')
    out_file_path = os.path.join(out_folder, out_file_name)
    print('writing to %s' % out_file_path)
    with open(out_file_path, 'w') as f:
        pprint.pprint(db.get(), f)
    print('also see log file for raw database data')

if __name__ == '__main__':
    main()