#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


"""
The idea is to do epi_reg for mean_epi to the T1 in the .anat dir (from fsl_anat). 
Then can apply the coeff already done to move this to MNI space
"""

def converttoNIFTI(ss, brain):
    f = open('stdout_files/stdout_from_converttoNIFTI', 'w')
    cmdargs = split('3dAFNItoNIFTI %(brain)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def epi_reg(ss, epi, wholet1, extrt1, out):
    f = open('stdout_files/stdout_from_epireg.txt', 'w')
    cmdargs = split('epi_reg --epi=%(epi)s --t1=%(wholet1)s --t1brain=%(extrt1)s --out=%(out)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def applywarpFNIRT(ss, input, out, coeff):
    f = open('stdout_files/stdout_from_applywarp.txt', 'w')
    decor = os.environ['decor']
    cmdargs = split('applywarp -i %(input)s -r %(decor)s/groupstuff/MNI152_T1_2mm.nii.gz -o %(out)s -w %(coeff)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def applywarpFLIRT(ss, input, extrt1, out, premat):
    f = open('stdout_files/stdout_from_applywarpFLIRT.txt', 'w')
    cmdargs = split('applywarp -i %(input)s -r %(extrt1)s -o %(out)s --premat=%(premat)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['SEKI', 'LSRS', 'SSGO']
brain = 'mprage2'

if __name__ == "__main__":

    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        meanepi = '%(ss)s_sess1_meanepi+orig' % locals()
        converttoNIFTI(ss, meanepi)

        epi = '%(ss)s_sess1_meanepi.nii.gz' % locals()
        wholet1 = '%(ss)s.%(brain)s.gert_reco.anat/T1_biascorr.nii.gz' % locals()
        extrt1 = '%(ss)s.%(brain)s.gert_reco.anat/T1_biascorr_brain.nii.gz' % locals()
        out = 'epi2anat_%(ss)s_sess1_meanepi_%(brain)s' % locals()
        epi_reg(ss, epi, wholet1, extrt1, out)
        premat = '%(out)s.mat' % locals()   # this will be used below in applywarpFLIRT

        input = '%(out)s.nii.gz' % locals()
        coeff = '%(ss)s.%(brain)s.gert_reco.anat/T1_to_MNI_nonlin_coeff.nii.gz' % locals()
        out = 'highres_fnirted_MNI2mm_%(ss)s_sess1_meanepi_%(brain)s' % locals()
        applywarpFNIRT(ss, input, out, coeff)

        '''
        This section is to transform from orig space to the registered biasscor brain
        Then to standard 1mm iso highres MNI brain
        '''
        for m in ('AV', 'A', 'V', 'lowlev'):
            input = '%(m)s_%(ss)s_tcorr_out_spearman_mean_Z.nii.gz' % locals()
            outFL = 'highres_flirted_MNI2mm_%(ss)s_%(m)s_Z' % locals()
            applywarpFLIRT(ss, input, extrt1, outFL, premat)

            input = '%(outFL)s.nii.gz' % locals()
            outFN = 'highres_fnirted_MNI2mm_%(ss)s_%(m)s_Z' % locals()
            applywarpFNIRT(ss, input, outFN, coeff)




