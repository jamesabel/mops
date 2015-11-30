
import argparse

import mops.app
import mops.gui
import mops.config


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--redis', nargs=2, help="provide and set redis endpoint and password")
    parser.add_argument('-t', '--test', action="store_true", help="use test data (don't access the redis DB)")
    parser.add_argument('-v', '--verbose', action="store_true", help='print verbose status messages')
    args = parser.parse_args()

    config = mops.config.MopsConfig()
    if args.verbose:
        print('config file path: %s' % config.get_config_file_path())

    if args.redis and not args.nodb:
        config.set_redis_login(args.redis[0], args.redis[1])

    mops.app.main(args.test, args.verbose)

if __name__ == '__main__':
    main()