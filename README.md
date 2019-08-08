# PRESTOport
Currently supported telescopes are: TESS

PRESTOport is a software package written in Python that reduces light curves from EvryScope and TESS, to port them to PRESTO for analysis. To use PRESTOport, clone the repository and take a look at example.py, which is effectively a tutorial for getting started in lieu of more formal documentation. Sample light curves from TESS are included to practice with. These are in the examples/ sub-directory.

PRESTOport's functionality includes:
 * Removing bad data based on TESS quality flags
 * Filtering light curves to remove noise / dropouts
 * Rebinning light curves to an evenly-sampled interval using three methods: median-replace, running-median-replace, and no replacement
 * Exporting light curve data in the ``.dat`` and ``.inf`` format necessitated by PRESTO's FFT process
 * Generating simulated data from existing light curves, including injecting artificial signal and artificial noise
 * Light curve plotting and reduced chi squared analysis
