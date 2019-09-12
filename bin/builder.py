#!/usr/bin/env python3

import os
import pathlib
import sys

from bs4 import BeautifulSoup

colors = {
    '#ffffff': '--foreground',
    '#eeeeee': '--foreground',
    '#326ce5': '--background'
}

parent_markup = """
<svg
    aria-hidden="true"
    style="position: absolute; width: 0; height: 0; overflow: hidden;"
    version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">
    <defs>
    </defs>
</svg>
"""

def get_fnames():
    return [
        os.path.join(d, fname)
        for d, _, fnames in os.walk(sys.argv[1])
        for fname in fnames if '.svg' in fname]

def convert_svg(root):
    for tag in root.get('style', '').split(';'):
        try:
            k, v = tag.split(':', 1)
        except:
            continue
        root[k] = v

    del root['style']

    for k in ['fill', 'stroke']:
        v = root.attrs.get(k, 'none')
        if v == 'none':
            continue

        root[k] = 'var({}, {})'.format(colors.get(v, '--missing'), v)

    for child in root.children:
        if not child.name:
            continue
        convert_svg(child)

if __name__ == '__main__':
    parent = BeautifulSoup(parent_markup, "html.parser")

    for fname in get_fnames():
        doc = BeautifulSoup(open(fname, 'r').read(), 'html.parser')
        convert_svg(doc.svg.g)

        tag = parent.new_tag(
            "symbol",
            id=fname[2:].replace('/', '-')[:-4])

        tag['viewbox'] = doc.svg.get('viewbox')

        tag.append(doc.svg.g)
        parent.defs.append(tag)

    print(parent)
