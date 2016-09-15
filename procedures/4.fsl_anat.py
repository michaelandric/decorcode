# -*- coding: utf-8 -*-
"""
updated on Fri May  6 11:27:14 2016.

again on June 8 2016
@author: andric
"""

import os
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT
from setlog import setup_log


class FslAnat(object):
    """This sets up and does fsl_anat."""

    def __init__(self, t1pref):
        """Initialize the FslAnat."""
        print('Initializing... \n')
        self.t1pref = t1pref
        print('Got it.')

    def afni_to_nifti(self, log):
        """Do afni_to_nifti."""
        log.info('Doing afni_to_nifti for %s', self.t1pref)
        print('AFNItoNIFTI...')
        stdfname = 'stdout_from_afnitonifti_{}'.format(self.t1pref)
        stdf = open(os.path.join('stdout_files', stdfname), 'w')
        cmdargs = split('3dAFNItoNIFTI {}+orig.'.format(self.t1pref))
        call(cmdargs, stdout=stdf, stderr=STDOUT)
        stdf.close()
        print('DONE...')

    def fslanat(self, log):
        """Do fsl_anat."""
        log.info('Doing fsl_anat for %s', self.t1pref)
        print('fslanat...')
        stdfname = 'stdout_from_fsl_anat_{}'.format(self.t1pref)
        stdf = open(os.path.join('stdout_files', stdfname), 'w')
        fslargs = split('fsl_anat -i {}.nii.gz'.format(self.t1pref))
        Popen(fslargs, stdout=stdf, stderr=STDOUT)
        stdf.close()
        print('DONE')


def main(subjectlist, anatlist):
    """Wrap methods in main call."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                        'fsl_anat'))
    logfile.info('started 4.fsl_anat.py')
    for subject in subjectlist:
        os.chdir(os.path.join(os.environ['decor'], subject))
        for mprage in anatlist:
            anat = '{}.{}.gert_reco'.format(subject, mprage)
            fsla = FslAnat(anat)
            fsla.afni_to_nifti(logfile)
            fsla.fslanat(logfile)


if __name__ == "__main__":
    SUBJECTLIST = ['RSDE', 'VREA']
    T1LIST = ['mprage1', 'mprage2', 'mprage_2ndsess']
    main(SUBJECTLIST, T1LIST)
