#!/usr/bin/python

import os
from shlex import split
from subprocess import call
from subprocess import PIPE
from subprocess import STDOUT


def ttest(out, ss_list, m):
    '''
    in the above arguments, "m" is for modality, e.g., "AV", "A", or "V"
    '''
    for ss in ss_list:
        datasets = ' '.join(['highres_fnirted_MNI2mm_%(ss)s_%(m)s_Z.nii.gz' % locals() for ss in ss_list])

    f = open('stdout_files/stdout_from_3dttest.txt', 'w')
    cmdargs = split('3dttest -prefix %(out)s -base1 0 -set2 ' % locals() +datasets)
    call(cmdargs, stdout = f, stderr = STDOUT)

def meanRes(pref, epis):
    f = open('stdout_files/stdout_from_3dmean.txt', 'w')
    cmdargs = split('3dMean -prefix %(pref)s %(epis)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)


subj_list = ['SSGO', 'LSRS', 'SEKI', 'JNWL']

if __name__ == "__main__":
    os.chdir(os.environ['decor']+'/groupstuff')

    #for m in ['AV', 'A', 'V', 'lowlev']:
    for m in ['AV']:
        #out = '4ss_ttestout_%(m)s' % locals()
        #ttest(out, subj_list, m)
        epis = ' '.join(['highres_fnirted_MNI2mm_%(ss)s_%(m)s_Z.nii.gz' % locals() for ss in subj_list])
        pref = '4ss_mean_%(m)s' % locals()
        meanRes(pref, epis)
        #out = '3ss_ttestout_%(m)s' % locals()
        #ttest(out, subj_list[1:], m)
        epis = ' '.join(['highres_fnirted_MNI2mm_%(ss)s_%(m)s_Z.nii.gz' % locals() for ss in subj_list[1:]])
        pref = '3ss_mean_%(m)s' % locals()
        meanRes(pref, epis)



