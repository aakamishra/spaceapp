from astroquery.jplhorizons import conf
conf.horizons_server = 'https://ssd.jpl.nasa.gov/horizons_batch.cgi'
import numpy as np
import astropy.io.fits as fits
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.wcs import WCS
from astroquery.jplhorizons import conf,Horizons
conf.horizons_server = 'https://ssd.jpl.nasa.gov/horizons_batch.cgi'
import urllib

def locate(name):
	Davis = {'lon': -121.7405,'lat': 38.5449,'elevation': 0.0158}
	eph = Horizons(id=name, location = Davis).ephemerides()
	azi, elev = eph['AZ'][0],eph['EL'][0]
	return azi,elev

