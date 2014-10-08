#!/usr/bin/python

import os
import shutil
from glob import glob



def cmdCP(brain, location):
    """
    simple copy function
    """
    print "subject: "+ss
    print os.getcwd()

    for filename in glob("masking/xyz_coords_graymattermask_*"):
        shutil.copy2(filename, os.environ["state"]+"/TSfiles")
    

subj_list = ['SSGO', 'SEKI', 'JNWL']

if __name__ == "__main__":

    for ss in subj_list: 
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for m in ('AV', 'A', 'V', 'lowlev'):
            brain = 'highres_fnirted_MNI2mm_%(ss)s_%(m)s_Z.nii.gz' % locals()
            '''
            Not actually using the above function this time
            '''
            shutil.copy2(brain, os.environ['decor']+'/groupstuff/')


