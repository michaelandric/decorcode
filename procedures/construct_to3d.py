#!/usr/bin/python

import os
import shutil
import shlex
from glob import glob
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE

"""
For full provenance, will include full paths
Run names, e.g., 'SC5' correspond to the stimuli file (SC5.avi in this case) that were shown.
Order of these stimuli files found in Google Drive file 'SS runs; presentation order and answers'
"""

def mk(ss, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def rmdir(ss, dir):
    shutil.rmtree(dir)

"""
stim_dict = {
    'LSRS': {
    'SC5': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201405271250/LNIF_Hasson_Uri_Eight-channel-RF-coil/11_lnif_epi1_4x4x4_TR1500_DiCo',
    'SC6': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201405271250/LNIF_Hasson_Uri_Eight-channel-RF-coil/19_lnif_epi1_4x4x4_TR1500_DiCo',
    'SC2': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201405271250/LNIF_Hasson_Uri_Eight-channel-RF-coil/23_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV2.1': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201405271250/LNIF_Hasson_Uri_Eight-channel-RF-coil/27_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV1.1': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201405271250/LNIF_Hasson_Uri_Eight-channel-RF-coil/31_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV3.1': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201405271250/LNIF_Hasson_Uri_Eight-channel-RF-coil/35_lnif_epi1_4x4x4_TR1500_DiCo',
    'SC1': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201406031250/LNIF_Hasson_Uri_Eight-channel-RF-coil/8_lnif_epi1_4x4x4_TR1500_DiCo',
    'SC3': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201406031250/LNIF_Hasson_Uri_Eight-channel-RF-coil/12_lnif_epi1_4x4x4_TR1500_DiCo',
    'SC4': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201406031250/LNIF_Hasson_Uri_Eight-channel-RF-coil/16_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV1.2': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201406031250/LNIF_Hasson_Uri_Eight-channel-RF-coil/20_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV3.2': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201406031250/LNIF_Hasson_Uri_Eight-channel-RF-coil/24_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV2.2': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201406031250/LNIF_Hasson_Uri_Eight-channel-RF-coil/28_lnif_epi1_4x4x4_TR1500_DiCo'
    }}
"""

stim_dict = {
    'LSRS': {
    'Rest': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201405271250/LNIF_Hasson_Uri_Eight-channel-RF-coil/7_lnif_epi1_4x4x4_TR1500_DiCo/'
    }}

for ss in stim_dict.keys():
    os.chdir('/mnt/lnif-storage/urihas/MAdecorproj/%(ss)s' % locals ())
    for stim in stim_dict[ss]:
        tmp_dir = '/mnt/lnif-storage/urihas/MAdecorproj/%(ss)s/dicomtmp%(stim)s' % locals()
        mk(ss, tmp_dir)
        for filename in glob(stim_dict[ss][stim]+'/*.DCM'):
            shutil.copy2(filename, tmp_dir)

        print os.system("ls "+tmp_dir+"/ | wc")        
        f = open('stdout_from_to3d_'+stim+'.txt', 'w')
        #cmd = 'to3d -datum float -time:zt 25 333 1.5s altplus -prefix raw.LSRS.'+stim+' '+tmp_dir+'/*.DCM'
        cmd = 'to3d -datum float -time:zt 25 165 1.5s altplus -prefix raw.LSRS.'+stim+' '+tmp_dir+'/*.DCM'
        cmdargs = shlex.split(cmd)
        print cmdargs
        Popen(cmdargs, stdout = f, stderr = STDOUT)
        f.close()
        #shutil.rmtree(tmp_dir)   # rm temp dir

