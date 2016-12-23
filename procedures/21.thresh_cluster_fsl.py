# -*- coding: utf-8 -*-
"""
Created November 2016.

(AFNI doesn't work in 3+)

@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def fsl_maths(log, corrp, statimg, outname):
    """Threshold via FSL procedure."""
    log.info('Doing fsl_maths to threshold the image...')
    cmdargs = split('fslmaths {} -thr 0.95 -bin -mul {} {}'.format(
        corrp, statimg, outname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def cluster(log, inputf, clustindx, lmax, omeanf, clustsize):
    """Cluster via FSL procedure."""
    log.info('Now doing cluster...')
    log.info('input file: ', inputf)
    log.info('clustindx: ', clustindx)
    cmdargs = split('cluster --in={} --thresh=0.005 --oindex={} \
                    --olmax={} --omean={} --osize={} --mm'.format(
                        inputf, clustindx, lmax, omeanf, clustsize))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def cluster_addon_metric(log, inputf, clustindx, lmax, omeanf, clustsize):
    """Cluster via FSL procedure. Now also get mean for images."""
    log.info('Now doing cluster...')
    log.info('input file: ', inputf)
    log.info('clustindx: ', clustindx)
    cmdargs = split('cluster --in={} --thresh=0.005 --oindex={} \
                    --olmax={} --omean={} --osize={} --mm'.format(
                        inputf, clustindx, lmax, omeanf, clustsize))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Call methods for thresholding and clustering."""
    lname = 'thresh_cluster_fsl_randomise_3set_moremetrics'
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs', lname))
    logfile.info('Threshold and cluster.')
    os.chdir(os.path.join(os.environ['decor'], 'randomise_3set_moremetrics'))

    pref = 'repmeas_randomise3set_p005_n5000'
    for ctype in ['clusterm', 'tfce']:
        for i in range(1, 4):
            cluster_addon_metric(logfile,
                                 '{}_{}_corrp_tstat{}_fwe05.nii.gz'.format(pref, ctype, i),
                                 '{}_{}_corrp_tstat{}_fwe05_cluster_index'.format(pref, ctype, i),
                                 '{}_{}_corrp_tstat{}_fwe05lmax.txt'.format(pref, ctype, i),
                                 '{}_{}_corrp_tstat{}_thr005_fwe05omean.txt'.format(pref, ctype, i),
                                 '{}_{}_corrp_tstat{}_fwe05cluster_size'.format(pref, ctype, i))


if __name__ == '__main__':
    main()
