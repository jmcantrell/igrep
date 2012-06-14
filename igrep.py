#!/usr/bin/env python

"""Find image files by attributes like dimension and aspect ratio

Examples of usage:

    To find all images under the current directory with a 4:3 aspect ratio:
        igrep -r -a 4:3 .

    To find all images that are at least 1600 pixels wide:
        igrep -r -W >=1600 .

    Options can be combined:
        igrep -r -a 4:3 -W >=1600 .

"""

import os, operator
from imageutils.size import same_aspect_ratio
from scriptutils.arguments import Arguments
from PIL import Image


def is_size_match(size1, size2):  # {{{1
    for pair in zip(size1, size2):
        if None in pair:
            continue
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
        if pair[0] != pair[1]:
            return False
    return True


def get_images(paths, recursive=False):  # {{{1
    for f in get_files(paths, recursive):
        try:
            yield Image.open(f)
        except (IOError, ValueError):
            pass


def get_files(paths, recursive=False):  # {{{1
    for path in paths:
        if os.path.isdir(path):
            if not recursive:
                continue
            for root, dirs, files in os.walk(path):
                for f in files:
                    yield os.path.join(root, f)
        elif os.path.isfile(path):
            yield path


def image_info(image):  # {{{1
    return '\t'.join(str(s) for s in [
            image.filename,
            image.format,
            image.mode,
            '%sx%s' % image.size,
            operator.mul(*image.size)
            ])


def get_arguments():  # {{{1
    a = Arguments(description="Find image files by attributes.")
    a.add_argument('paths', metavar='PATH', nargs='+', help="path to search for images")
    a.add_argument('-r', '--recursive', action='store_true', help='recurse into directories')
    a.add_argument('-a', '--aspect', help='search by aspect ratio (ex: 4:3)')
    a.add_argument('-v', '--invert-match', action='store_true', help='invert the search logic')
    a.add_argument('-W', '--width', type=int, help='specify width')
    a.add_argument('-H', '--height', type=int, help='specify height')
    a.add_argument('-I', '--info', action='store_true', help='display image information')
    return a.parse_args()


def main():  # {{{1
    args = get_arguments()
    images = get_images(args.paths, args.recursive)
    comp = operator.not_ if args.invert_match else operator.truth
    if args.aspect:
        sa = [float(x) for x in args.aspect.split(':')]
        images = (i for i in images if comp(same_aspect_ratio(i.size, sa)))
    if args.width or args.height:
        s = (args.width, args.height)
        images = (i for i in images if comp(is_size_match(i.size, s)))
    if args.info:
        for i in images:
            print image_info(i)
    else:
        for i in images:
            print i.filename

# }}}1

if __name__ == '__main__':
    main()
