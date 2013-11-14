#! /usr/bin/env python

import os
import re

from mincss.processor import Processor


def process(urls):
    p = Processor()
    p.process(*urls)
    return p


def list_html_files(path, address):
    path = os.path.realpath(os.path.expanduser(path))
    address = address.rstrip('/')
    html_files = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.html'):
                file_path = os.path.join(root, f)
                html_files.append(re.sub('^%s' % path, address, file_path))
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('assets', 'src')]

    return html_files


def out(link):
    name = link.href.rsplit('/', 1)[1]
    with open('before_' + name, 'w') as f:
        f.write(link.before)
    with open('after_' + name, 'w') as f:
        f.write(link.after)


def join_files(files, output):
    output = os.path.realpath(os.path.expanduser(output))
    with open(output, 'w') as out_file:
        for file_name in files:
            file_name = os.path.realpath(os.path.expanduser(file_name))
            with open(file_name, 'r') as f:
                out_file.write(f.read())


if __name__ == '__main__':
    html_files = list_html_files('~/Sites/blog/', 'http://127.0.0.1:8000/')
    results = process(html_files)
    for link in results.links:
        out(link)

"""
join_files(['themes/pixrobot/assets/css/bootstrap.css', 'themes/base-jinja/assets/css/rst.css', 'themes/pixrobot/assets/css/code.css', 'themes/pixrobot/assets/css/theme.css'], 'themes/pixrobot/assets/css/all.css')
"""
