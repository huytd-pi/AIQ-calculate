import rasterio
import numpy as np
from affine import Affine
from pyproj import Proj, transform
import sys
np.set_printoptions(threshold=sys.maxsize)

fname = '../NDVI/LC08_L1TP_20210514_20210524_01_T1_NDVI_cut_HN_resize.tif'

# Read raster
with rasterio.open(fname) as r:
    T0 = r.transform  # upper-left pixel corner affine transform
    p1 = Proj(r.crs)
    A = r.read()  # pixel values

# All rows and columns
cols, rows = np.meshgrid(np.arange(A.shape[2]), np.arange(A.shape[1]))

# Get affine transform for pixel centres
T1 = T0 * Affine.translation(0.5, 0.5)
# Function to convert pixel row/column index (from 0) to easting/northing at centre
def rc2en(r, c): return (c, r) * T1


# All eastings and northings (there is probably a faster way to do this)
eastings, northings = np.vectorize(rc2en, otypes=[float, float])(rows, cols)

# Project all longitudes, latitudes
p2 = Proj(proj='latlong', datum='WGS84')
longs, lats = transform(p1, p2, eastings, northings)

print(A)
