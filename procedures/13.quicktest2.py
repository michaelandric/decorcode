#!/usr/bin/python

import os
from shlex import split
from subprocess import call
from subprocess import PIPE
from subprocess import STDOUT
from string import ascii_lowercase

def calcMask(pref, epiA, epiB, epiC, mask):
    f = open('stdout_files/stdout_from_3dcalc.txt', 'w')
    cmdargs = split("3dcalc -a %(epiA)s -b %(epiB)s -c %(epiC)s -d %(mask)s -expr 'step(a-max(b,c))*d' -prefix %(pref)s" % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def calcMask2(pref, ss_list):
    epis = []
    letters = []
    for i, ss in enumerate(ss_list):
        epis.append("-%s AV_greaterthanmaxAorV_%s+tlrc" % (ascii_lowercase[i], ss))
        letters.append(ascii_lowercase[i])

    datasets = ' '.join(epis)
    letterslist = '+'.join(letters)
    f = open('stdout_files/stdout_from_3dcalc2.txt', 'w')
    cmdargs = split("3dcalc "+datasets+" -expr '("+letterslist+")' -prefix %(pref)s" % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['SSGO', 'LSRS', 'SEKI', 'JNWL']

if __name__ == "__main__":
    os.chdir(os.environ['decor']+'/groupstuff')

    for ss in subj_list:
        epiA = 'highres_fnirted_MNI2mm_%(ss)s_AV_Z.nii.gz' % locals() 
        epiB = 'highres_fnirted_MNI2mm_%(ss)s_A_Z.nii.gz' % locals() 
        epiC = 'highres_fnirted_MNI2mm_%(ss)s_V_Z.nii.gz' % locals() 
        mask = '/mnt/lnif-storage/urihas/MAdecorproj/JNWL/JNWL.mprage1.gert_reco.anat/MNI152_T1_2mm_brain_mask_dil1.nii.gz'
        outpref = 'AV_greaterthanmaxAorV_%(ss)s' % locals()
        #calcMask(outpref, epiA, epiB, epiC, mask)

    outpref = '3ss_AV_greaterthanmaxAorV'
    calcMask2(outpref, subj_list[1:])

    outpref = '4ss_AV_greaterthanmaxAorV'
    calcMask2(outpref, subj_list)


