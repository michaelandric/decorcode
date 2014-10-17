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
    cmdargs = split('3dMean -prefix %(ss)s_%(sess)s_6mmblur_avgepi %(epi_list)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def mean_sess(ss, sess):
    f = open('stdout_files/stdout_from_meanses.txt', 'w')
    cmdargs = split('3dTstat -prefix %(ss)s_%(sess)s_6mmblur_meanepi -mean %(ss)s_%(sess)s_6mmblur_avgepi+orig' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    #cmdargs3 = split('rm -rf %(ss)s_%(sess)s_avgepi+orig*' % locals())
    #call(cmdargs3, stdout = f, stderr = STDOUT)
    f.close()

def align_epis(ss):
    '''
    Creating template to align second session runs to first session.
    '''
    f = open('stdout_files/stdout_from_epi_align2.txt', 'w')
    cmdargs = split('align_epi_anat.py -dset1 %(ss)s_sess1_6mmblur_meanepi+orig -dset2 %(ss)s_sess2_6mmblur_meanepi+orig -dset2to1 -epi_base 0 -anat_has_skull no -master_dset1_dxyz BASE -giant_move -suffix _gm' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

    '''have to resample, giant_move uses min_dxyz, can't change it. It is not necessary however because the 3dAllineate will not
    redo the voxel sizes on its own below.
    3dresample -master NNPT_sess1_meanepi+orig. -inset NNPT_sess2_meanepi_gm2+orig. -prefix NNPT_sess2_meanepi_gm2_resamp'''

def allineate(ss, cc):
    '''
    Only need this for aligning second session runs to their first session counterparts. First session already good from 3dvolreg.
    '''
    f = open('stdout_files/stdout_from_allineate_epis.txt', 'w')
    basedir = os.environ['decor']+'/%s' % (ss)
    cmdargs = split('3dAllineate -cubic -base %(ss)s_sess1_6mmblur_meanepi+orig -1Dmatrix_apply %(ss)s_sess2_6mmblur_meanepi_gm_mat.aff12.1D \
                    -prefix errts.%(ss)s.%(cc)s.6mmblur_REML_gm -input %(basedir)s/%(ss)s.%(cc)s.6mmblur.results/errts.%(ss)s.%(cc)s.6mmblur_REML+orig -master SOURCE \
                    -weight_frac 1.0 -maxrot 6 -maxshf 10 -VERB -warp aff -source_automask+2 -twopass' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def copyn(ss, cc):
    '''
    This is to copy errts into the dir and have contiguous naming convention
    '''
    f = open('stdout_files/stdout_from_3dcopy_epis_sess1.txt', 'w')
    basedir = os.environ['decor']+'/%s' % (ss)
    cmdargs = split('3dcopy %(basedir)s/%(ss)s.%(cc)s.6mmblur.results/errts.%(ss)s.%(cc)s.6mmblur_REML+orig errts.%(ss)s.%(cc)s.6mmblur_REML_gm' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


stim_dict = {
    #'LSRS': {'sess1': ['SC5', 'SC6', 'SC2', 'AV2.1', 'AV1.1', 'AV3.1'], 'sess2': ['SC1', 'SC3', 'SC4', 'AV1.2', 'AV3.2', 'AV2.2']}
    #'NNPT': {'sess1': ['SC1', 'SC2', 'SC3', 'AV1.1', 'AV2.1', 'AV3.1'], 'sess2': ['SC4', 'SC5', 'SC6', 'AV3.2', 'AV2.2', 'AV1.2']}
    #'SSGO': {'sess1': ['SC1', 'SC2', 'SC3', 'AV1.1', 'AV2.1', 'AV3.1'], 'sess2': ['SC4', 'SC5', 'SC6', 'AV3.2', 'AV2.2', 'AV1.2']}
    'SEKI': {'sess1': ['SC2', 'SC1', 'SC6', 'AV2.1', 'AV1.1', 'AV3.1'], 'sess2': ['SC4', 'SC5', 'SC3', 'AV1.2', 'AV3.2', 'AV2.2']}
    #'JNWL': {'sess1': ['SC4', 'SC1', 'SC3', 'AV2.1', 'AV3.1', 'AV1.1'], 'sess2': ['SC2', 'SC6', 'SC5', 'AV3.2', 'AV1.2', 'AV2.2']}
}


if __name__ == "__main__":
    
    for ss in stim_dict.keys():
        os.chdir(os.environ['decor']+'/%(ss)s/6mmblur_results' % locals())  # now setting dir here for 6mmblur
        for sess in stim_dict[ss]:
            #ll = ' '.join(map(str, ['%(ss)s.' % locals() + cc + '.results/pb03.%(ss)s.' % locals() + cc + '.r01.volreg+orig' for cc in stim_dict[ss][sess]]))
            ll = ' '.join([os.environ['decor']+'/%s/%s.%s.6mmblur.results/pb03.%s.%s.6mmblur.r01.volreg+orig' % (ss, ss, cc, ss, cc) for cc in stim_dict[ss][sess]])
            avgepis(ss, sess, ll)
            mean_sess(ss, sess)

        align_epis(ss)
        for cc in stim_dict[ss]['sess2']:
            allineate(ss, cc)

        for cc in stim_dict[ss]['sess1']:
            copyn(ss, cc)


