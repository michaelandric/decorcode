# -*- coding: utf-8 -*-
"""
recoded on Fri May  6 15:49:50 2016

@author: andric
"""

import os
from shlex import split
from subprocess import call
from subprocess import STDOUT


def align_epis(subj, anatname):
    """align anatomy to the epi
    Arg:
        subj: Subject identifier
        anatname: Name of anatomy session (e.g., mprage1)
    """
    anatfile = os.path.join(os.environ['decor'], subj,
                            '{}.{}.gert_reco.anat'.format(subj, anatname),
                            'T1_biascorr_brain.nii.gz')
    stdf = open('stdout_files/stdout_from_align_vol.txt', 'w')
    cmdargs = split('align_epi_anat.py -anat {} -anat_has_skull no \
                    -epi {}_sess1_6mmblur_meanepi+orig -epi_base 0 \
                    -suffix _{} -anat2epi -big_move'.format(
                        anatfile, subj, anatname))
    call(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()


def main():
    """Main run to call align_epis"""

    subjectlist = ['LNSE']
    t1list = ['mprage1']

    for subject in subjectlist:
        for anat in t1list:
            os.chdir(os.path.join(os.environ['decor'],
                                  subject, '6mmblur_results'))
            align_epis(subject, anat)


if __name__ == "__main__":
    main()
