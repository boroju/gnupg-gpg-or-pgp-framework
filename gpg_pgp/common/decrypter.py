import os

import common.keys as k
import common.utils as u
import gnupg
from amherst_common.amherst_logger import AmherstLogger

py_file = os.path.splitext(os.path.split(__file__)[1])[0]
log = AmherstLogger(log_directory='/etl/log/', log_file_app=py_file, vendor_name='Internal',
                    vendor_product='GpgDecrypter')

# TODO: This class is not being used for the moment...


class GpgDecrypter(k.GpgKeys):

    def __init__(self, home, recipients, passphrase=None, k_type=None, length=None):
        super().__init__(home, recipients, passphrase, k_type, length)

    def decrypt_string_w_private_key(self, encrypted_data, secret):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'

        encrypted_string = str(encrypted_data)
        decrypted_data = gpg.decrypt(encrypted_string, passphrase=secret)

        log.info('ok: ' + str(decrypted_data.ok))
        log.info('status: ' + str(decrypted_data.status))
        log.info('stderr: ' + str(decrypted_data.stderr))
        log.info('valid: ' + str(decrypted_data.valid))
        log.info('decrypted string: ' + str(decrypted_data.data))

    def decrypt_file_w_public_key(self, file_path, encrypted_file_name, unencrypted_file_name=None):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'
        path = u.valid_path(file_path)

        if unencrypted_file_name is None:
            new_file_name = encrypted_file_name.replace('.pgp', '')
        else:
            new_file_name = unencrypted_file_name

        with open(path + encrypted_file_name, 'rb') as f:
            status = gpg.decrypt_file(f, always_trust=True, output=new_file_name)

        log.info('ok: ' + str(status.ok))
        log.info('status: ' + str(status.status))
        log.info('stderr: ' + str(status.stderr))
        log.info('valid: ' + str(status.valid))
        log.info('trust_text: ' + str(status.trust_text))
        log.info('trust_level: ' + str(status.trust_level))

    def decrypt_multiple_files_w_public_key(self, files_path_loc, new_path_target_loc=None):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'
        path = u.valid_path(files_path_loc)

        if new_path_target_loc:
            final_path = u.valid_path(new_path_target_loc)
        else:
            final_path = path

        for f in os.listdir(path):
            new_file_name = f.replace('.pgp', '')
            with open(path + f, 'rb') as efile:
                decrypted_data = gpg.decrypt_file(efile, always_trust=True, output=final_path+new_file_name)

            log.info('ok: ' + str(decrypted_data.ok))
            log.info('status: ' + str(decrypted_data.status))
            log.info('stderr: ' + str(decrypted_data.stderr))
            log.info('valid: ' + str(decrypted_data.valid))
            log.info('trust_text: ' + str(decrypted_data.trust_text))
            log.info('trust_level: ' + str(decrypted_data.trust_level))
