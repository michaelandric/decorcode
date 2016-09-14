# -*- coding: utf-8 -*-
"""
re-working this Thu May  5 12:04:12 2016 and June 8 2016.

@author: andric

Run names, e.g., 'SC5' correspond to the
stimuli file (SC5.avi in this case) that were shown.
Order of these stimuli files found in
Google Drive file 'SS runs; presentation order and answers'
"""


import os
import shutil
from shlex import split
from glob import glob
from subprocess import Popen
from subprocess import STDOUT


class DoReconstruction(object):
    """Go from dicom images to AFNI."""

    def __init__(self, subject, scan_dictionary):
        """initialize with subject and dictionary."""
        self.subj = subject
        self.scan_dict = scan_dictionary

    def reconstruct(self):
        """Implement the AFNI programs."""
        dicom_base = os.path.join(os.environ['decor'],
                                  'subject_dicoms/HASURI002X49')
        subj_dir = os.path.join(os.environ['decor'], self.subj)
        os.chdir(subj_dir)
        print("Now in: \n")
        print(os.getcwd())

        if not os.path.exists(os.path.join(subj_dir, 'stdout_files')):
            os.makedirs(os.path.join(subj_dir, 'stdout_files'))
        for session_dir in self.scan_dict:
            for stim, i in self.scan_dict[session_dir]:
                tmp_dir = os.path.join(subj_dir, 'dicomtmp{}'.format(stim))
                if not os.path.exists(tmp_dir):
                    os.makedirs(tmp_dir)

                dic_dir = os.path.join(dicom_base, session_dir,
                                       'LNIF_Hasson_Uri_Eight-channel-RF-coil',
                                       '{}_lnif_epi1_4x4x4_TR1500_DiCo'.format(i))
                for filename in glob('{}/*.DCM'.format(dic_dir)):
                    shutil.copy2(filename, tmp_dir)

                stdf = open('stdout_files/stdout_from_to3d_{}.txt'.format(
                    stim), 'w')
                cmdargs = split('Dimon -infile_prefix {}/*.DCM -dicom_org \
                                -gert_create_dataset -gert_outdir {} \
                                -gert_to3d_prefix raw.{}.{}.gert_reco'.format(
                                    tmp_dir, subj_dir, self.subj, stim))
                print(cmdargs)
                Popen(cmdargs, stdout=stdf, stderr=STDOUT)
                stdf.close()

    def reconstruct_anat(self):
        """Vary the method for the anatomical images."""
        dicom_base = os.path.join(os.environ['decor'],
                                  'subject_dicoms/HASURI002X49')
        subj_dir = os.path.join(os.environ['decor'], self.subj)
        os.chdir(subj_dir)
        print("Now in: \n")
        print(os.getcwd())

        if not os.path.exists(os.path.join(subj_dir, 'stdout_files')):
            os.makedirs(os.path.join(subj_dir, 'stdout_files'))
        for session_dir in self.scan_dict:
            for stim, i, proto in self.scan_dict[session_dir]:
                tmp_dir = os.path.join(subj_dir, 'dicomtmp{}'.format(stim))
                if not os.path.exists(tmp_dir):
                    os.makedirs(tmp_dir)

                dic_dir = os.path.join(dicom_base, session_dir,
                                       'LNIF_Hasson_Uri_Eight-channel-RF-coil',
                                       '{}_t1_mprage_{}_pat2'.format(i, proto))
                for filename in glob('{}/*.DCM'.format(dic_dir)):
                    shutil.copy2(filename, tmp_dir)

                stdf = open('stdout_files/stdout_from_to3d_{}.txt'.format(
                    stim), 'w')
                cmdargs = split('Dimon -infile_prefix {}/*.DCM -dicom_org \
                                -gert_create_dataset -gert_outdir {} \
                                -gert_to3d_prefix {}.{}.gert_reco'.format(
                                    tmp_dir, subj_dir, self.subj, stim))
                print(cmdargs)
                Popen(cmdargs, stdout=stdf, stderr=STDOUT)
                stdf.close()


def main():

    """Main wrapper to put together the methods."""
    scan_dict = {'19961023RSDE_201606201400':
                 [('SC4', 12), ('SC3', 16), ('SC2', 20),
                  ('AV2.1', 24), ('AV1.1', 28), ('AV3.1', 32), ('Rest', 6)],
                 '19961023RSDE_201607041550':
                 [('SC6', 6), ('SC5', 10), ('SC1', 14),
                  ('AV2.2', 18), ('AV3.2', 22), ('AV1.2', 26)]}

    anat_scan_dict = {'19961023RSDE_201606201400':
                      [('mprage1', 2, 'CNR'), ('mprage2', 33, 'SNR')],
                      '19961023RSDE_201607041550':
                      [('mprage_2ndsess', 2, 'CNR')]}

    reco = DoReconstruction('RSDE', scan_dict)
    reco.reconstruct()

    reco = DoReconstruction('RSDE', anat_scan_dict)
    reco.reconstruct_anat()

if __name__ == '__main__':
    main()
