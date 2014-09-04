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


def volreg(ss, runID, ref_runID):
    f = open('stdout_files/stdout_from_volreg_withinsess_%(runID)s.txt' % locals(), 'w')
    cmdargs = split('3dvolreg -twopass -twodup -tshift 0 -dfile motion_%(runID)s_%(ss)s -base %(ref_runID)s.%(ss)s.TRIM.despike+orig\[0\] -prefix volreg_withinsess_%(runID)s_%(ss)s %(ref_runID)s.%(ss)s.TRIM.despike+orig' % locals())
    print cmdargs
    Popen(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['LSRS']
stim_dict = {
    'LSRS': {'SC5': ['SC5', 'SC6', 'SC2', 'AV2.1', 'AV1.1', 'AV3.1'], 'SC1': ['SC1', 'SC3', 'SC4', 'AV1.2', 'AV3.2', 'AV2.2']}
    }


if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for ref in stim_dict[ss]:
            for rr in stim_dict[ss][ref]:
                volreg(ss, rr, ref)
