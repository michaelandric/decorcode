#!/usr/bin/python

import os

subjects = ["NNPT", "SSGO"]


def mk(ss):
    newdir = '/mnt/lnif-storage/urihas/MAdecorproj/%(ss)s/' % locals()
    if not os.path.exists(newdir):
        os.makedirs(newdir)


if __name__ == "__main__":
    for ss in subjects:
        mk(ss)
