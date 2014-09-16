#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def converttoNIFTI(ss, brain):
    f = open('stdout_files/stdout_from_converttoNIFTI.txt', 'w')
    cmdargs = split('3dAFNItoNIFTI %(brain)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def epi_reg(ss, epi, wholet1, extrt1, out):
    f = open('stdout_files/stdout_from_epireg.txt', 'w')
    cmdargs = split('epi_reg --epi=%(epi)s --t1=%(wholet1)s --t1brain=%(extrt1)s --out=%(out)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['NNPT']
brain = 'mprage1'

if __name__ == "__main__":

    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())

        meanepi = '%(ss)s_sess1_meanepi+orig' % locals()
        converttoNIFTI(ss, meanepi)

        epi = '%(ss)s_sess1_meanepi.nii.gz' % locals()
        wholet1 = '%(ss)s.%(brain)s.gert_reco.anat/T1_biascorr.nii.gz' % locals()
        extrt1 = '%(ss)s.%(brain)s.gert_reco.anat/T1_biascorr_brain.nii.gz' % locals()
        out = 'epi2anat_%(ss)s_%(brain)s' % locals()
        epi_reg(ss, epi, wholet1, extrt1, out)

