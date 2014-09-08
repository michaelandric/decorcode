#!/usr/bin/python

import os
import shutil
from shlex import split
from glob import glob
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE


def avg_anats(ss, a1, a2):
    f = open('stdout_files/stdout_from_3dmerge_%(ss)s.txt' % locals(), 'w')
    cmdargs = split('3dmerge -gmean -prefix mprage_avg_%(ss)s %(a1)s %(a2)s' % locals())
    Popen(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['LSRS']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        a1 = '%(ss)s.mprage1.gert_reco+orig' % locals()
        a2 = '%(ss)s.mprage2.gert_reco+orig' % locals()
        avg_anats(ss, a1, a2)


