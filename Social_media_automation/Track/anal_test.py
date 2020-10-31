import multiprocessing
from multiprocessing import Pool
import os
import sys


def run_file(filename):
    os.system('{} {}'.format(sys.executable, filename))


filenames = ['following.py', 'followers.py']


if __name__ == '__main__':
    with Pool(2) as p:
        p.map(run_file, filenames)
