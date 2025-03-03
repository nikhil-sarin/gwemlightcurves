# https://arxiv.org/abs/1611.09822
# https://arxiv.org/abs/1705.07084

import os, sys, glob
import numpy as np
import scipy.interpolate
from scipy.interpolate import interpolate as interp
from scipy.interpolate import griddata

from .model import register_model
from .. import KNTable

from kilonova_lightcurves import lightcurve_utils, Global, svd_utils
from kilonova_lightcurves.EjectaFits.DiUj2017 import calc_meje, calc_vej

def get_RoFe2017_model(table, **kwargs):

    if not 'n_coeff' in table.colnames:
        table['n_coeff'] = 100

    if not Global.svd_mag_model == 0:
        svd_mag_model = Global.svd_mag_model
    else:
        svd_mag_model = svd_utils.calc_svd_mag(table['tini'][0], table['tmax'][0], table['dt'][0], model = "RoFe2017", n_coeff = table['n_coeff'][0])
        Global.svd_mag_model = svd_mag_model

    if not Global.svd_lbol_model == 0:
        svd_lbol_model = Global.svd_lbol_model
    else:
        svd_lbol_model = svd_utils.calc_svd_lbol(table['tini'][0], table['tmax'][0], table['dt'][0], model = "RoFe2017", n_coeff = table['n_coeff'][0])
        Global.svd_lbol_model = svd_lbol_model

    if not 'mej' in table.colnames:
        # calc the mass of ejecta
        table['mej'] = calc_meje(table['m1'], table['mb1'], table['c1'], table['m2'], table['mb2'], table['c2'])
        # calc the velocity of ejecta
        table['vej'] = calc_vej(table['m1'], table['c1'], table['m2'], table['c2'])

    # Throw out smaples where the mass ejecta is less than zero.
    mask = (table['mej'] > 0)
    table = table[mask]
    if len(table) == 0: return table

    # Log mass ejecta
    table['mej10'] = np.log10(table['mej'])
    # Initialize lightcurve values in table

    timeseries = np.arange(table['tini'][0], table['tmax'][0]+table['dt'][0], table['dt'][0])
    table['t'] = [np.zeros(timeseries.size)]
    table['lbol'] = [np.zeros(timeseries.size)]
    table['mag'] =  [np.zeros([9, timeseries.size])]

    # calc lightcurve for each sample
    for isample in range(len(table)):
        table['t'][isample], table['lbol'][isample], table['mag'][isample] = svd_utils.calc_lc(table['tini'][isample], table['tmax'][isample],table['dt'][isample], [np.log10(table['mej'][isample]),table['vej'][isample],table['Ye'][isample]],svd_mag_model = svd_mag_model, svd_lbol_model = svd_lbol_model, model = "RoFe2017")

    return table

register_model('RoFe2017', KNTable, get_RoFe2017_model,
                 usage="table")
