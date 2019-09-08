#!/usr/bin/env python3
"""
Usage:
    test.py [-i] [-f|-d] <pattern> <repl>

Arguments:
    pattern             pattern
    repl                replace

Options:
    -h, --help          Show this
    -v, --version       Show version
    -d                  only rename directory
    -f                  only rename file
    -i                  ignore case

"""
import os
import re

from docopt import docopt

base_dir = os.getcwd()


def getfiles(dirpath, onlyfile=False, onlydir=False):
    # 返回目录下所有文件和目录的名称组成的list, 不包含路径
    files = os.listdir(dirpath)
    files.sort()
    items = []
    if onlyfile:
        for i in files:
            if os.path.isfile(i):
                items.append(i)
    elif onlydir:
        for i in files:
            if os.path.isdir(i):
                items.append(i)
    else:
        items = files
    return items


def ren(items, pattern, repl, flags):
    renamelist = dict()
    for oldname in items:
        newname = re.sub(pattern, repl, oldname, flags=flags)
        if newname != oldname:
            # print(oldname, ' \033[31mTO\033[0m ', newname)
            renamelist[oldname] = newname
    if not renamelist:
        print('There is no files to rename.')
        return
    keys = renamelist.keys()
    maxlength = 0
    for i in keys:
        maxlength = max(maxlength, len(i))
    for k, v in renamelist.items():
        print('{0:<{maxlength}} \033[31mTO\033[0m {1}'.format(k, v, maxlength=maxlength))
    action = input('\033[36mRename [y/n]?\033[0m').lower()
    if action == 'y':
        for oldname, newname in renamelist.items():
            try:
                os.rename(oldname, newname)
            except:
                print('Rename fail:', oldname)
    else:
        print('Nothing changed, exit')
        return


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    items = getfiles(base_dir, args['-f'], args['-d'])
    if args['-i']:
        flags = re.I
    else:
        flags = 0
    ren(items, args['<pattern>'], args['<repl>'], flags)
