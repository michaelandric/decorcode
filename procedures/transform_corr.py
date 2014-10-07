#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def fishertransform(inputcor, out):
    f = open("stdout_files/stdout_from_fishertransform.txt", "w")
    cmdargs = split("3dcalc -a %(inputcor)s -expr 'atanh(a)' -prefix %(out)s" % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


def converttoNIFTI(brain):
    f = open('stdout_files/stdout_from_converttoNIFTI', 'w')
    cmdargs = split('3dAFNItoNIFTI %(brain)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()



subj_list = ['JNWL']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for m in ('AV', 'A', 'V', 'lowlev'):
            input = '%(m)s_%(ss)s_tcorr_out_spearman_mean+orig' % locals()
            out = '%(m)s_%(ss)s_tcorr_out_spearman_mean_Z' % locals()
            fishertransform(input, out)
            converttoNIFTI(out+'+orig.')


