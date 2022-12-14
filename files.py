import glob
import os
from datetime import date
from os.path import expanduser


def get_file_path_by_date(arg_date: date):
    return get_file_path_by_yw(arg_date.year, arg_date.isocalendar().week)


def get_file_path_by_yw(year, week):
    return "{0}/{1}/w{2:02d}.hr".format(get_base_path(), year, week)

def get_base_path():
    return expanduser("~/.config/punch")


def parse_path(the_path):
    # Parse paths
    full_paths = [os.path.join(os.getcwd(), path) for path in the_path]
    files = set()
    for path in full_paths:
        if os.path.isfile(path):
            files.add(path)
        else:
            files |= set(glob.glob(path + '/*.hr'))
    return files;
