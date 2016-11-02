# -*- coding: utf-8 -*-
"""
Code overhaul on October 2016.

The idea is to do epi_reg for mean_epi to the T1 in
the .anat dir (from fsl_anat).
Then can apply the coeff already done to move this to MNI space

This has to run in Python 2.7 (AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def converttoNIFTI(log, convbrain):
    """Convert afni to nifti format."""
    log.info('Convert To NIFTI format.')
    cmdargs = split('3dAFNItoNIFTI %s' % convbrain)
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def epi_reg(log, epiimg, whlt1, xtrt1, outreg):
    """Register epi to T1 dim."""
    log.info('Do epi_reg.')
    cmdargs = split('epi_reg --epi=%s --t1=%s \
                    --t1brain=%s --out=%s' % (epiimg, whlt1, xtrt1, outreg))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def applywarpFNIRT(log, infile, outfnirt, coefftrans):
    """Apply the FNIRT warp."""
    log.info('applywarpFNIRT.')
    cmdargs = split('applywarp -i %s -r %s/MNI152_T1_2mm.nii.gz \
                    -o %s -w %s' %
                    (infile, os.path.join(os.environ['decor'], 'groupstuff'),
                     outfnirt, coefftrans))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def applywarpFLIRT(log, infile, xtrt1, outflirt, prematrx):
    """Apply the FLIRT warp."""
    log.info('applywarpFLIRT.')
    cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s' %
                    (infile, xtrt1, outflirt, prematrx))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def apply_transforms(log, subject, inflirt, outflirt,
                     infnirt, outfnirt, prematrx):
    """Apply FLIRT and FNIRT."""
    log.info('Doing applywarpFLIRT...')
    extrct1 = os.path.join(os.path.join(os.environ['decor'], subject),
                           '%s.mprage2.gert_reco.anat' % subject,
                           'T1_biascorr_brain.nii.gz')
    coeffcnt = os.path.join(os.path.join(os.environ['decor'], subject),
                            '%s.mprage2.gert_reco.anat' % subject,
                            'T1_to_MNI_nonlin_coeff.nii.gz')
    applywarpFLIRT(log, inflirt, extrct1, outflirt, prematrx)
    applywarpFNIRT(log, infnirt, outfnirt, coeffcnt)


def main():
    """Wrap funciton calls to main."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'epi_reg'))
    logfile.info('Started 10.epi_reg.py')

    subj_list = ['NNPT']
    for subject in subj_list:
        basedir = os.path.join(os.environ['decor'], subject)
        os.chdir(os.path.join(basedir, '6mmblur_results'))
        print os.getcwd()
        outpref = 'epi2anat_%s_sess1_6mmblur_meanepi_mprage2' % subject
        converttoNIFTI(logfile, '%s_sess1_6mmblur_meanepi+orig' % subject)
        epi_reg(logfile, '%s_sess1_6mmblur_meanepi.nii.gz' % subject,
                os.path.join(basedir, '%s.mprage2.gert_reco.anat' % subject,
                             'T1_biascorr.nii.gz'),
                os.path.join(basedir, '%s.mprage2.gert_reco.anat' % subject,
                             'T1_biascorr_brain.nii.gz'),
                outpref)

        for modal in ['AV', 'A', 'V', 'lowlev']:
            # below runs full time series segment
            out_flirt = 'highres_flirted_MNI2mm_%s_%s_6mmblur__Z' % \
                        (subject, modal)
            apply_transforms(logfile, subject,
                             '%s_%s_6mmblur_tcorr_out_spearman_mean_Z.nii.gz'
                             % (modal, subject),
                             out_flirt,
                             '%s.nii.gz' % out_flirt,
                             'highres_fnirted_MNI2mm_%s_%s_6mmblur_Z'
                             % (subject, modal),
                             '%s.mat' % outpref)
            # below runs shorter time series segments
            for seg in ['twothirds', 'abouthalf']:
                out_flirt = 'highres_flirted_MNI2mm_%s_%s_%s_6mmblur__Z' % \
                            (subject, modal, seg)
                apply_transforms(logfile, subject,
                                 '%s_%s_6mmblur_tcorr_out_spearman_%s_mean_Z.nii.gz'
                                 % (modal, subject, seg),
                                 out_flirt,
                                 '%s.nii.gz' % out_flirt,
                                 'highres_fnirted_MNI2mm_%s_%s_%s_6mmblur_Z'
                                 % (subject, modal, seg),
                                 '%s.mat' % outpref)

if __name__ == "__main__":
    main()
