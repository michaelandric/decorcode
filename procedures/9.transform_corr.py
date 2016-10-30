# -*- coding: utf-8 -*-
"""
Code overhaul on June 10 2016.

This has to run in Python 2.7 (AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def fishertransform(log, inputcor, outpref):
    """Transform correlation value by Fisher's z."""
    log.info('Do fishertransform')
    cmdargs = split("3dcalc -a {} -expr 'atanh(a)' \
                    -prefix {}".format(inputcor, outpref))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def convert_to_nifti(log, brain):
    """Convert the AFNI format to NIFTI."""
    log.info('Doing convert_to_nifti')
    cmdargs = split('3dAFNItoNIFTI {}'.format(brain))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def setnames_call_funcs(log, subj, modal, tcorrsufx):
    """Inner function to call the methods and iterate naming."""
    infile = '{}_{}_{}_mean+orig'.format(modal, subj, tcorrsufx)
    outname = '{}_{}_{}_mean_Z'.format(modal, subj, tcorrsufx)
    fishertransform(log, infile, outname)
    convert_to_nifti(log, outname+'+orig.')


def main():
    """Wrap the methods to do both main call."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'transform_corr'))
    logfile.info('Started 9.transform_corr.py')

    subj_list = ['RSDE', 'VREA']
    for subject in subj_list:
        os.chdir(os.path.join(os.environ['decor'], subject, '6mmblur_results'))
        for m in ['AV', 'A', 'V', 'lowlev']:
            tcorr_suf = '6mmblur_tcorr_out_spearman'
            setnames_call_funcs(logfile, subject, m, tcorr_suf)
#            for funcseg in ['abouthalf', 'twothirds']:
#                tcorr_suf = '6mmblur_tcorr_out_spearman_{}'.format(funcseg)
#                setnames_call_funcs(logfile, subject, m, tcorr_suf)

if __name__ == "__main__":
    main()
