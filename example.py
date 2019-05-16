from dataclass import Star

# ------------------------------------------
# -          LOADING TIME SERIES           -
# ------------------------------------------

# Create a star object and load in the time series (which may be in separate 
# pieces)

star = Star('./tutorial/example_lc_1.fits', './tutorial/example_lc_2.fits')

# Star data can also be loaded in using wildcards.

star = Star('*.fits')

# This will load all the '.fits' files in the current directory and attempt
# to piece them together into a single, continuous time series. If you do this,
# make sure all the '.fits' files in the directory are from the same star and
# that there are no duplicate files!


star.filter()

star.plot()

star.prepare()

star.export()
