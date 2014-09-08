#!/usr/bin/python

'''
following somewhat http://afni.nimh.nih.gov/sscc/dglen/alignmentacross2sessions
also relying on the SAMPLE USAGE in 3dQwarp help file
I have already skull stripped the anatomicals using fsl_anat

Going to first align the two from the session 1 then align from the two different sessions:
1. 3dUnifize the skull stripped 
2. 3dQwarp with -allineate 

'''

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

def Qwarp_proc(ss, brain1, brain2, Qwarp_pref):
    f = open('stdout_files/stdout_from_align_%(brain1)s_%(brain2)s' % locals(), 'w')
    for bb in [brain1, brain2]:
        cmdargs = split('3dUnifize -prefix %(bb)s_unifized -input %(bb)s.gert_reco.anat/T1_biascorr.nii.gz' % locals())
        #call(cmdargs)

    cmdargs = split('3dQwarp -prefix %(Qwarp_pref)s -allineate -duplo -useweight -blur 0 3 \
                    -base %(brain1)s_unifized+orig. -source %(brain2)s_unfized+orig' % locals())
    call(cmdargs)


subj_list = ['LSRS']
t1_list = ['mprage1', 'mprage2']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        brain1 = '%(ss)s.' % locals()+t1_list[0]
        brain2 = '%(ss)s.' % locals()+t1_list[1]
        qpref = '%(ss)s_mprage_sess1_Q' % locals()
        Qwarp_proc(ss, brain1, brain2, qpref)


