#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def _fslanat(t1):
    f = open('stdout_files/stdout_from_fsl_anat_%(t1)s' % locals(), 'w')
    #convertargs = split('3dAFNItoNIFTI %(t1)s.gert_reco+orig.' % locals())
    #Popen(convertargs, stdout = f, stderr = STDOUT)
    fslargs = split('fsl_anat -i %(t1)s.gert_reco.nii.gz' % locals())    
    Popen(fslargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['LSRS']
t1_list = ['mprage1', 'mprage2', 'mprage_2ndsess']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for mprage in t1_list:
            t1 = '%(ss)s.%(mprage)s' % locals()
            _fslanat(t1)
