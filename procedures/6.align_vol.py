# -*- coding: utf-8 -*-
"""
recoded on Fri May  6 15:49:50 2016.

Revamped logging June 9 2016
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def align_epis(log, subj, anatname):
    """Align anatomy to the epi.

    Arg:
        subj: Subject identifier
        anatname: Name of anatomy session (e.g., mprage1)
    """
    log.info('Do align_epis')
    anatfile = os.path.join(os.environ['decor'], subj,
                            '{}.{}.gert_reco.anat'.format(subj, anatname),
                            'T1_biascorr_brain.nii.gz')
    cmdargs = split('align_epi_anat.py -anat {} -anat_has_skull no \
                    -epi {}_sess1_6mmblur_meanepi+orig -epi_base 0 \
                    -suffix _{} -anat2epi -big_move'.format(
                        anatfile, subj, anatname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Main call align_epis."""
    subjectlist = ['RSDE', 'VREA']
    t1list = ['mprage1']
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'align_vol'))
    logfile.info('Started 6.align_vol.py')

    for subject in subjectlist:
        for anat in t1list:
            os.chdir(os.path.join(os.environ['decor'],
                                  subject, '6mmblur_results'))
            align_epis(logfile, subject, anat)

if __name__ == "__main__":
    main()
