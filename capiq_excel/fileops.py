import os
import shutil
import time


def get_path_of_failed_folder_add_if_necessary(orig_folder):
    return _join_path_and_create_if_necessary(orig_folder, r'..\failed')

def get_path_of_additional_failed_folder_add_if_necessary(orig_folder):
    return _join_path_and_create_if_necessary(orig_folder, r'failed')

def _join_path_and_create_if_necessary(orig_folder, new_relative_path):
    out_path = os.path.join(orig_folder, new_relative_path)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    return out_path


def move_file_to_failed_folder(file, failed_folder, retries_remaining=100):
    if retries_remaining <= 0:
        print(f'ERROR SKIPPING {file}! Could not move to {failed_folder}')
        return

    try:
        shutil.copy(file, failed_folder)
    except (PermissionError, OSError):
        time.sleep(.1)
        move_file_to_failed_folder(file, failed_folder, retries_remaining=retries_remaining - 1)