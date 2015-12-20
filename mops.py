
import argparse

import mops.app
import mops.gui_systems
import mops.preferences


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--redis', nargs=2, help="provide and set redis endpoint and password")
    parser.add_argument('-t', '--test', action="store_true", help="use test data (don't access the redis DB)")
    parser.add_argument('-c', '--clear', action="store_true", help="clear preferences")
    parser.add_argument('-v', '--verbose', action="store_true", help='print verbose status messages')
    args = parser.parse_args()

    config = mops.preferences.MopsPreferences()
    if args.verbose:
        print('config file path: %s' % config.get_preferences_file_path())

    if args.clear:
        config.clear()

    if args.redis and not args.test:
        config.set_redis_login(args.redis[0], args.redis[1])

    app = mops.app.App(args.test, args.verbose)
    app.exec()

if __name__ == '__main__':
    main()