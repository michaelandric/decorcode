#!/usr/bin/python

import os
from shlex import split
from subprocess import call
from subprocess import PIPE
from subprocess import STDOUT


def anova(outsuf, ss_list, cond_list, vers):
    dsets = []
    ameans = []
    for i,m in enumerate(cond_list):
        ameans.append("-amean %d %s_mean" % (i+1, m))
        for j,ss in enumerate(ss_list):
            basedir = os.environ['decor']+'/%s/6mmblur_results' % (ss)
            dsets.append("-dset %d %d '%s/highres_fnirted_MNI2mm_%s_%s_%s_6mmblur_Z.nii.gz'" % (i+1, j+1, basedir, ss, m, vers))
    
    ameans = ' '.join(ameans)
    dsets = ' '.join(dsets)
    f = open('stdout_files/stdout_from_3dANOVA2.txt', 'w')
    cmdargs = split('3dANOVA2 -type 3 -alevels 4 -blevels '+`len(ss_list)`+' \
                    '+dsets+' -fa all_fstat '+ameans+' \
                    -mask /mnt/lnif-storage/urihas/MAdecorproj/JNWL/JNWL.mprage1.gert_reco.anat/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                    -acontr 3 -1 -1 -1 AV_contrast \
                    -acontr -1 3 -1 -1 A_constrast \
                    -acontr -1 -1 3 -1 V_contrast \
                    -acontr -1 -1 -1 3 lowlev_contr \
                    -bucket quickanova_withmask_'+vers+'_6mmblur_'+outsuf)
    call(cmdargs, stdout = f, stderr = STDOUT)


subj_list = ['SSGO', 'LSRS', 'SEKI', 'JNWL']
modes = ['AV', 'A', 'V', 'lowlev']

if __name__ == "__main__":
    os.chdir(os.environ['decor']+'/groupstuff/')

    for v in ['twothirds', 'abouthalf']:
        outsuf = '4ss'
        anova(outsuf, subj_list, modes, v)

        outsuf = '3ss'
        anova(outsuf, subj_list[1:], modes, v)

    
