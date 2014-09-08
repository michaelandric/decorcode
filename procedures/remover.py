#!/usr/bin/python

import os
import shutil
from glob import glob
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def remov(file):
    for fil in glob(file+'*_al*'):
        os.remove(fil)



subj_list = ['LSRS']
stim_dict = {
    'LSRS': {'sess1': ['SC5', 'SC6', 'SC2', 'AV2.1', 'AV1.1', 'AV3.1'], 'sess2': ['SC1', 'SC3', 'SC4', 'AV1.2', 'AV3.2', 'AV2.2']}
    }


if __name__ == "__main__":
    for ss in stim_dict.keys():
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for cc in stim_dict[ss]['sess2']:
            f = '%(ss)s.%(cc)s.results/' % locals()
            remov(f)
