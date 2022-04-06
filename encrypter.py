import os

import common.keys as k
import common.utils as u
import gnupg
from amherst_common.amherst_logger import AmherstLogger

py_file = os.path.splitext(os.path.split(__file__)[1])[0]
log = AmherstLogger(log_directory='/etl/log/', log_file_app=py_file, vendor_name='Internal',
                    vendor_product='GpgEncrypter')


class GpgEncrypter(k.GpgKeys):

    def __init__(self, home, recipients, passphrase=None, k_type=None, length=None, file_pattern=None):
        super().__init__(home, recipients, passphrase, k_type, length)

        self._file_pattern = file_pattern

    # function to get value of _file_pattern
    def get_file_pattern(self):
        return self._file_pattern

    def encrypt_string(self, str_text):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'

        unencrypted_string = str_text
        encrypted_data = gpg.encrypt(data=unencrypted_string, recipients=self._recipients)
        encrypted_string = str(encrypted_data)
        log.info('ok: ' + str(encrypted_data.ok))
        log.info('status: ' + str(encrypted_data.status))
        log.info('stderr: ' + str(encrypted_data.stderr))
        log.info('unencrypted_string: ' + str(unencrypted_string))
        log.info('encrypted_string: ' + str(encrypted_string))

    # TODO: To encrypt multiple files from same path location by using "always_trust=True" (Public Key)
    def encrypt_multiple_files_w_public_key(self, files_path_loc, file_name_pattern, new_extension=None,
                                            new_path_target_loc=None):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'
        path = u.valid_path(files_path_loc)

        if new_path_target_loc:
            new_path = u.valid_path(new_path_target_loc)
        else:
            new_path = path

        # TODO: Not used for now // Only for ArchiveStore
        # get datetime now as string
        # datetime_ext = '.' + u.get_datetime_now_str()

        if new_extension:
            new_file_ext = new_extension + '.pgp'
        else:
            new_file_ext = '.pgp'

        if path:
            for f in os.listdir(path):
                if u.filename_contains_pattern(filename=f, pattern=file_name_pattern):
                    with open(path + f, 'rb') as efile:
                        status = gpg.encrypt_file(
                            efile, recipients=[self._recipients], always_trust=True,
                            output=new_path + f + new_file_ext
                        )
        else:
            log.error('Something goes wrong with file path location')
            raise RuntimeError(str(files_path_loc))

    # TODO: Below function is not used for the moment.
    def encrypt_and_sign_multiple_files_w_public_key(self, files_path_loc, file_name_pattern, new_extension=None,
                                                     new_path_target_loc=None):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'
        path = u.valid_path(files_path_loc)
        edata = None

        if new_path_target_loc:
            new_path = u.valid_path(new_path_target_loc)
        else:
            new_path = path

        # TODO: Not used for now // Only for ArchiveStore
        # get datetime now as string
        # datetime_ext = '.' + u.get_datetime_now_str()

        if new_extension:
            new_file_ext = new_extension + '.pgp'
        else:
            new_file_ext = '.pgp'

        if path:
            for f in os.listdir(path):
                if u.filename_contains_pattern(filename=f, pattern=file_name_pattern):
                    stream = open(path + f, 'rb')
                    # sign with private key
                    fp = gpg.list_keys(True).fingerprints[0]

                    edata = gpg.encrypt_file(
                        stream, recipients=[self._recipients], sign=fp,
                        always_trust=True, output=new_path + f + new_file_ext
                    )
        else:
            log.error('Something goes wrong with file path location')
            raise RuntimeError(str(files_path_loc))
