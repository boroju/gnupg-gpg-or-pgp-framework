import argparse
import os

from amherst_common.amherst_logger import AmherstLogger

import common.loader as l
import common.utils as u


def parse_args():
    """
    Argument parsing function
    :return: Namespace containing all of the command line arguments
    """
    # Setup argument parsing
    parser = argparse.ArgumentParser(
        description='Python program for Lexis-Nexis Bridger ACaM EoM Encrypter by using Gnupg PGP.',
        add_help=True)
    parser.add_argument('-g', '--gpg_home', type=str, required=True, help='Home path where GPG is installed - e.g. "/home/uac-agent.prod.svc@corp.amherst.com"')
    parser.add_argument('-f', '--file_location', type=str, required=True, help='File locations (separated by commas - if multiple)')
    parser.add_argument('-t', '--target_location', type=str, required=True, help='Encrypted files destination - e.g. "/mnt/loadstore/ACAM/Compliance/Bridger/EOM/encrypted"')
    parser.add_argument('-r', '--public_key_recipient_email', type=str, required=True, help='Recipient Email - e.g. no-reply-bridger@LexisNexisRisk.com')
    parser.add_argument('-p', '--filename_contains_pattern', type=str, required=True, help='Check if files contain proper name pattern - e.g. *File-WC-Amherst*.txt')
    parser.add_argument('-l', '--log', type=str, required=False, help='Specify path to the log directory',
                        default='/etl/log/')
    parser.add_argument('-d', '--debug', action='store_true', required=False, help='Specify log level as DEBUG')
    parsed_args = parser.parse_args()

    return parsed_args


if __name__ == '__main__':
    # get arguments
    args = parse_args()

    py_file = os.path.splitext(os.path.split(__file__)[1])[0]
    log = AmherstLogger(log_directory=args.log, log_file_app=py_file, vendor_name='ACaM',
                        vendor_product='EoMEncrypter')

    # create a new object of GpgLoader class
    loader = l.GpgLoader(home=args.gpg_home, file_location=args.file_location,
                         recipients=args.public_key_recipient_email, target_location=args.target_location)

    if loader.send_encrypter_request(pk_recipient_email=loader.recipients,
                                     filename_pattern=args.filename_contains_pattern):
        log.info('All files have been successfully encrypted!')
        log.info('Process finished')
    else:
        log.error('An error has occurred while encrypting files.')
        day_today = str(u.get_datetime_now_str())[0:8]
        raise RuntimeError('Check errors for load date -> ' + day_today)
