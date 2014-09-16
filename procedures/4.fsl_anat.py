#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def _AFNItoNIFTI(t1):
    f = open('stdout_files/stdout_from_afnitonifti_%(t1)s' % locals(), 'w')
    cmdargs = split('3dAFNItoNIFTI %(t1)s.gert_reco+orig.' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def _fslanat(t1):
    f = open('stdout_files/stdout_from_fsl_anat_%(t1)s' % locals(), 'w')
    fslargs = split('fsl_anat -i %(t1)s.gert_reco.nii.gz' % locals())    
    Popen(fslargs, stdout = f, stderr = STDOUT)
    f.close()



subj_list = ['SSGO']
t1_list = ['mprage1', 'mprage2', 'mprage_2ndsess']

if __name__ == "__main__":

    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for mprage in t1_list:
            t1 = '%(ss)s.%(mprage)s' % locals()
            _AFNItoNIFTI(t1)
            _fslanat(t1)
