def test1():
    import numpy as np
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt

    x = np.linspace(-1,1,100)
    y =  np.linspace(-1,1,100)
    X, Y = np.meshgrid(x,y)

    def f(x, y):
        s = np.hypot(x, y)
        phi = np.arctan2(y, x)
        tau = s + s*(1-s)/5 * np.sin(6*phi) 
        return 5*(1-tau) + tau

    T = f(X, Y)
    # Choose npts random point from the discrete domain of our model function
    npts = 400
    px, py = np.random.choice(x, npts), np.random.choice(y, npts)

    fig, ax = plt.subplots(nrows=2, ncols=2)
    # Plot the model function and the randomly selected sample points
    ax[0,0].contourf(X, Y, T)
    ax[0,0].scatter(px, py, c='k', alpha=0.2, marker='.')
    ax[0,0].set_title('Sample points on f(X,Y)')

    # Interpolate using three different methods and plot
    for i, method in enumerate(('nearest', 'linear', 'cubic')):
        Ti = griddata((px, py), f(px,py), (X, Y), method=method)
        r, c = (i+1) // 2, (i+1) % 2
        ax[r,c].contourf(X, Y, Ti)
        ax[r,c].set_title("method = '{}'".format(method))

    plt.tight_layout()
    plt.show()

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
def test2():
    import matplotlib.pyplot as plt
    import numpy as np
    import sys
    from scipy.interpolate import griddata
    import geopandas as gpd
    import pandas as pd
    from shapely import geometry

    np.set_printoptions(threshold=sys.maxsize)
    pathFileRead = '../out/data/DataIDW/2021-03-07.csv'
    data = pd.read_csv(pathFileRead)
    n = 500
    x = data['Longtitude'].to_numpy()
    y = data['Latitude'].to_numpy()
    z = data['AQI 24h'].to_numpy()
    np.set_printoptions(threshold=sys.maxsize)
    shp = gpd.read_file('../shpHaNoi/QuanHuyen/BacTuLiem.shp')
    polygon = points_from_polygons(shp.geometry)
    boundery = shp.total_bounds
    xi = np.linspace(boundery[0], boundery[2], n)
    yi = np.linspace(boundery[1], boundery[3], n)
    
    xi, yi = np.meshgrid(xi, yi)
    xi, yi = xi.flatten(), yi.flatten()

    bounderyX = np.array([])
    bounderyY = np.array([])
    line = geometry.LineString(polygon)

    for indexXi,indexYi in zip(xi,yi):
        point = geometry.Point(indexXi, indexYi)
        polygon = geometry.Polygon(line)
        if polygon.contains(point):
            pass
        else:
            bounderyX = np.append(bounderyX,indexXi)
            bounderyY = np.append(bounderyY,indexYi)
    kitX = np.array([])
    kitY = np.array([])
    kitZ = np.array([])
    polygon = points_from_polygons(shp.geometry)
    line = geometry.LineString(polygon)
    for indexX,indexY,indexZ in zip(x,y,z):
        point = geometry.Point(indexX, indexY)
        polygon = geometry.Polygon(line)
        if polygon.contains(point):
            kitX = np.append(kitX,indexX)
            kitY = np.append(kitY,indexY)
            kitZ = np.append(kitZ,indexZ)
    # set mask
    mask = (xi > 0.5) & (xi < 0.6) & (yi > 0.5) & (yi < 0.6)

    # interpolate
    zi = griddata((kitX,kitY),kitZ,(xi,yi),method='linear')

    # mask out the field
    zi[(bounderyX,bounderyY)] = np.nan

    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.contourf(xi,yi,zi,np.arange(0,1.01,0.01))
    plt.plot(x,y,'k.')
    plt.xlabel('xi',fontsize=16)
    plt.ylabel('yi',fontsize=16)
    # plt.savefig('interpolated.png',dpi=100)
    # # plt.close(fig)
    plt.show()

test2()