import argparse
import os

from amherst_common.amherst_logger import AmherstLogger

import common.keys as k


def parse_args():
    """
    Argument parsing function
    :return: Namespace containing all of the command line arguments
    """
    # Setup argument parsing
    parser = argparse.ArgumentParser(
        description='Python program for importing GnuPGP Public Key (.asc) of Lexis-Nexis Bridger.',
        add_help=True)
    parser.add_argument('-g', '--gpg_home', type=str, required=True, help='Home path where GPG is installed - e.g. "/home/uac-agent.prod.svc@corp.amherst.com"')
    parser.add_argument('-r', '--public_key_recipient_email', type=str, required=True, help='Recipient Email - e.g. no-reply-bridger@LexisNexisRisk.com')
    parser.add_argument('-f', '--file_location', type=str, required=True, help='Lexis-Nexis Risk Key File Location - e.g. "/mnt/loadstore/Temp/GnuPGP/Keys/"')
    parser.add_argument('-n', '--file_name', type=str, required=True, help='Lexis-Nexis Risk Key File Name - e.g. "lexis_nexis_risk.asc"')
    parser.add_argument('-l', '--log', type=str, required=False, help='Specify path to the log directory',
                        default='/etl/log/')
    parser.add_argument('-d', '--debug', action='store_true', required=False, help='Specify log level as DEBUG')
    parsed_args = parser.parse_args()

    return parsed_args


if __name__ == '__main__':
    # get arguments
    args = parse_args()

    py_file = os.path.splitext(os.path.split(__file__)[1])[0]
    log = AmherstLogger(log_directory=args.log, log_file_app=py_file, vendor_name='LexisNexis',
                        vendor_product='ImportKey')

    # create a new object of GpgKeys class
    log.info('Creating GpgKeys object...')
    key = k.GpgKeys(home=args.gpg_home, recipients=args.public_key_recipient_email)

    # importing Lexis-Nexis Risk public key (with .asc file extension)
    log.info('Importing key...')
    key.import_keys(file_location=args.file_location, file_name=args.file_name)

    # Listing all existing GnuPGP keys
    log.info('Listing keys...')
    key.list_keys()

    log.info('Process completed!')
