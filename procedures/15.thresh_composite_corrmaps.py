#!/usr/bin/python

import os
from shlex import split
from subprocess import call
from subprocess import STDOUT
from string import ascii_lowercase


def threshCor(epi, pref):
    f = open('stdout_files/stdout_from_3dcalc.txt', 'w')
    cmdargs = split("3dcalc -a %(epi)s -expr 'ispositive(a-0.165)' -prefix  %(pref)s" % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def converttoNIFTI(ss, brain):
    f = open('stdout_files/stdout_from_converttoNIFTI', 'w')
    cmdargs = split('3dAFNItoNIFTI %(brain)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def applywarpFLIRT(ss, input, extrt1, out, premat):
    f = open('stdout_files/stdout_from_applywarpFLIRT.txt', 'w')
    cmdargs = split('applywarp -i %(input)s -r %(extrt1)s --interp=nn -o %(out)s --premat=%(premat)s' % locals())
    #cmdargs = split('applywarp -i %(input)s -r %(extrt1)s -o %(out)s --premat=%(premat)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def applywarpFNIRT(ss, input, out, coeff):
    f = open('stdout_files/stdout_from_applywarp.txt', 'w')
    decor = os.environ['decor']
    cmdargs = split('applywarp -i %(input)s -r %(decor)s/groupstuff/MNI152_T1_2mm.nii.gz --interp=nn -o %(out)s -w %(coeff)s' % locals())
    #cmdargs = split('applywarp -i %(input)s -r %(decor)s/groupstuff/MNI152_T1_2mm.nii.gz -o %(out)s -w %(coeff)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def calcUnionMask(pref, ss_list):
    epis = []
    letters = []
    for i, ss in enumerate(ss_list):
        epis.append("-%s /mnt/lnif-storage/urihas/MAdecorproj/%s/highres_fnirted_nn_MNI2mm_%s_%s_THRESH.165.nii.gz" % (ascii_lowercase[i], ss, ss, m))
        #epis.append("-%s /mnt/lnif-storage/urihas/MAdecorproj/%s/highres_fnirted_trilin_MNI2mm_%s_%s_THRESH.165_bin.nii.gz" % (ascii_lowercase[i], ss, ss, m))
        letters.append(ascii_lowercase[i])

    datasets = ' '.join(epis)
    letterslist = '+'.join(letters)
    f = open('stdout_files/stdout_from_3dcalcUnionMask.txt', 'w')
    cmdargs = split("3dcalc "+datasets+" -expr '("+letterslist+")' -prefix %(pref)s" % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def makeBinaryFL(epiIN, epiOUT):
    f = open('stdout_files/stdout_from_makeBinary.txt', 'w')
    cmdargs = split('fslmaths %s -thr 0.25 -bin %s -odt short' % (epiIN, epiOUT))
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def makeBinaryFN(epiIN, epiOUT):
    f = open('stdout_files/stdout_from_makeBinary.txt', 'w')
    cmdargs = split('fslmaths %s -thr 0.0 -bin %s -odt short' % (epiIN, epiOUT))
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['SSGO', 'LSRS', 'SEKI', 'JNWL']

if __name__ == "__main__":
    '''
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for m in ['AV', 'A', 'V', 'lowlev']:
            epi = '%s_%s_tcorr_out_spearman_mean' % (m, ss)
            epiIN = '%s+orig' % (epi)
            pref = '%s_THRESH.165' % (epi)
            threshCor(epiIN, pref)
            converttoNIFTI(ss, pref+'+orig')

            extrt1 = '%s.mprage2.gert_reco.anat/T1_biascorr_brain.nii.gz' % (ss)
            premat = 'epi2anat_%s_sess1_meanepi_mprage2.mat' % (ss)
            input = '%s.nii.gz' % (pref)
            #outFL = 'highres_flirted_trilin_%s_%s_THRESH.165' % (ss, m)
            outFL = 'highres_flirted_nn_%s_%s_THRESH.165' % (ss, m)
            applywarpFLIRT(ss, input, extrt1, outFL, premat)
            binoutFL = '%s_bin' % (outFL)
            makeBinaryFL(outFL+'.nii.gz', binoutFL)

            coeff = '%s.mprage2.gert_reco.anat/T1_to_MNI_nonlin_coeff.nii.gz' % (ss)
            inputFN = '%s.nii.gz' % (binoutFL)
            #outFN = 'highres_fnirted_trilin_MNI2mm_%s_%s_THRESH.165' % (ss, m)
            outFN = 'highres_fnirted_nn_MNI2mm_%s_%s_THRESH.165' % (ss, m)
            applywarpFNIRT(ss, inputFN, outFN, coeff)
            binoutFN = '%s_bin' % (outFN)
            makeBinaryFN(outFN+'.nii.gz', binoutFN)
    '''
    os.chdir(os.environ['decor']+'/groupstuff')
    for m in ['AV', 'A', 'V', 'lowlev']:
        #outpref = '3ss_highres_fnirted_trilin_MNI2mm_%s_THRESH.165' % (m)
        outpref = '3ss_highres_fnirted_nn_MNI2mm_%s_THRESH.165' % (m)
        calcUnionMask(outpref, subj_list[1:])

        #outpref = '4ss_highres_fnirted_trilin_MNI2mm_%s_THRESH.165' % (m)
        outpref = '4ss_highres_fnirted_nn_MNI2mm_%s_THRESH.165' % (m)
        calcUnionMask(outpref, subj_list)


