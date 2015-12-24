
import argparse
import logging

import mops.app
import mops.gui_systems
import mops.preferences
import mops.logger


def main():
    mops.logger.init()

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action="store_true", help="use test data (don't access the redis DB)")
    parser.add_argument('-v', '--verbose', action="store_true", help='print verbose status messages')
    args = parser.parse_args()

    if args.verbose:
        mops.logger.set_file_log_level(logging.DEBUG)

    app = mops.app.App(args.test, args.verbose)
    app.exec()

if __name__ == '__main__':
    main()