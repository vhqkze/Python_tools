#!/usr/bin/env python3
import re
import os
import sys

base_dir = os.getcwd()


# print(base_dir)


def getfiles(dirpath):
    # 返回目录下所有文件和目录的名称组成的list, 不包含路径
    files = os.listdir(dirpath)
    # files = []
    # for item in os.listdir(dirpath):
    #     if os.path.isfile(item):
    #         files.append(item)
    return files


def rename(oldnames):
    havefile = False
    for filename in oldnames:
        if re.match(pattern, filename):
            havefile = True
            newname = re.sub(pattern, new, filename)
            print(filename, '  TO  ', newname)
    if havefile:
        exe = input('continue [y/n]?')
        if exe == 'y':
            for filename in oldnames:
                if re.match(pattern, filename):
                    newname = re.sub(pattern, new, filename)
                    # print(filename, '  TO  ', newname)
                    try:
                        os.rename(filename, newname)
                    except Exception:
                        print('rename fail:', filename)
        else:
            print('rename cancel.')
    else:
        print('There is no files to rename.')
    return


def ren(namelist):
    havefile = False
    for oldname in namelist:
        newname = re.sub(pattern, new, oldname)
        if newname == oldname:
            pass
        else:
            print(oldname, ' \033[31mTO\033[0m ', newname)
            havefile = True or havefile
    if havefile:
        dorename = input('\033[36mrename [y/n]?\033[0m').lower()
        if dorename == 'y':
            for oldname in namelist:
                newname = re.sub(pattern, new, oldname)
                if newname == oldname:
                    pass
                else:
                    try:
                        os.rename(oldname, newname)
                    except Exception:
                        print('\033[33mrename fail:\033[0m', oldname)
        else:
            print('nothing changed, exit')
    else:
        print('There is no files to rename.')


if __name__ == "__main__":
    pattern = re.compile(sys.argv[1])
    new = sys.argv[2]
    filenames = getfiles(base_dir)
    # rename(filenames)
    ren(filenames)
