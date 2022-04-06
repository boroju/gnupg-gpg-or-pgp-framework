
import os

import common.utils as u
import gnupg
from amherst_common.amherst_logger import AmherstLogger

py_file = os.path.splitext(os.path.split(__file__)[1])[0]
log = AmherstLogger(log_directory='/etl/log/', log_file_app=py_file, vendor_name='Internal',
                    vendor_product='GpgKeys')


class GpgKeys:

    def __init__(self, home, recipients=None, passphrase=None, k_type=None, length=None):
        self._home = home
        self._recipients = recipients
        self._passphrase = passphrase
        self._k_type = k_type
        self._length = length

    # function to get value of _home
    def get_home(self):
        return self._home

    home = property(get_home)

    # function to get value of _recipients
    def get_recipients(self):
        return self._recipients

    recipients = property(get_recipients)

    # function to get value of _passphrase
    def get_passphrase(self):
        return self._passphrase

    passphrase = property(get_passphrase)

    # function to get value of _k_type
    def get_k_type(self):
        return self._k_type

    k_type = property(get_k_type)

    # function to get value of _length
    def get_length(self):
        return self._length

    length = property(get_length)

    def gen_key(self):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'

        input_data = gpg.gen_key_input(
            name_email=self._recipients,
            passphrase=self._passphrase,
            key_k_type=self._k_type,
            key_length=self._length
        )

        key = gpg.gen_key(input_data)

        log.info('New Key:')
        log.info(str(key))

    def list_keys(self):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'

        public_keys = gpg.list_keys()
        private_keys = gpg.list_keys(True)
        log.info('Public keys:')
        log.info(str(public_keys))
        log.info('Private keys:')
        log.info(str(private_keys))

    def list_public_keys(self):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'

        public_keys = gpg.list_keys()
        log.info('Public keys:')
        log.info(str(public_keys))

    def export_keys(self, keys, file_path, file_name):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'
        path = u.valid_path(file_path)

        ascii_armored_public_keys = gpg.export_keys(keyids=keys)
        ascii_armored_private_keys = gpg.export_keys(keyids=keys, secret=True)

        if not file_name.endswith('.asc'):
            filename = file_name + '.asc'
        else:
            filename = file_name

        with open(path+filename, 'w') as f:
            f.write(ascii_armored_public_keys)
            f.write(ascii_armored_private_keys)

        log.info('Keys have been exported to: ' + path+filename + ' file.')

    def import_keys(self, file_location, file_name):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'
        path = u.valid_path(file_location)

        if not file_name.endswith('.asc'):
            filename = file_name + '.asc'
        else:
            filename = file_name

        log.info('Reading ' + str(path+filename) + ' file...')
        key_data = open(path+filename).read()
        import_result = gpg.import_keys(key_data)
        log.info('Imported results:')
        log.info(str(import_result.results))

    def delete_public_key(self, file_location, file_name):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'
        path = u.valid_path(file_location)

        if not file_name.endswith('.asc'):
            filename = file_name + '.asc'
        else:
            filename = file_name

        key_file = f'{path + filename}'
        log.info('Reading ' + key_file + ' file...')
        scan_key = gpg.scan_keys(key_file)

        first_key = scan_key[0]
        fingerprint_to_delete = first_key['fingerprint']

        log.info('Deleting Key with fingerprint: ' + fingerprint_to_delete + ' ...')
        result = gpg.delete_keys(fingerprints=fingerprint_to_delete)

        if str(result) == 'ok':
            log.info('Public key has been successfully deleted..')
            return True
        else:
            log.error('Something went wrong while deleting Public Key..')
            return False
