import os
import shutil
import datetime


count_ = 0


def count_for_uniq():
    global count_
    count_ += 1
    return count_


def check_or_create_temp_folder(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def check_or_create_source_folder(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def get_source_name(source_path):
    for root, dirs, files in os.walk(source_path):
        try:
            return files[0]
        except IndexError:
            pass


def create_folder_and_move_files(name_dest_folder):
    with os.scandir("lib\\temp_folder") as files:

        date_fmt = datetime.datetime.now()

        final_folder = f"{name_dest_folder}__{date_fmt.date()}_{date_fmt.hour}_{date_fmt.minute}_{date_fmt.second}"
        os.mkdir(f'Результат\{final_folder}')

        subdir = [file.name for file in files]
        [shutil.move(f'lib\\temp_folder\{t}', f'Результат\{final_folder}\{t}') for t in subdir]

