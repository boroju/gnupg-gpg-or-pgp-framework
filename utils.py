import os
from datetime import datetime, timezone
from pathlib import Path

import pytz


def get_datetime_now_str():
    utc_dt = datetime.now(timezone.utc)  # UTC time
    dt = utc_dt.astimezone(tz=pytz.timezone('US/Central'))  # local time
    str_datetime = str(dt.strftime('%Y%m%d%H%M%S'))
    return str_datetime


def create_unencrypted_text_file(file_path, file_name):
    path = valid_path(file_path)

    if not str(file_name).endswith('.txt'):
        txt_file = file_name + '.txt'
    else:
        txt_file = file_name

    new_file = path + txt_file
    open(new_file, 'w').write('Just a Txt File .')

    print('New file has been created:' + new_file)


def check_if_dir_exists(path):
    return os.path.isdir(path)


def check_if_file_exists(file_path):
    return os.path.isfile(file_path)


def split_string(string_var, splitted_by):
    splitted_str = string_var.split(splitted_by)
    return splitted_str


def filename_contains_pattern(filename, pattern):
    file_name = str(filename)

    # TODO: splitting pattern separated by dot (.) - E.g. *File-Amherst*.txt
    # TODO: splitted[0] = File-Amherst and splitted[1] = .txt
    splitted = split_string(str(pattern).replace('*', ''), '.')
    name_pattern = splitted[0]
    ext_pattern = '.' + splitted[1]

    if name_pattern in file_name and ext_pattern in file_name:
        return True
    else:
        return False


def valid_path(file_path):
    if not str(file_path).startswith('/'):
        temp_path = '/' + file_path
    else:
        temp_path = file_path

    if not str(temp_path).endswith('/'):
        path = temp_path + '/'
    else:
        path = temp_path

    # Instantiate the Path class
    p = Path(path)

    # Check if path refers to directory or not
    if p.is_dir():
        return path
    else:
        return None
