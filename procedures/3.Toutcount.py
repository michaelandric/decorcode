#!/usr/bin/python


import shlex
import os
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE


def Toutcount(ss, runID):
    call('3dToutcount -automask ./%(runID)s.%(ss)s.TRIM+orig > outcount.%(runID)s.%(ss)s.TRIM.1D' % locals (), shell = True)
    call('3dToutcount -automask ./%(runID)s.%(ss)s.TRIM+orig | 1dplot -stdin -jpg outcount.%(runID)s.%(ss)s.TRIM.jpg' % locals(), shell = True)


subj_list = ['LSRS']
SC_IDs = ['SC%(i)d' % locals() for i in xrange(1, 7)]
AV_IDs = ['AV1.1', 'AV1.2', 'AV2.1', 'AV2.2', 'AV3.1', 'AV3.2']
#runIDs = SC_IDs + AV_IDs
runIDs = ['Rest']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for rr in runIDs:
            Toutcount(ss, rr)


