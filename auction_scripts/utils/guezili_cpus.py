#!/user/bin/env python
# -*- coding:utf-8 -*-

"""
Uage: set variable folder = 'your photo path'
 quality default value is 84,you can up to
"""
import os

from os import path, remove, rename
from imghdr import what
from subprocess import call
from multiprocessing import Pool
import time

# setting configuration
TEMP_FILE = 'temp.jpg'
TYPE = ('jpg',)
LIMIT_QUALITY = 84

folder = '/Users/py2018/antique_images/'
quality = 84


def get_image_paths(folder):
    return (os.path.join(folder, f)
            for f in os.listdir(folder)
            if 'jpg' in f)


def run(url):
    if what(url) in TYPE or quality >= LIMIT_QUALITY:
        url_out = path.join(folder, TEMP_FILE)
        call(['guetzli', '--quality', str(quality), url, url_out])
        size_source = path.getsize(url)

        try:
            size_out = path.getsize(url_out)

        except BaseException:
            size_out = size_source

        size_acurate = 100 * size_out / size_source

        if size_acurate < 100:
            try:
                remove(url)
            except BaseException:
                pass

            rename(url_out, url)
            print (size_acurate)


if __name__ == '__main__':
    start = time.time()
    images = get_image_paths(folder)
    pool = Pool()
    pool.map(run, images)
    pool.close()
    pool.join()
    print(time.time() - start)
