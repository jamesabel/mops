
import argparse
import logging

from PyQt5 import QtGui

import mops.app
import mops.gui_systems
import mops.preferences
import mops.logger


def main():
    mops.logger.init()
    mops.logger.log.info('log folder:%s' % mops.logger.get_log_folder())

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action="store_true", help="use test data (don't access the redis DB)")
    parser.add_argument('-v', '--verbose', action="store_true", help='print verbose status messages')
    args = parser.parse_args()

    if args.verbose:
        print('log folder : %s' % mops.logger.get_log_folder())
        mops.logger.set_file_log_level(logging.DEBUG)

    app = mops.app.App(args.test, args.verbose)
    app.exec()

if __name__ == '__main__':
    main()