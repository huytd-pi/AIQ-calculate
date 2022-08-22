import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import geopandas as gpd
from matplotlib_scalebar.scalebar import ScaleBar
from shapely.geometry import Point
from shapely.ops import unary_union
from descartes import PolygonPatch
from scipy.interpolate import griddata
from matplotlib import path
from shapely import geometry
import sys
from shapely.geometry.polygon import Polygon
import glob
import shapefile as shp
import gc

def simple_idw(x, y, z, xi, yi):
    dist = distance_matrix(x,y, xi,yi)

    # In IDW, weights are 1 / distance
    weights = 1.0 / dist

    # Make weights sum to one
    weights /= weights.sum(axis=0)

    # Multiply the weights for each interpolated point by all observed Z-values
    zi = np.dot(weights.T, z)
    return zi

def linear_rbf(x, y, z, xi, yi):
    dist = distance_matrix(x,y, xi,yi)

    # Mutual pariwise distances between observations
    internal_dist = distance_matrix(x,y, x,y)

    # Now solve for the weights such that mistfit at the observations is minimized
    weights = np.linalg.solve(internal_dist, z)

    # Multiply the weights for each interpolated point by the distances
    zi =  np.dot(dist.T, weights)
    return zi
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

def scipy_idw(x, y, z, id,n,shp):
    # xi yi generate two arrays of evenly space data between ends of previous arrays
    boundery = shp.total_bounds
    xi = np.linspace(boundery[0], boundery[2], n)
    yi = np.linspace(boundery[1], boundery[3], n)
    
    xi, yi = np.meshgrid(xi, yi)
    xi, yi = xi.flatten(), yi.flatten()

    # bounderyX = np.array([])
    # bounderyY = np.array([])
    # line = geometry.LineString(polygon)

    # for indexXi,indexYi in zip(xi,yi):
    #     point = geometry.Point(indexXi, indexYi)
    #     polygon = geometry.Polygon(line)
    #     if polygon.contains(point):
    #         bounderyX = np.append(bounderyX,indexXi)
    #         bounderyY = np.append(bounderyY,indexYi)
    #     else:
    #         bounderyX = np.append(bounderyX,np.nan)
    #         bounderyY = np.append(bounderyY,np.nan)
    # print(x,y)
    kitX = np.array([])
    kitY = np.array([])
    kitZ = np.array([])
    flag = False
    polygon = Polygon(points_from_polygons(shp.geometry))
    # print(shp['VARNAME_2'])
    for indexX,indexY,indexZ,indexID in zip(x,y,z,id):
        # print(indexX,indexY)
        point = Point(indexX, indexY)
        if polygon.contains(point):
            kitX = np.append(kitX,indexX)
            kitY = np.append(kitY,indexY)
            kitZ = np.append(kitZ,indexZ)
            flag = True
            # print(indexID)

    interp =    simple_idw(kitX,kitY,kitZ,xi,yi).reshape(n,n)
    return interp,kitX,kitY,kitZ,flag
    

def distance_matrix(x0, y0, x1, y1):
    obs = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T

    # Make a distance matrix between pairwise observations
    # Note: from <http://stackoverflow.com/questions/1871536>
    # (Yay for ufuncs!)
    d0 = np.subtract.outer(obs[:,0], interp[:,0])
    d1 = np.subtract.outer(obs[:,1], interp[:,1])

    return np.hypot(d0, d1)


def createbuffer(x, y, shp,im, axs):
    polygon1 = Polygon(points_from_polygons(shp.geometry))

    polygons = []
    polygons.append(polygon1)
    unary = unary_union(polygons)
    patch = PolygonPatch(unary, alpha=0.8, fill=False)
    axs.add_patch(patch)
    im.set_clip_path(patch)

def plot(x,y,z, grid, shp, save = False):
	#set color
	sizevalue = 500
	colorkit = "white"
	colorkitdata = "blue"
	
	cmaps = LinearSegmentedColormap.from_list(  "mycmap", 
												[
													(000/sizevalue, "lime"      ),
													(100/sizevalue, "yellow"    ),
													(150/sizevalue, "darkorange"),
													(200/sizevalue, "red"       ),
													(300/sizevalue, "darkorchid"),
													(500/sizevalue, "maroon"    )
													]
												)
	#set plot
	#fig = plt.figure(figsize=(15,9))
	#axs = plt.axes()Polygon
	# shp.plot(ax = axs, alpha = 0.2, color = 'white', edgecolor='black')
	#axs.add_collection(shp)

	#scale bar
	scalebar = ScaleBar(0.2) # 1 pixel = 0.2 meter
	plt.gca().add_artist(scalebar)

	#import grid
	im = plt.imshow(grid,
					#interpolation= 'sinc',
					cmap    = cmaps,
					extent  = (105.644, 106.025, 20.84, 21.24),
					vmin    = 0, 
					vmax    = sizevalue,
					origin 	= "lower",
		)#, vmin=0, vmax = 500
	#hien thi cac tram thu
	informationKitID = pd.read_csv('../out/locationFairKit.csv')
	latitude = informationKitID['Latitude']
	longtitude = informationKitID['Longitude']
	plt.scatter(longtitude,
				latitude,
				c = colorkit
		)
	#hien thi cac tam co du lieu
	plt.scatter(x,
				y,
				c = colorkitdata,#z, 
				#cmap = cmaps,
				vmin = 0, 
				vmax = 500
		)
				#vmin = 0,vmax = 500
	
	plt.colorbar(im)#color bar
	
	#Tao buffer - vung dem
	createbuffer(x,y,shp,im, axs)
	# InterpolateByZone(im, axs)
	#save
	# if save == True:
	# 	pathsave = '../out/image/'+title+'.png'
	# 	fig.savefig(pathsave)
    
def test_IDW():
    np.set_printoptions(threshold=sys.maxsize)
    pathFileRead = '../out/data/DataIDW/2021-03-07.csv'
    data = pd.read_csv(pathFileRead)
    n = 500
    x = data['Longtitude'].to_numpy()
    y = data['Latitude'].to_numpy()
    z = data['AQI 24h'].to_numpy()
    gridIDW,kitX,kitY,kitZ = scipy_idw(x, y, z, n)
    plot(kitX, kitY, kitZ, gridIDW, 'IDW2021-01-01', save = False)
    plt.show()

# pathFileRead = '../out/data/DataIDW/2021-03-09.csv'
def InterpolateByZone(pathFileRead,yymmdd):
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
        gridIDW, kitX, kitY, kitZ,flag = scipy_idw(x, y, z,id, n,shp1)
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
        createbuffer(x,y,shp1,im, axs)
        # del shp1
        # del sf
        # gc.collect()
    plt.colorbar(im)  # color bar
    # plt.show()
    pathsave = '../out/image/zone/'+ str(yymmdd) + '.png'
    fig.savefig(pathsave)
    # del pathFileRead
    # gc.collect()
        
if __name__ == '__main__':
    # InterpolateByZone(pathFileRead, str(pathFileRead))
    pass
