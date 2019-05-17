from dataclass import Star
import numpy as np


# REAL DATA
# =========


# LOADING TIME SERIES
# -------------------

# Create a star object and load in the time series (which may be in separate 
# pieces)

### star = Star('./example/example_lc_1.fits', './example/example_lc_2.fits')

# Star data can also be loaded in using wildcards.

star = Star('./example/*.fits')

# This will load all the '.fits' files in the current directory and attempt
# to piece them together into a single, continuous time series. If you do this,
# make sure all the '.fits' files in the directory are from the same star and
# that there are no duplicate files!


# FILTERING                     
# ---------

# Remove bad data. Takes out data points with 10% highest error, and removes 
# all data with bad TESS quality flags.

star.filter()

# PLOTTING
# --------

# Show the time series on axes of flux and BJD.

### star.plot()

# ^ This also returns the chi squared of the data, which can be slow sometimes. 
# If you want only the light curve plot, do this (much quicker)

### star.plot(chsq=False)

# You can also Save the figure to a pickle file, to preserve its interactivity.
# Run 'python plotpickle.py ./example/example_plot.pickle' to plot the pickled 
# figure.

star.plot(filename='./example/example_plot.pickle')

# BINNING
# -------

# The 'prepare' method rebins the flux and error, overwriting the object's
# 'data' attribute. Afterwards, it is ready to be exported for analysis in 
# PRESTO.

star.prepare()

# EXPORTING
# ---------

# If no arguments are provided, this will save two new files using the star's
# TIC ID as the root filename.

star.export('./example/')

# At this point, a star's time series has been filtered, prepared, and exported
# for Fourier analysis in PRESTO.

# It may also be necessary to create some simulated data to compare this 'real'
# data against.


# SIMULATED DATA
# ==============

# It's best to start from real data, so you can decide whether or not you want
# to preserve the window function of the original time series.

# Load the data
star = Star('./example/*.fits')

# Filter
star.filter()

# Replace all the flux with the median
median_flux = np.median(star.data['flux'])
n = len(star.data)
star.data['flux'] = np.full(n, median_flux)

# Inject a sine wave into this median flux
star.inject(10000., 0.125) # (Flux in e-/s, Period in days)

# You can also add some white noise if you like
star.addnoise(100.) # (Amplitude of noise in e-/s, centered about the data)

# Now this simulated data (with gaps) can be prepared and exported too
star.prepare()

# Give it a different name so our real data doesn't get overwritten
star.export(filename='./example/'+star.id+'_SIMULATED')
