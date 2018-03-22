#!/user/bin/env python
# -*- coding:utf-8 -*-

# image_compression_with_guetzili.py
# https://medium.com/@ageitgey/quick-tip-speed-up-your-python-data-processing-scripts-with-process-pools-cf275350163a
"""
image compression with high quality for transmission
that  aims for excellent compression density at high visual quality
给用户提供更顺畅的体验，并且减少移动用户的加载时间和带宽消耗
"""
import click
from os import path, walk, remove, rename
from imghdr import what
from subprocess import call
import time

# define variables

TEMP_FILE = 'temp.jpg'
TYPE = ('jpeg',)
LIMIT_QUALITY = 84


@click.command()
@click.option(
    '--quality',
    default=100,
    help='Quality >= {quality}[default 100].'.format(
        quality=LIMIT_QUALITY)
            )
@click.argument('folder', type=click.Path(exists=True))
def run(quality, folder):
    for dirpath, dirnames, files in walk(folder):
        for name in files:
            url = path.join(dirpath, name)
            # check type
            if what(url) in TYPE or quality >= LIMIT_QUALITY:
                click.echo(url)
                url_out = path.join(folder, TEMP_FILE)
                try:
                    remove(url_out)
                except:
                    pass

                #  Execute guetzli
                #  guetzli [--quality Q] [--verbose] original.png output.jpg
                call(['guetzli', '--quality', str(quality), url, url_out])
                size_source = path.getsize(url)
                try:
                    size_out = path.getsize(url_out)
                except:
                    size_out = size_source

                size_acurate = 100 * size_out / size_source
                if size_acurate < 100:
                    try:
                        remove(url)
                    except:
                        pass

                    rename(url_out, url)
                    click.echo('Save ' + str(round(100 - size_acurate, 2)) + '%')

                else:
                    click.echo('It is not neccessary to optimize!')


if __name__ == '__main__':
    start = time.time()
    run()
    print (time.time()-start)




