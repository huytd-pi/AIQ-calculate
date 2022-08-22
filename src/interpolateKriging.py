import numpy as np
from pykrige.ok import OrdinaryKriging
from pykrige.uk import UniversalKriging
from shapely.geometry import MultiPolygon
from shapely.geometry.polygon import Polygon
from shapely.ops import unary_union
from descartes import PolygonPatch
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import geopandas as gpd
import shapefile as shp
import glob
from shapely.geometry import Point




def OK(x, y, z, n,shp):  # https://geostat-framework.readthedocs.io/projects/pykrige/en/stable/generated/pykrige.ok.OrdinaryKriging.html
	#tao grid tu x, y
    boundery = shp.total_bounds
    xi = np.linspace(boundery[0], boundery[2], n)
    yi = np.linspace(boundery[1], boundery[3], n)
	#noi suy
	
    OK = OrdinaryKriging(
		x,
		y,
		z,
		variogram_model="spherical",
		variogram_parameters=None,
		variogram_function=None,
		nlags=6,
		weight=False,
		anisotropy_scaling=1.0,
		anisotropy_angle=0.0,
		verbose=False,
		enable_plotting=False,
		enable_statistics=False,
		coordinates_type="geographic",
		exact_values=True,
		pseudo_inv=True,
		pseudo_inv_type="pinv2",
	)
    grid, ss = OK.execute("grid", xi, yi)
    return grid


def OK_zone(x, y, z, n, shp):  # https://geostat-framework.readthedocs.io/projects/pykrige/en/stable/generated/pykrige.ok.OrdinaryKriging.html
	#tao grid tu x, y
    boundery = shp.total_bounds
    xi = np.linspace(boundery[0], boundery[2], n)
    yi = np.linspace(boundery[1], boundery[3], n)
    #noi suy
    kitX = np.array([])
    kitY = np.array([])
    kitZ = np.array([])
    flag = False
    polygon = Polygon(points_from_polygons(shp.geometry))
    for indexX, indexY, indexZ in zip(x, y, z):
        point = Point(indexX, indexY)
        if polygon.contains(point):
            kitX = np.append(kitX, indexX)
            kitY = np.append(kitY, indexY)
            kitZ = np.append(kitZ, indexZ)
            flag = True
    OK = OrdinaryKriging(
        kitX,
        kitY,
        kitZ,
        variogram_model="spherical",
        variogram_parameters=None,
        variogram_function=None,
        nlags=6,
        weight=False,
        anisotropy_scaling=1.0,
        anisotropy_angle=0.0,
        verbose=False,
        enable_plotting=False,
        enable_statistics=False,
        coordinates_type="geographic",
        exact_values=True,
        pseudo_inv=True,
        pseudo_inv_type="pinv2",
    )
    grid, ss = OK.execute("grid", xi, yi)
    return grid, kitX, kitY, kitZ,flag

def UK(x, y, z, n,shp):
	#tao grid tu x, y
    boundery = shp.total_bounds
    xi = np.linspace(boundery[0], boundery[2], n)
    yi = np.linspace(boundery[1], boundery[3], n)
	#noi suy
    UK = UniversalKriging(
		x,
		y,
		z,
		variogram_model="linear",
		variogram_parameters=None,
		variogram_function=None,
		nlags=6,
		weight=False,
		anisotropy_scaling=1.0,
		anisotropy_angle=0.0,
		drift_terms=None,
		point_drift=None,
		external_drift=None,
		external_drift_x=None,
		external_drift_y=None,
		specified_drift=None,
		functional_drift=None,
		verbose=False,
		enable_plotting=False,
		exact_values=True,
		pseudo_inv=False,
		pseudo_inv_type="pinv",
	)
    grid, ss = UK.execute("grid", xi, yi)
    return grid


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

def createbuffer(x, y, shp, im, axs):
    polygon1 = Polygon(points_from_polygons(shp.geometry))

    polygons = []
    polygons.append(polygon1)
    unary = unary_union(polygons)
    patch = PolygonPatch(unary, alpha=0.8, fill=False)
    axs.add_patch(patch)
    im.set_clip_path(patch)


def InterpolateByZoneHN(pathFileRead, yymmdd):
    sizevalue = 500
    colorkit = "white"
    colorkitdata = "blue"

    cmaps = LinearSegmentedColormap.from_list("mycmap",
                                              [
                                                  (000/sizevalue, "lime"),
                                                  (100/sizevalue, "yellow"),
                                                  (150/sizevalue, "darkorange"),
                                                  (200/sizevalue, "red"),
                                                  (300/sizevalue, "darkorchid"),
                                                  (500/sizevalue, "maroon")
                                              ])
    fig, axs = plt.subplots(figsize=(9, 9))
    plt.title(str(yymmdd))

    # pathFileRead = '../out/data/DataIDW/2021-03-09.csv'
    data = pd.read_csv(pathFileRead)
    n = 500
    x = data['Longtitude'].to_numpy()
    y = data['Latitude'].to_numpy()
    z = data['AQI 24h'].to_numpy()
    id = data['Kit ID'].to_numpy()
    shpHN = gpd.read_file('../shpHaNoi/HaNoi_1.shp')
    informationKitID = pd.read_csv('../out/locationFairKit.csv')
    latitude = informationKitID['Latitude']
    longtitude = informationKitID['Longitude']
    # gridIDW = OK(x, y, z, n, shpHN)
    gridIDW = UK(x, y, z, n, shpHN)
    boundery = shpHN.total_bounds
    #import grid
    im = plt.imshow(gridIDW,
                    #interpolation= 'sinc',
                    cmap=cmaps,
                    extent=(boundery[0], boundery[2],
                            boundery[1], boundery[3]),
                    vmin=0,
                    vmax=sizevalue,
                    origin="lower",
                    )  # , vmin=0, vmax = 500
    #hien thi cac tram thu
    plt.scatter(longtitude,
                latitude,
                c=colorkit)
    #hien thi cac tam co du lieu
    plt.scatter(x,
                y,
                c=colorkitdata,  # z,
                #cmap = cmaps,
                vmin=0,
                vmax=500
                )
    #vmin = 0,vmax = 500

    plt.colorbar(im)  # color bar

    #Tao buffer - vung dem
    createbuffer(x, y, shpHN, im, axs)
    # plt.show()
    pathsave = '../out/image/UK/' + str(yymmdd) + '.png'
    fig.savefig(pathsave)
    # del pathFileRead
    # gc.collect()


def InterpolateByZone(pathFileRead, yymmdd):
    sizevalue = 500
    colorkit = "white"
    colorkitdata = "blue"

    cmaps = LinearSegmentedColormap.from_list("mycmap",
                                              [
                                                  (000/sizevalue, "lime"),
                                                  (100/sizevalue, "yellow"),
                                                  (150/sizevalue, "darkorange"),
                                                  (200/sizevalue, "red"),
                                                  (300/sizevalue, "darkorchid"),
                                                  (500/sizevalue, "maroon")
                                              ])
    fig, axs = plt.subplots(figsize=(9, 9))
    plt.title(str(yymmdd))

    # pathFileRead = '../out/data/DataIDW/2021-03-09.csv'
    data = pd.read_csv(pathFileRead)
    n = 500
    x = data['Longtitude'].to_numpy()
    y = data['Latitude'].to_numpy()
    z = data['AQI 24h'].to_numpy()
    id = data['Kit ID'].to_numpy()
    shpFile = glob.glob('../shpHaNoi/QuanHuyen/*.shp')
    informationKitID = pd.read_csv('../out/locationFairKit.csv')
    latitude = informationKitID['Latitude']
    longtitude = informationKitID['Longitude']
    #hien thi cac tram thu
    plt.scatter(longtitude,
                latitude,
                c=colorkit)
    for index in range(len(shpFile)):
        shp1 = gpd.read_file(shpFile[index])
        sf = shp.Reader(shpFile[index])
        gridIDW, kitX, kitY, kitZ, flag = OK_zone(x, y, z, n, shp1)
        im = plt.imshow(gridIDW,
                        #interpolation= 'sinc',
                        cmap=cmaps,
                        extent=(105.72, 106.025, 20.77, 21.22),
                        vmin=0,
                        vmax=sizevalue,
                        origin="lower",
                        )  # , vmin=0, vmax = 500
        # plt.show()

        #hien thi cac tam co du lieu
        plt.scatter(kitX,
                    kitY,
                    c=colorkitdata,  # z,
                    #cmap = cmaps,
                    vmin=0,
                    vmax=500)
        #vmin = 0,vmax = 500
        if flag == False:
            for shape in sf.shapeRecords():
                xPoly = [i[0] for i in shape.shape.points[:]]
                yPoly = [i[1] for i in shape.shape.points[:]]
                plt.plot(xPoly, yPoly, color='k')
                plt.fill(xPoly, yPoly, color='w')
        createbuffer(x, y, shp1, im, axs)
        # del shp1
        # del sf
        # gc.collect()
    plt.colorbar(im)  # color bar
    # plt.show()
    pathsave = '../out/image/OK/zone/' + str(yymmdd) + '.png'
    fig.savefig(pathsave)
    # del pathFileRead
    # gc.collect()
