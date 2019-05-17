import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord as sc
from astropy.table import Table, vstack
from astropy.utils.console import ProgressBar
from matplotlib import pyplot as plt
from scipy.stats import chisquare
from astropy.io import fits
from utils import uconv
from glob import glob
import pickle
import os
import warnings
from rebin import rebin


class ArgumentError(ValueError):
    pass


class Star(object):
    '''
    A class to handle individual stars from time series data.
    '''

    def __init__(self, *args):

        # See if argument should be handled by glob, or if it's one or more 
        # complete filenames instead
        check_wildcard = []
        for arg in args:
            check_wildcard.append('*' in arg)
        wildcard = any(check_wildcard)

        # If a wildcard is present, use glob to find matching filenames
        if wildcard:
            if len(args)==1:
                self.filenames = glob(str(args[0]))
                if len(self.filenames) == 0:
                    raise ArgumentError('No filenames found!')
            else:
                raise ArgumentError('Too many arguments to use a wildcard.')
        else:
            self.filenames = [os.path.abspath(arg) for arg in args]

        self.get_data()
        self.filtered = False


    def get_data(self):

        with fits.open(self.filenames[0], mode='readonly') as hdulist:
            self.time_unit = u.Unit(hdulist[1].header['TIMEUNIT'])

            self.ra = hdulist[1].header['RA_OBJ']
            self.dec = hdulist[1].header['DEC_OBJ']
            self.id = str(hdulist[0].header['TICID'])

            self.exposure_time = hdulist[1].header['TIMEDEL'] # days
            
        s = sc(ra=self.ra*u.degree, dec=self.dec*u.degree).to_string('hmsdms')

        self.ra_hms = (s.split(' ')[0].split('h')[0]
                      + ':' 
                      + s.split(' ')[0].split('h')[1].split('m')[0]
                      + ':'
                      + s.split(' ')[0].split('m')[1].split('s')[0])

        self.dec_dms = (s.split(' ')[1].split('d')[0]
                       + ':' 
                       + s.split(' ')[1].split('d')[1].split('m')[0]
                       + ':'
                       + s.split(' ')[1].split('m')[1].split('s')[0])

        datalist = []

        for filename in self.filenames:
            with fits.open(filename, mode='readonly') as hdulist:

                bjd = hdulist[1].data['TIME']
                bjd_nans = np.isnan(bjd)

                flux = hdulist[1].data['SAP_FLUX']
                flux_nans = np.isnan(flux)

                err = hdulist[1].data['SAP_FLUX_ERR']
                err_nans = np.isnan(err)

                flags = hdulist[1].data['QUALITY']

                nan_mask = np.invert(np.logical_or(bjd_nans, flux_nans, 
                                                   err_nans))
        
                data = Table([bjd[nan_mask], flux[nan_mask], err[nan_mask], 
                              flags[nan_mask]], names=['bjd', 'flux', 'err', 
                                                       'flags'], masked=True)                
                datalist.append(data)

        if len(datalist) > 1:
            self.data = vstack([data for data in datalist])
        else:
            self.data = datalist[0]

        self.data.sort('bjd')
        self.flux = self.data['flux']
        self.err = self.data['err']
        self.bjd = self.data['bjd']
        self.flags = self.data['flags']
        
        self.duration = ((self.data['bjd'][-1] - self.data['bjd'][0])
                        * self.time_unit)

    def filter(self, tolerance=0.1):
        # Filtering based on bad data flags (FOR TESS DATA ONLY)
        # Flags commented out of the list below are kept
        flags_key = [
#            0, # None
            8, # Spacecraft is in Earth point
            32, # Reaction wheel desaturation event
            128, # manual exclude (anomaly)
            512, # Impulsive outlier removed before cotrending
                    ]

        # Native flags are powers of two
        native_flags = np.array(2)**range(12)
        native_flags = np.insert(native_flags, 0, 0, axis=0)

        for flag in set(self.data['flags']):
            if flag in flags_key:   
                self.data.remove_rows(self.data['flags'] == flag)
            elif flag not in native_flags:
                self.data.remove_rows(self.data['flags'] == flag)

        self.data.sort('err')
        self.data.reverse()
        n_to_kill = int(np.round(tolerance*len(self.data)))
        self.data.remove_rows(range(n_to_kill))
        self.data.sort('bjd')
        self.filtered = True


    def inject(self, amplitude, period):
        omega = 2.*np.pi/period
        t = np.array(self.data['bjd'])
        sinflux = amplitude*np.sin(omega*t)

        sumflux = np.array(self.data['flux']) + sinflux
        self.data['flux'] = sumflux
        self.flux = sumflux


    def addnoise(self, amplitude, plot=False):
        n = len(self.data['flux'])
        noise = amplitude*np.random.random(n) - 0.5*amplitude
        self.data['flux'] = self.data['flux'] + noise
        self.flux = self.data['flux']

        if plot:
            plt.hist(noise)
            plt.title('White noise added to flux points')
            plt.xlabel('Flux (e-/s)')
            plt.ylabel('n')
            plt.show()


    def prepare(self):

        if self.filtered == False:
            print('Filtering data...')
            self.filter()
        
        print('Rebinning flux...')
        rebin_flux = rebin(self.data['bjd','flux'], binwidth=2./60./24., 
                           exptime=2./60./24., timestamp_position=0.5, 
                           median_replace=True)
        print('Rebinning error...')    
        rebin_err = rebin(self.data['bjd','err'], binwidth=2./60./24., 
                          exptime=2./60./24., timestamp_position=0.5, 
                          median_replace=True)

        new_bjd = rebin_flux[:,0]
        new_flux = rebin_flux[:,1]
        new_err = rebin_err[:,1]

        self.bjd = new_bjd
        self.flux = new_flux
        self.err = new_err

        self.data = Table([new_bjd, new_flux, new_err], 
                          names=['bjd', 'flux', 'err'])

        print('Done!')


    def plot(self, filename=None, chsq=True):
        """
        Plot the light curve.

        Parameters
        ----------
        filename : str, optional
            The filename of the pickled matplotlib figure to save. If not 
            provided, the figure will be displayed without saving.
        chsq : boolean, optional
            If true, the light curve will be fitted to a 0-order polynomial
            to measure the reduced chi squared. This is intended to be a 
            measure of how variable or non-variable the light curve is.

        Returns
        -------
        None : None
            None is returned if chsq is set to False.
        chsq : float
            The reduced chi squared of the light curve, if chsq is set to True.
        """

        
        fig = plt.figure(figsize=[10,4])
        ax = fig.add_subplot(111)
        ax.errorbar(self.data['bjd'], self.data['flux'], alpha=0.5,
                    yerr=self.data['err'], ms=2, fmt='ko', elinewidth=.5)

        if chsq is True:
            x = np.linspace(0, len(self.data) - 1, len(self.data))
            z = np.polyfit(x, self.data['flux'], 1)

            chsq = np.sum(((self.data['flux'] - np.polyval(z, x)) ** 2.)
                          / self.data['err']**2.)/(len(self.data) - 1)
            p = np.poly1d(z)
            ax.plot(self.data['bjd'], p(self.data['bjd']), 'b--')
            ax.text(0.1, 0.9, "Reduced Chi Squared: {:.4f}".format(chsq), 
                    transform=ax.transAxes)

        ax.set_xlabel('BJD (Days)')
        ax.set_ylabel('Flux (e-/s)')
        ax.set_title('ID: {}    Avg Brightness = {:.2f} e-/s'
                     .format(str(self.id), np.mean(self.data['flux'])))
        
        if filename is not None:
            pickle.dump(ax, open(filename, 'wb'))
        else:
            plt.show()
            plt.close()
        
        return chsq


    def split_nights(self):
        """
        Split a star's time series data by night of observation. Intended for
        use only with ground-based telescopes.

        Parameters
        ----------
        None
        
        Returns
        -------
        nights: list
            List of astropy.table.Table objects, one for each night of 
            observations.
        """
        bjds = np.array(list(self.data['bjd']))
        gaps = bjds[1:] - bjds[:-1] # Time between consecutive data points
        gap_indices = np.where(gaps > 0.01)[0]

        nights = [self.data[:gap_indices[0]]]
        for i in range(1, len(gap_indices)-1):
            nights.append(self.data[gap_indices[i]+1:gap_indices[i+1]])
        nights.append(self.data[(gap_indices[-1]+1):])
        return nights


    def export(self, filename=None):
        
        if filename is None:
            filename = './'+str(self.id)
        elif filename[-1] == '/':
            filename = os.path.splitext(filename)[0]+str(self.id)
        else:
            filename = os.path.splitext(filename)[0]

        flux = self.data['flux']*10e6 # RESCALE
        zero_loc = np.where(flux == 0.)
        nonzero_loc = np.where(flux != 0.)
        median = np.median(flux[nonzero_loc])
        flux[zero_loc] = median
        flux.astype(np.float32).tofile(filename+'.dat')

        descriptors = np.array([' Data file name without suffix          =  ',
                                ' Telescope used                         =  ',
                                ' Instrument used                        =  ',
                                ' Object being observed                  =  ',
                                ' J2000 Right Ascension (hh:mm:ss.ssss)  =  ',
                                ' J2000 Declination     (dd:mm:ss.ssss)  =  ',
                                ' Data observed by                       =  ',
                                ' Epoch of observation (MJD)             =  ',
                                ' Barycentered?           (1 yes, 0 no)  =  ',
                                ' Number of bins in the time series      =  ',
                                ' Width of each time series bin (sec)    =  ',
                                ' Any breaks in the data? (1 yes, 0 no)  =  ',
                                ' Type of observation (EM band)          =  ',
                                ' Photometric filter used                =  ',
                                ' Field-of-view diameter (arcsec)        =  ',
                                ' Central wavelength (nm)                =  ',
                                ' Bandpass (nm)                          =  ',
                                ' Data analyzed by                       =  ',
                                ' Any additional notes:',
                                '   none'])

        values = np.array([str(self.id), 'TESS', 'unset', str(self.id), 
                           self.ra_hms, self.dec_dms, 'unset', 
                           str(np.min(self.data['bjd'])), '0', 
                           str(len(self.flux)), 
                           (self.exposure_time*self.time_unit).to('s'),
                           '0', 'Optical', 'Other', '180.00', '500.0', '400.0', 
                           'unset', '', ''], 
                          dtype=str)

        inf = np.core.defchararray.add(descriptors, values)
        np.savetxt(filename+'.inf', inf, fmt='%s')

if __name__ == '__main__':
    pass

