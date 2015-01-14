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


#subj_list = ['JNWL']
subj_list = ['SEKI', 'LSRS', 'SSGO']
brain = 'mprage2'

if __name__ == "__main__":

    for ss in subj_list:
        basedir = os.environ['decor']+'/%s' % (ss)
        os.chdir(os.environ['decor']+'/%(ss)s/6mmblur_results' % locals())
        
        meanepi = '%(ss)s_sess1_6mmblur_meanepi+orig' % locals()
        #converttoNIFTI(ss, meanepi)

        epi = '%s_sess1_6mmblur_meanepi.nii.gz' % (ss)
        wholet1 = '%s/%s.%s.gert_reco.anat/T1_biascorr.nii.gz' % (basedir, ss, brain)
        extrt1 = '%s/%s.%s.gert_reco.anat/T1_biascorr_brain.nii.gz' % (basedir, ss, brain)
        out = 'epi2anat_%s_sess1_6mmblur_meanepi_%s' % (ss, brain)
        #epi_reg(ss, epi, wholet1, extrt1, out)
        premat = '%s.mat' % (out)   # this will be used below in applywarpFLIRT

        input = '%s.nii.gz' % (out)
        coeff = '%s/%s.%s.gert_reco.anat/T1_to_MNI_nonlin_coeff.nii.gz' % (basedir, ss, brain)
        out = 'highres_fnirted_MNI2mm_%s_sess1_6mmblur_meanepi_%s' % (ss, brain)
        #applywarpFNIRT(ss, input, out, coeff)

        '''
        This section is to transform from orig space to the registered biasscor brain
        Then to standard 1mm iso highres MNI brain
        '''
        
        for m in ('AV', 'A', 'V', 'lowlev'):
            for v in ['twothirds', 'abouthalf']:
                input = '%s_%s_6mmblur_tcorr_out_spearman_%s_mean_Z.nii.gz' % (m, ss, v)
                outFL = 'highres_flirted_MNI2mm_%s_%s_%s_6mmblur__Z' % (ss, m, v)
                applywarpFLIRT(ss, input, extrt1, outFL, premat)

                input = '%s.nii.gz' % (outFL)
                outFN = 'highres_fnirted_MNI2mm_%s_%s_%s_6mmblur_Z' % (ss, m, v)
                applywarpFNIRT(ss, input, outFN, coeff)




