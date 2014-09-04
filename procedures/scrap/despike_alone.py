#!/usr/bin/python


'''
THIS WAS A TEST SCRIPT NOT USED
INSTEAD USING AFPROC.PY TO GENERATE STEPS IN THE WORKFLOW
'''


import os
import shutil
from shlex import split
from glob import glob
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE

def despike(ss, runID):
    f = open('stdout_files/stdout_from_despike_%(runID)s.txt' % locals(), 'w')
    cmdargs = split('3dDespike -nomask -prefix %(runID)s.%(ss)s.TRIM.despike %(runID)s.%(ss)s.TRIM+orig' % locals())
    Popen(cmdargs, stdout = f, stderr = STDOUT)
    f.close()



subj_list = ['LSRS']
SC_IDs = ['SC%(i)d' % locals() for i in xrange(1, 7)]
AV_IDs = ['AV1.1', 'AV1.2', 'AV2.1', 'AV2.2', 'AV3.1', 'AV3.2']
runIDs = SC_IDs + AV_IDs
#runIDs = ['Rest']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for rr in runIDs:
            despike(ss, rr)
