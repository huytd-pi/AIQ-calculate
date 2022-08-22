from itertools import product
from scipy.sparse import dok_matrix
import numpy as np

# https://pcjericks.github.io/py-gdalogr-cookbook
from osgeo import ogr

# DATA:
# http://www.naturalearthdata.com/downloads/110m-cultural-vectors/

SHP_FNAME = '../shpHaNoi/QuanHuyen/CauGiay.shp'

driver = ogr.GetDriverByName('ESRI Shapefile')
data = driver.Open(SHP_FNAME, 0)
layer = data.GetLayer()

XDIAM = 360.0
YDIAM = 180.0
XRES = YRES = 10 ** 2
dX = XDIAM / XRES
dY = YDIAM / YRES

def to_key(pt):
    x, y = pt
    x -= x % dX - XDIAM / 2
    y -= y % dY - YDIAM / 2
    return (x / dX, y / dY)

def geom_to_keys(g):
    xmin, xmax, ymin, ymax = g.GetEnvelope()
    print (xmax, ymax, xmin, ymin)
    xs = np.linspace(xmin, xmax, (xmax - xmin) / dX)
    ys = np.linspace(ymin, ymax, (ymax - ymin) / dY)
    for x, y in product(xs, ys):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(x, y)
        if g.Contains(point):
            yield to_key((x, y))

smatrix = dok_matrix((XRES + 1, YRES + 1), np.int8)

one = np.int8(1)

for feature in layer:
    geom = feature.GetGeometryRef()
    if geom.Area() > 1000:
        continue
        # sampling is slow for large polygons

    for key in geom_to_keys(geom):
        smatrix.update({
            key : one,
            })

if XRES * YRES < 10 ** 6 + 1:
    from matplotlib import pyplot as plt
    plt.pcolor(smatrix.toarray().transpose(),edgecolors ='k', linewidths = 1)
    plt.show()