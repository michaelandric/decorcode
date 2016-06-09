# -*- coding: utf-8 -*-
"""
Created on Thu May  5 18:26:53 2016.

Re-did logging with setlog.py June 8 2016
@author: andric
"""

import os
from shlex import split
from setlog import setup_log
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE


def splicer(log, subj, run):
    """Splice time series."""
    log.info('Doing splicer %s %s ...', subj, run)
    cmdargs = split('3dTcat -prefix {}.{}.TRIM \
                    raw.{}.{}.gert_reco+orig.BRIK[5-324]'.format(
                        run, subj, subj, run))
    log.info('cmd: \n%s', cmdargs)
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def splicer_rest(log, subj, run):
    """Splice rest time series."""
    log.info('Doing splicer_rest %s %s...', subj, run)
    cmdargs = split('3dTcat -prefix {}.{}.TRIM \
                    raw.{}.{}.gert_reco+orig.BRIK[5-164]'.format(
                        run, subj, subj, run))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def splicer_localizer(subj, run):
    """Splice localizer series."""
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
    SUBJECTLIST = ['GOPR', 'ANRC', 'DAHL']

    logfile = setup_log(os.path.join(os.environ['decor'], 'logs/splicer'))
    logfile.info('started splicer.py')
    for ss in SUBJECTLIST:
        subjectdir = os.path.join(os.environ['decor'], ss)
        os.chdir(subjectdir)
        for rr in RUNIDS:
            splicer(logfile, ss, rr)
        splicer_rest(logfile, ss, 'Rest')
