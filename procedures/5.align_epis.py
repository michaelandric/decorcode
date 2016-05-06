# -*- coding: utf-8 -*-
"""
code overhaul on Fri May  6 13:27:13 2016

See avgepis doc for warning about the way these should be run

@author: andric
"""

import os
from shlex import split
from subprocess import call
from subprocess import STDOUT


def avgepis(subj, sess, epilist):
    """Do this function first and separate.
    Otherwise it fucks up everything else, since it will try to run other
    functions without the average being completed."""
    stdf = open('stdout_files/stdout_from_alignepis.txt', 'w')
    cmdargs = split('3dMean -prefix {}_{}_6mmblur_avgepi {}'.format(
        subj, sess, epilist))
    call(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()


def mean_sess(subj, sess):
    """Get the the mean over the runs"""
    stdf = open('stdout_files/stdout_from_meanses.txt', 'w')
    cmdargs = split('3dTstat -prefix {}_{}_6mmblur_meanepi \
                    -mean {}_{}_6mmblur_avgepi+orig'.format(
                        subj, sess, subj, sess))
    call(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()


def align_epis(subj):
    """
    Creating template to align second session runs to first session.
    """
    stdf = open('stdout_files/stdout_from_epi_align2.txt', 'w')
    cmdargs = split('align_epi_anat.py -dset1 {}_sess1_6mmblur_meanepi+orig \
                    -dset2 {}_sess2_6mmblur_meanepi+orig -dset2to1 \
                    -epi_base 0 -anat_has_skull no -master_dset1_dxyz BASE \
                    -giant_move -suffix _gm'.format(subj, subj))
    call(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()


def allineate(subj, cond):
    """Only need this for aligning second session runs to their
    first session counterparts. First session already good from 3dvolreg.
    """
    basedir = os.path.join(os.environ['decor'], subj,
                           '{}.{}.6mmblur.results'.format(subj, cond))
    infile = os.path.join(basedir,
                          'errts.{}.{}.6mmblur_REML+orig'.format(subj, cond))
    stdf = open('stdout_files/stdout_from_allineate_epis.txt', 'w')
    cmdargs = split('3dAllineate -cubic -base {ss}_sess1_6mmblur_meanepi+orig \
                    -1Dmatrix_apply {ss}_sess2_6mmblur_meanepi_gm_mat.aff12.1D \
                    -prefix errts.{ss}.{cc}.6mmblur_REML_gm \
                    -input {infile} -master SOURCE \
                    -weight_frac 1.0 -maxrot 6 -maxshf 10 -VERB \
                    -warp aff -source_automask+2 -twopass'.format(
                        ss=subj, cc=cond, infile=infile))
    call(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()


def copyn(subj, cond):
    """This is to copy errts into the dir and
    have contiguous naming convention
    """
    stdf = open('stdout_files/stdout_from_3dcopy_epis_sess1.txt', 'w')
    basedir = os.path.join(os.environ['decor'], subj,
                           '{}.{}.6mmblur.results'.format(subj, cond))
    cmdargs = split('3dcopy {}/errts.{}.{}.6mmblur_REML+orig \
                    errts.{}.{}.6mmblur_REML_gm'.format(
                        basedir, subj, cond, subj, cond))
    call(cmdargs, stdout=stdf, stderr=STDOUT)
    stdf.close()


def do_all(stimdict):
    """Wrapper function to execute all the above
    Arg:
        stimdict: This is a dict of a dict
        Contains the subject identifier --> session --> run order
    """
    for subject in stimdict.keys():
        os.chdir(os.path.join(os.environ['decor'], subject, '6mmblur_results'))
        for session in stimdict[subject]:
            epilist = []
            for run in stimdict[subject][session]:
                rundir = os.path.join(os.environ['decor'],
                                      '{}.{}.6mmblur.results'.format(
                                          subject, run))
                fname = 'pb03.{}.{}.6mmblur.r01.volreg+orig'.format(
                    subject, run)
                epilist.append(os.path.join(rundir, fname))

            epilist = ' '.join(epilist)
            avgepis(subject, session, epilist)
            mean_sess(subject, session)

        align_epis(subject)
        for run in stimdict[subject]['sess2']:
            allineate(subject, run)

        for run in stimdict[subject]['sess1']:
            copyn(subject, run)


if __name__ == "__main__":

    STIMDICT = {
        'LNSE': {'sess1': ['SC5', 'SC2', 'SC6', 'AV3.1', 'AV2.1', 'AV1.1'],
                 'sess2': ['SC1', 'SC4', 'SC3', 'AV1.2', 'AV3.2', 'AV2.2']}}

    do_all(STIMDICT)
