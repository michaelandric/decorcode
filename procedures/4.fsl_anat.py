#!/usr/bin/python

import os
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT

class FSLANAT:

    def __init__(self, anat):
        print 'Initializing... \nRequires anat'
        self.t1pref = anat   # this is the T1 volume prefix
        print 'Got it.'

    def AFNItoNIFTI(self):
        print 'AFNItoNIFTI...'
        f = open('stdout_files/stdout_from_afnitonifti_%s' % self.t1pref, 'w')
        cmdargs = split('3dAFNItoNIFTI %s+orig.' % self.t1pref)
        call(cmdargs, stdout = f, stderr = STDOUT)
        f.close()
        print 'DONE...'

    def fslanat(self):
        print 'fslanat...'
        f = open('stdout_files/stdout_from_fsl_anat_%s' % self.t1pref, 'w')
        fslargs = split('fsl_anat -i %s.nii.gz' % self.t1pref)
        Popen(fslargs, stdout = f, stderr = STDOUT)
        f.close()
        print 'DONE'


subj_list = ['CRSA']
t1_list = ['mprage1']   # localizer only the one brain

if __name__ == "__main__":
    for ss in subj_list:
        print 'LOCALIZERS!'
        os.chdir(os.environ['decor']+'/localizers/%(ss)s' % locals())   # set for localizers
        for mprage in t1_list:
            anat = '%(ss)s.%(mprage)s.gert_reco' % locals()
            FA = FSLANAT()
            FA.AFNItoNIFTI()
            FA.fslanat()
