# -*- coding: utf-8 -*-
"""
updated on Fri May  6 11:27:14 2016

@author: andric
"""

import os
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT


class FslAnat(object):
    """
    This sets up and does fsl_anat
    """

    def __init__(self, t1pref):
        print('Initializing... \n')
        self.t1pref = t1pref
        print('Got it.')

    def afni_to_nifti(self):
        print('AFNItoNIFTI...')
        stdfname = 'stdout_from_afnitonifti_{}'.format(self.t1pref)
        stdf = open(os.path.join('stdout_files', stdfname), 'w')
        cmdargs = split('3dAFNItoNIFTI {}+orig.'.format(self.t1pref))
        call(cmdargs, stdout=stdf, stderr=STDOUT)
        stdf.close()
        print('DONE...')

    def fslanat(self):
        print('fslanat...')
        stdfname = 'stdout_from_fsl_anat_{}'.format(self.t1pref)
        stdf = open(os.path.join('stdout_files', stdfname), 'w')
        fslargs = split('fsl_anat -i {}.nii.gz'.format(self.t1pref))
        Popen(fslargs, stdout=stdf, stderr=STDOUT)
        stdf.close()
        print('DONE')


def main(subjectlist, anatlist):
    for subject in subjectlist:
        os.chdir(os.path.join(os.environ['decor'], subject))
        for mprage in anatlist:
            anat = '{}.{}.gert_reco'.format(subject, mprage)
            fsla = FslAnat(anat)
            fsla.afni_to_nifti()
            fsla.fslanat()


if __name__ == "__main__":
    SUBJECTLIST = ['LNSE']
    T1LIST = ['mprage1', 'mprage2', 'mprage_2ndsess']
    main(SUBJECTLIST, T1LIST)
