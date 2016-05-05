# -*- coding: utf-8 -*-
"""
Created on Thu May  5 18:26:53 2016

@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import STDOUT


def splicer(subj, run):
    stdf = open('stdout_files/stdout_from_Tcat_{}.txt'.format(run), 'w')
    cmdargs = split('3dTcat -prefix {}.{}.TRIM \
                    raw.{}.{}.gert_reco+orig.BRIK[5-324]'.format(
                        run, subj, subj, run))
    Popen(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()

def splicer_rest(subj, run):
    stdf = open('stdout_files/stdout_from_Tcat_{}.txt'.format(run), 'w')
    cmdargs = split('3dTcat -prefix {}.{}.TRIM \
                    raw.{}.{}.gert_reco+orig.BRIK[5-164]'.format(
                        run, subj, subj, run))
    Popen(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()

def splicer_localizer(subj, run):
    stdf = open('stdout_files/stdout_from_Tcat_{}.txt'.format(run), 'w')
    cmdargs = split('3dTcat -prefix {}.{}.TRIM \
                    raw.{}.{}.gert_reco+orig.BRIK[14-405]'.format(
                        run, subj, subj, run))
    Popen(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()


if __name__ == "__main__":

    SCRUNS = ['SC{}'.format(i) for i in range(1, 7)]
    AVRUNS = ['AV1.1', 'AV1.2', 'AV2.1', 'AV2.2', 'AV3.1', 'AV3.2']
    RUNIDS = SCRUNS + AVRUNS
    SUBJECTLIST = ['LNSE', 'PMBI']

    for ss in SUBJECTLIST:
        os.chdir(os.path.join(os.environ['decor'], ss))
        for rr in RUNIDS:
            splicer(ss, rr)
        splicer_rest(ss, 'Rest')
