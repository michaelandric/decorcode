#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


'''
DO AVGEPIS (BELOW FUNCTION) FIRST AND SEPARATE. 
OTHERWISE FUCKS UP EVERYTHING ELSE--WILL TRY TO RUN REST WITHOUT THE AVG BEING DONE
NEED TO PUT A 'WAIT' FUNCTION IN THE SCRIPT BUT NOT SURE HOW YET
''' 

def avgepis(ss, sess, epi_list):
    f = open('stdout_files/stdout_from_alignepis.txt', 'w')
    cmdargs = split('3dMean -prefix %(ss)s_%(sess)s_avgepi %(epi_list)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def mean_sess(ss, sess):
    f = open('stdout_files/stdout_from_meanses.txt', 'w')
    cmdargs = split('3dTstat -prefix %(ss)s_%(sess)s_meanepi -mean %(ss)s_%(sess)s_avgepi+orig' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    #cmdargs3 = split('rm -rf %(ss)s_%(sess)s_avgepi+orig*' % locals())
    #call(cmdargs3, stdout = f, stderr = STDOUT)
    f.close()

def align_epis(ss):
    f = open('stdout_files/stdout_from_epi_align2.txt', 'w')
    cmdargs = split('align_epi_anat.py -dset1 %(ss)s_sess1_meanepi+orig -dset2 %(ss)s_sess2_meanepi+orig -dset2to1 -epi_base 0' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def allineate(ss, cc):
    f = open('stdout_files/stdout_from_allineate_epis.txt', 'w')
    cmdargs = split('3dAllineate -cubic -base %(ss)s_sess1_meanepi+orig -1Dmatrix_apply %(ss)s_sess2_meanepi_al_mat.aff12.1D \
                    -prefix errts.%(ss)s.%(cc)s_REML_al -input %(ss)s.%(cc)s.results/errts.%(ss)s.%(cc)s_REML+orig -master SOURCE \
                    -weight_frac 1.0 -maxrot 6 -maxshf 10 -VERB -warp aff -source_automask+4 -twopass' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['NNPT']
stim_dict = {
    #'LSRS': {'sess1': ['SC5', 'SC6', 'SC2', 'AV2.1', 'AV1.1', 'AV3.1'], 'sess2': ['SC1', 'SC3', 'SC4', 'AV1.2', 'AV3.2', 'AV2.2']}
    'NNPT': {'sess1': ['SC1', 'SC2', 'SC3', 'AV1.1', 'AV2.1', 'AV3.1'], 'sess2': ['SC4', 'SC5', 'SC6', 'AV1.2', 'AV2.2', 'AV3.2']}
    }


if __name__ == "__main__":
    '''
    for ss in stim_dict.keys():
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for sess in stim_dict[ss]:
            ll = ' '.join(map(str, ['%(ss)s.' % locals() + cc + '.results/pb03.%(ss)s.' % locals() + cc + '.r01.volreg+orig' for cc in stim_dict[ss][sess]]))
            #avgepis(ss, sess, ll)
            #mean_sess(ss, sess)

        #align_epis(ss)

        for sess in stim_dict[ss]:
            for cc in stim_dict[ss][sess]:
                #allineate(ss, cc)

    Below is for Rest data'''
    cc = 'Rest'
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        allineate(ss, cc)

