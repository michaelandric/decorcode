#!/usr/bin/python

'''
This is necessary to make a mean in order to get better alignment to volume
'''

import os
from shlex import split
from subprocess import call
from subprocess import STDOUT

def make_mean(inpref):
    f = open('stdout_files/stdout_from_align_vol.txt', 'w')
    cmdargs = split('3dTstat -mean -prefix mean.%s %s+orig' % (inpref, inpref))
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['IAGO']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/localizers/%s' % ss)   # adjusted for localizer
        inpref = 'localizer.%s.TRIM' % ss
        make_mean(inpref)
