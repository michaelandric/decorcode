#!/usr/bin/python

import os
from shlex import split
from subprocess import call
from subprocess import STDOUT
from string import ascii_lowercase


def threshCor(epi, pref, thresh):
    f = open('stdout_files/stdout_from_3dcalc.txt', 'w')
    cmdargs = split("3dcalc -a %(epi)s -expr 'ispositive(a-%(thresh)s)' -prefix  %(pref)s" % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def converttoNIFTI(ss, brain):
    f = open('stdout_files/stdout_from_converttoNIFTI', 'w')
    cmdargs = split('3dAFNItoNIFTI %(brain)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def applywarpFLIRT(ss, input, extrt1, out, premat, interp):
    f = open('stdout_files/stdout_from_applywarpFLIRT.txt', 'w')
    if interp == 'nn':
        cmdargs = split('applywarp -i %(input)s -r %(extrt1)s --interp=nn -o %(out)s --premat=%(premat)s' % locals())
    else:
        cmdargs = split('applywarp -i %(input)s -r %(extrt1)s -o %(out)s --premat=%(premat)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def applywarpFNIRT(ss, input, out, coeff, interp):
    f = open('stdout_files/stdout_from_applywarp.txt', 'w')
    decor = os.environ['decor']
    if interp == 'nn':
        cmdargs = split('applywarp -i %(input)s -r %(decor)s/groupstuff/MNI152_T1_2mm.nii.gz --interp=nn -o %(out)s -w %(coeff)s' % locals())
    else:
        cmdargs = split('applywarp -i %(input)s -r %(decor)s/groupstuff/MNI152_T1_2mm.nii.gz -o %(out)s -w %(coeff)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def calcUnionMask(pref, ss_list, interp, thresh):
    epis = []
    letters = []
    for i, ss in enumerate(ss_list):
        epis.append("-%s /mnt/lnif-storage/urihas/MAdecorproj/%s/6mmblur_results/highres_fnirted_%s_MNI2mm_%s_%s_6mmblur_THRESH%s.nii.gz" % (ascii_lowercase[i], ss, interp, ss, m, thresh))
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



if __name__ == "__main__":

    '''
    Modifying arguments
    '''
    subj_list = ['SSGO', 'LSRS', 'SEKI', 'JNWL']
    interp = 'nn'   # otherwise default interpolation in applywarp is trilinear
    thresh = '.09'

    '''
    Now main executes
    '''
    for ss in subj_list:
        basedir = os.environ['decor']+'/%s' % (ss)
        os.chdir(basedir+'/6mmblur_results')
        for m in ['AV', 'A', 'V', 'lowlev']:
            epi = '%s_%s_6mmblur_tcorr_out_spearman_mean' % (m, ss)
            epiIN = '%s+orig' % (epi)
            pref = '%s_6mmblur_THRESH%s' % (epi, thresh)
            threshCor(epiIN, pref, thresh)
            converttoNIFTI(ss, pref+'+orig')

            extrt1 = '%s/%s.mprage2.gert_reco.anat/T1_biascorr_brain.nii.gz' % (basedir, ss)
            premat = '%s/epi2anat_%s_sess1_meanepi_mprage2.mat' % (basedir, ss)
            input = '%s.nii.gz' % (pref)
            outFL = 'highres_flirted_%s_%s_%s_6mmblur_THRESH%s' % (interp, ss, m, thresh)
            applywarpFLIRT(ss, input, extrt1, outFL, premat, interp)
            binoutFL = '%s_bin' % (outFL)
            makeBinaryFL(outFL+'.nii.gz', binoutFL)

            coeff = '%s/%s.mprage2.gert_reco.anat/T1_to_MNI_nonlin_coeff.nii.gz' % (basedir, ss)
            inputFN = '%s.nii.gz' % (binoutFL)
            outFN = 'highres_fnirted_%s_MNI2mm_%s_%s_6mmblur_THRESH%s' % (interp, ss, m, thresh)
            applywarpFNIRT(ss, inputFN, outFN, coeff, interp)
            binoutFN = '%s_bin' % (outFN)
            makeBinaryFN(outFN+'.nii.gz', binoutFN)

    os.chdir(os.environ['decor']+'/groupstuff')
    for m in ['AV', 'A', 'V', 'lowlev']:
        outpref = '3ss_highres_fnirted_%s_MNI2mm_%s_6mmblur_THRESH%s' % (interp, m, thresh)
        calcUnionMask(outpref, subj_list[1:], interp, thresh)

        outpref = '4ss_highres_fnirted_%s_MNI2mm_%s_6mmblur_THRESH%s' % (interp, m, thresh)
        calcUnionMask(outpref, subj_list, interp, thresh)


