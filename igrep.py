#!/usr/bin/env python

# DOCUMENTATION {{{
"""Find image files by attributes like dimension and aspect ratio

Examples of usage:

    To find all images under the current directory with a 4:3 aspect ratio:
        igrep -r -a 4:3 .

    To find all images that are at least 1600 pixels wide:
        igrep -r -W >=1600 .

    Options can be combined:
        igrep -r -a 4:3 -W >=1600 .

""" #}}}

import os, operator
from imageutils.size import same_aspect_ratio
from argparse import ArgumentParser
from PIL import Image

def is_size_match(size1, size2): #{{{1
    for pair in zip(size1, size2):
        if None in pair: continue
        if pair[1][0:2] == '<=':
            if pair[0] <= int(pair[1][2:]): continue
            return False
        elif pair[1][0:2] == '>=':
            if pair[0] >= int(pair[1][2:]): continue
            return False
        elif pair[1][0] == '<':
            if pair[0] < int(pair[1][1:]): continue
            return False
        elif pair[1][0] == '>':
            if pair[0] > int(pair[1][1:]): continue
            return False
        if pair[0] != pair[1]: return False
    return True

def get_images(paths, recursive=False): #{{{1
    for f in get_files(paths, recursive):
        try:
            yield Image.open(f)
        except (IOError, ValueError):
            pass

def get_files(paths, recursive=False): #{{{1
    for path in paths:
        if os.path.isdir(path):
            if not recursive: continue
            for root, dirs, files in os.walk(path):
                for f in files:
                    yield os.path.join(root, f)
        elif os.path.isfile(path):
            yield path

def image_info(image): #{{{1
    return '\t'.join(str(s) for s in [
            image.filename,
            image.format,
            image.mode,
            '%sx%s' % image.size,
            operator.mul(*image.size)
            ])

def get_options(): #{{{1
    opts = ArgumentParser(description="Find image files by attributes.")
    opts.add_argument('paths', metavar='PATH', nargs='+', help="path to search for images")
    opts.add_argument('-r', '--recursive', action='store_true', help='recurse into directories')
    opts.add_argument('-a', '--aspect', help='search by aspect ratio (ex: 4:3)')
    opts.add_argument('-v', '--invert-match', action='store_true', help='invert the search logic')
    opts.add_argument('-W', '--width', type=int, help='specify width')
    opts.add_argument('-H', '--height', type=int, help='specify height')
    opts.add_argument('-I', '--info', action='store_true', help='display image information')
    return opts.parse_args()

def main(): #{{{1
    opts = get_options()
    images = get_images(opts.paths, opts.recursive)
    comp = operator.not_ if opts.invert_match else operator.truth
    if opts.aspect:
        sa = [float(x) for x in opts.aspect.split(':')]
        images = (i for i in images if comp(same_aspect_ratio(i.size, sa)))
    if opts.width or opts.height:
        s = (opts.width, opts.height)
        images = (i for i in images if comp(is_size_match(i.size, s)))
    if opts.info:
        for i in images:
            print image_info(i)
    else:
        for i in images:
            print i.filename

#}}}

if __name__ == '__main__': main()
