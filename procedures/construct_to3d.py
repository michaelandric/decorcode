#!/usr/bin/python

import os
import shutil
from shlex import split
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
    'NNPT': {
    'SC1': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201404301030/LNIF_Hasson_Uri_Eight-channel-RF-coil/14_lnif_epi1_4x4x4_TR1500_DiCo',
    'SC2': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201404301030/LNIF_Hasson_Uri_Eight-channel-RF-coil/18_lnif_epi1_4x4x4_TR1500_DiCo',
    'SC3': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201404301030/LNIF_Hasson_Uri_Eight-channel-RF-coil/22_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV1.1': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201404301030/LNIF_Hasson_Uri_Eight-channel-RF-coil/26_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV2.1': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201404301030/LNIF_Hasson_Uri_Eight-channel-RF-coil/30_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV3.1': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201404301030/LNIF_Hasson_Uri_Eight-channel-RF-coil/34_lnif_epi1_4x4x4_TR1500_DiCo',
    }}

stim_dict = {
    'NNPT': {
    'SC4': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201405120830/LNIF_Hasson_Uri_Eight-channel-RF-coil/7_lnif_epi1_4x4x4_TR1500_DiCo',
    'SC5': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201405120830/LNIF_Hasson_Uri_Eight-channel-RF-coil/11_lnif_epi1_4x4x4_TR1500_DiCo',
    'SC6': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201405120830/LNIF_Hasson_Uri_Eight-channel-RF-coil/15_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV1.2': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201405120830/LNIF_Hasson_Uri_Eight-channel-RF-coil/19_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV2.2': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201405120830/LNIF_Hasson_Uri_Eight-channel-RF-coil/23_lnif_epi1_4x4x4_TR1500_DiCo',
    'AV3.2': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201405120830/LNIF_Hasson_Uri_Eight-channel-RF-coil/27_lnif_epi1_4x4x4_TR1500_DiCo'
    }}
"""
stim_dict = {
    'NNPT': {
    'Rest': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19910517NNPT_201404301030/LNIF_Hasson_Uri_Eight-channel-RF-coil/10_lnif_epi1_4x4x4_TR1500_DiCo/'
    }}

for ss in stim_dict.keys():
    sess_dir = '/mnt/lnif-storage/urihas/MAdecorproj/%(ss)s' % locals ()
    os.chdir(sess_dir)

    for stim in stim_dict[ss]:
        tmp_dir = '/mnt/lnif-storage/urihas/MAdecorproj/%(ss)s/dicomtmp%(stim)s' % locals()
        mk(ss, tmp_dir)

        for filename in glob(stim_dict[ss][stim]+'/*.DCM'):
            shutil.copy2(filename, tmp_dir)

        f = open('stdout_files/stdout_from_to3d_'+stim+'.txt', 'w')
        #cmd = 'to3d -datum float -time:zt 25 333 1.5s altplus -prefix raw.LSRS.'+stim+' '+tmp_dir+'/*.DCM'
        cmd = 'Dimon -infile_prefix %(tmp_dir)s/*.DCM -dicom_org -gert_create_dataset -gert_outdir %(sess_dir)s -gert_to3d_prefix raw.%(ss)s.%(stim)s.gert_reco' % locals()
        cmdargs = split(cmd)
        print cmdargs
        Popen(cmdargs, stdout = f, stderr = STDOUT)
        f.close()


