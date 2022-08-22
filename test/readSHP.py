import geopandas as gpd
import pandas as pd
from matplotlib import path
import matplotlib.pyplot as plt
import numpy as np
import fiona
from shapely.geometry import shape
import numpy as np
# from osgeo import ogr
from shapely.geometry import MultiPolygon
def points_from_polygons(polygons):
    points = []
    for mpoly in polygons:
        if isinstance(mpoly, MultiPolygon):
            polys = list(mpoly)
        else:
            polys = [mpoly]
        for polygon in polys:
            for point in polygon.exterior.coords:
                points.append(point)
            for interior in polygon.interiors:
                for point in interior.coords:
                    points.append(point)
    return points
def main():
    pd.set_option('display.max_columns',None)
    shx = gpd.read_file('../shpHaNoi/QuanHuyen/CauGiay.shx',encoding='utf-8')
    shp = gpd.read_file('../shpHaNoi/QuanHuyen/CauGiay.shp',encoding='utf-8')
    print(shp)

def check_point_in_polygon():
    first = -3
    size  = (3-first)/100
    xv,yv = np.meshgrid(np.linspace(-3,3,100),np.linspace(-3,3,100))
    p = path.Path([(0,0), (0, 1), (1, 1), (1, 0)])  # square with legs length 1 and bottom left corner at the origin
    flags = p.contains_points(np.hstack((xv.flatten()[:,np.newaxis],yv.flatten()[:,np.newaxis])))
    grid = np.zeros((101,101),dtype='bool')
    grid[((xv.flatten()-first)/size).astype('int'),((yv.flatten()-first)/size).astype('int')] = flags

    xi,yi = np.random.randint(-300,300,100)/100,np.random.randint(-300,300,100)/100
    vflag = grid[((xi-first)/size).astype('int'),((yi-first)/size).astype('int')]
    plt.imshow(grid.T,origin='lower',interpolation='nearest',cmap='binary')
    plt.scatter(((xi-first)/size).astype('int'),((yi-first)/size).astype('int'),c=vflag,cmap='Greens',s=90)
def shape_lat_lon():
    ds = ogr.Open("../shpHaNoi/QuanHuyen/CauGiay.shp")
    lyr = ds.GetLayerByName("mn_counties")

    lyr.ResetReading()

    for feat in lyr:
        # get bounding coords in minx, maxx, miny, maxy format
        env = feat.GetGeometryRef().GetEnvelope()
        # get bounding coords in minx, miny, maxx, maxy format
        bbox = [env[0], env[2], env[1], env[3]]
        print (env)
        print (bbox)
        print
main()