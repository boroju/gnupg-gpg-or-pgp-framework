import os

import common.decrypter as d
import common.encrypter as e
import common.utils as u
import gnupg
from amherst_common.amherst_logger import AmherstLogger

py_file = os.path.splitext(os.path.split(__file__)[1])[0]
log = AmherstLogger(log_directory='/etl/log/', log_file_app=py_file, vendor_name='Internal',
                    vendor_product='GpgLoader')


# TODO: Class for consolidating Encrypter and Decrypter functionalities.


class GpgLoader(e.GpgEncrypter, d.GpgDecrypter):

    def __init__(self, file_location, target_location, home, recipients, passphrase=None, k_type=None, length=None,
                 file_pattern=None):
        super().__init__(home, recipients, passphrase, k_type, length, file_pattern)

        self._file_location = file_location
        self._target_location = target_location

    # function to get value of _file_location
    def get_file_location(self):
        return self._file_location

    file_location = property(get_file_location)

    # function to get value of _target_location
    def get_target_location(self):
        return self._target_location

    target_location = property(get_target_location)

    def send_encrypter_request(self, pk_recipient_email, filename_pattern):
        gpg = gnupg.GPG(gnupghome=self._home)
        gpg.encoding = 'utf-8'
        encrypter = e.GpgEncrypter(home=self.home, recipients=pk_recipient_email)
        target_valid_path = u.valid_path(self.target_location)

        # check if target location path exists
        if u.check_if_dir_exists(target_valid_path):

            # TODO: For multiple file locations
            # splitting file location paths separated by commas (,)
            if ',' in str(self.file_location):
                paths = u.split_string(self.file_location, ',')

                for path in paths:
                    src_valid_path = u.valid_path(path)
                    if u.check_if_dir_exists(src_valid_path):
                        log.info('Encrypting files within ->' + str(src_valid_path))
                        encrypter.encrypt_multiple_files_w_public_key(files_path_loc=src_valid_path,
                                                                      file_name_pattern=filename_pattern,
                                                                      new_path_target_loc=target_valid_path)
                    else:
                        log.error('Source location does not exist ->' + str(src_valid_path))
                        return False
                return True

            # TODO: For individual file location
            else:
                src_valid_path = u.valid_path(self.file_location)
                if u.check_if_dir_exists(src_valid_path):
                    log.info('Encrypting files within ->' + str(src_valid_path))
                    encrypter.encrypt_multiple_files_w_public_key(files_path_loc=src_valid_path,
                                                                  file_name_pattern=filename_pattern,
                                                                  new_path_target_loc=target_valid_path)
                    return True
                else:
                    log.error('Source location does not exist ->' + str(src_valid_path))
                    return False
        else:
            log.error('Target location does not exist ->' + str(target_valid_path))
            return False
