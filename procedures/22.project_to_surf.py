# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:59:05 2015.

@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def vol_to_surf_mni(log, hemi, parent, pn, outname):
    """Project volume to surface."""
    log.info("Project volume to surface...")
    log.info("Parent: ", parent)
    log.info("outname: ", outname)
    suma_dir = '/mnt/lnif-storage/urihas/software/AFNI2015/suma_MNI_N27'
    cmdargs = split('3dVol2Surf -spec %s \
                    -surf_A %s.smoothwm.gii -surf_B %s.pial.gii \
                    -sv %s -grid_parent %s \
                    -map_func max -f_steps 10 -f_index voxels \
                    -f_p1_fr -%s -f_pn_fr %s \
                    -outcols_NSD_format -oob_index -1 -oob_value 0.0 \
                    -out_1D %s' %
                    (os.path.join(suma_dir, 'MNI_N27_%s.spec' % hemi),
                     hemi, hemi,
                     os.path.join(suma_dir, 'MNI_N27_SurfVol.nii'),
                     parent, pn, pn, outname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Set names to call vol2surf_mni."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'project_to_surf'))
    os.chdir(os.path.join(os.environ['decor'], 'randomise_repmeas'))
    pndiff = '1.0'
    # No clusters survive tstat4 so do only the first 3
    for i in range(1, 4):
        for h in ['lh', 'rh']:
            parnt = os.path.join(os.environ['decor'], 'randomise_repmeas',
                                 '%s_clustere_corrp_tstat%d_thr005' %
                                 ('repmeas_randomise_out_n5000', i))
            vol_to_surf_mni(logfile, h, '%s.nii.gz' % parnt, pndiff,
                            '%s_%s_pn%s_MNI_N27.1D' % (parnt, h, pndiff))


if __name__ == '__main__':
    main()
