
import argparse
import os
import configparser

import mops.mops


def main():
    company = 'abel'
    application = 'iwantmyrdp'

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--advertise', help="advertise that this computer accepts RDP (usually execute on startup)")
    parser.add_argument('-c', '--connect', help="connect to a computer")
    parser.add_argument('-r', '--redis', nargs=2, help="set redis endpoint and password")
    parser.add_argument('-v', '--verbose', action="store_true", help='print verbose status messages')
    args = parser.parse_args()

    config_file_folder = os.path.join(os.getenv('APPDATA'), company, application)
    if not os.path.exists(config_file_folder):
        os.makedirs(config_file_folder)
    config_file_path = os.path.join(config_file_folder, 'config.ini')

    if args.verbose:
        print('config file path : %s' % config_file_path)

    did_something = False

    if args.redis:
        config = configparser.ConfigParser()
        config['redis'] = {'endpoint': args.redis[0], 'password': args.redis[1]}
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        did_something = True

    #rdp = iwantmyrdp.iwantmyrdp.IWantMyRDP()
    #print(rdp.get_rdp_systems())

    if not did_something:
        print('nothing to do - execute with --help for help')

    m = mops.mops.Mops()


if __name__ == '__main__':
    main()