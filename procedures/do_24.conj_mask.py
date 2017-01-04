# -*- coding: utf-8 -*-
"""Created Dec 2016.

Implement basic 3dCalc commands.
@author: andric.
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def conjunciton_overlap(log, afile, bfile, cfile, outname):
    """Overlap different functional images.

    expr arg is expression in 3dcalc
    e.g., step(a)+2*step(b)
    e.g., ispositive(a-b) + 2*ispositive(a-c)
    """
    log.info("Overlap func datasets.")
    log.info("Output: %s", outname)
    cmdargs = split("3dcalc -a %s -b %s -c %s \
                    -expr 'ispositive(a-b) + 2*ispositive(a-c)' -prefix %s" %
                    (afile, bfile, cfile, outname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())

def conj_twocond_contr(log, afile, bfile, outname):
    """Overlap different functional images.
    expr arg is expression in 3dcalc
    e.g., step(a)+2*step(b)
    e.g., ispositive(a-b) + 2*ispositive(a-c)
    """
    log.info("Overlap func datasets.")
    log.info("Output: %s", outname)
    cmdargs = split("3dcalc -a %s -b %s \
                    -expr 'ispositive(a) + 2*ispositive(b)' -prefix %s" %
                    (afile, bfile, outname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Call methods for thresholding and clustering."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'twocond_contr_conj_mask'))
    logfile.info('Threshold and cluster.')
    os.chdir(os.path.join(os.environ['decor'], 'randomise_twocond_contr_conj'))

    for ctype in ['clustere', 'clusterm', 'tfce']:
        conj_twocond_contr(logfile,
                           'AVvA_randomise_out_n5000_p005_{}_corrp_tstat1_fwe05.nii.gz'.format(ctype),
                           'AVvV_randomise_out_n5000_p005_{}_corrp_tstat1_fwe05.nii.gz'.format(ctype),
                           'conj_AVvA_AVvV_n5000_p005_{}_corrp_tstat1_fwe05'.format(ctype))


if __name__ == '__main__':
    main()
