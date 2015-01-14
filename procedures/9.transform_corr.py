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



subj_list = ['SEKI', 'LSRS', 'SSGO', 'JNWL']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s/6mmblur_results' % locals())
        for m in ['AV', 'A', 'V', 'lowlev']:
            for v in ['twothirds', 'abouthalf']:
                input = '%s_%s_6mmblur_tcorr_out_spearman_%s_mean+orig' % (m, ss, v)
                out = '%s_%s_6mmblur_tcorr_out_spearman_%s_mean_Z' % (m, ss, v)
                fishertransform(input, out)
                converttoNIFTI(out+'+orig.')


