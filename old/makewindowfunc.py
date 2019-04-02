from data_class import Star
import argparse
from astropy.table import Table
import numpy as np

parser = argparse.ArgumentParser(description='Make .dat and .inf files containing randomly generated noise within the window function of the time series.')
parser.add_argument('filename', metavar='filename', type=str, help='filename of the time series data')
parser.add_argument('--hash', metavar='hash', type=str, help='hash of the original .dat and .inf files produced for this time series')
args = parser.parse_args()

fname = args.filename

star = Star(fname)
try:
    star.uuid = args.hash+'_WINDOWNOISE'
except AttributeError:
    star.uuid = star.uuid+'_WINDOWNOISE'

n_datapoints = len(star.data['flux'])
random_noise = np.random.uniform(low=99., high=101., size=n_datapoints)

star.data['flux'] = random_noise

star.rebin()
star.export()




