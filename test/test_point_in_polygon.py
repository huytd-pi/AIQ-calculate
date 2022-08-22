from shapely.geometry import MultiPolygon
import numpy as np
from shapely import geometry
import pandas as pd
import geopandas as gpd
import glob
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

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


def check_point(x, y, z, id, n, shp):
    kitX = np.array([])
    kitY = np.array([])
    kitZ = np.array([])
    flag = False
    polygon = points_from_polygons(shp.geometry)
    line = geometry.LineString(polygon)
    for indexX, indexY, indexZ, indexID in zip(x, y, z, id):
        point = geometry.Point(indexX, indexY)
        polygon = geometry.Polygon(line)
        if polygon.contains(point):
            kitX = np.append(kitX, indexX)
            kitY = np.append(kitY, indexY)
            kitZ = np.append(kitZ, indexZ)
            flag = True
            print(indexID)
    print('--------------------------------------')


pathFileRead = '../out/data/DataIDW/2021-01-01.csv'
data = pd.read_csv(pathFileRead)
n = 500
x = data['Longtitude'].to_numpy()
y = data['Latitude'].to_numpy()
z = data['AQI 24h'].to_numpy()
id = data['Kit ID'].to_numpy()
# shp = gpd.read_file('../shpHaNoi/QuanHuyen/BacTuLiem.shp')
shpFile = glob.glob('../shpHaNoi/QuanHuyen/*.shp')
for index in range(len(shpFile)):
    shp = gpd.read_file(shpFile[index])
    polygon = Polygon(points_from_polygons(shp.geometry))
    print(shp['VARNAME_2'])
    for indexX,indexY,indexID in zip(x,y,id):
        point = Point(indexX,indexY)
        if polygon.contains(point):
            print(indexID)
