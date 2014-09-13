#!/usr/bin/python

import os
import shutil
from shlex import split
from glob import glob
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE


def splicer(ss, runID):
    f = open('stdout_files/stdout_from_Tcat_%(runID)s.txt' % locals(), 'w')
    cmdargs = split('3dTcat -prefix %(runID)s.%(ss)s.TRIM raw.%(ss)s.%(runID)s.gert_reco+orig.BRIK[5-324]' % locals())
    Popen(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def splicerRest(ss, runID):
    f = open('stdout_files/stdout_from_Tcat_%(runID)s.txt' % locals(), 'w')
    cmdargs = split('3dTcat -prefix %(runID)s.%(ss)s.TRIM raw.%(ss)s.%(runID)s.gert_reco+orig.BRIK[5-164]' % locals())
    Popen(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['NNPT', 'SSGO']
SC_IDs = ['SC%(i)d' % locals() for i in xrange(1, 7)]
AV_IDs = ['AV1.1', 'AV1.2', 'AV2.1', 'AV2.2', 'AV3.1', 'AV3.2']
runIDs = SC_IDs + AV_IDs

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        splicerRest(ss, 'Rest')
        for rr in runIDs:
            splicer(ss, rr)


