# import the pyidw package.
from pyidw import idw

# import mean_squared_error from scikit-learn for using with accuracy assessment functions. 
from sklearn.metrics import mean_squared_error

# import other libraries for data opening and visualization, 
# importing these are not essential for core pyidw functionalities.
import geopandas as gpd
import rasterio
from matplotlib import pyplot as plt

# point_file = gpd.read_file('../shpHaNoi/locationFairKit-point.shp',encoding='latin1')
gdf = gpd.read_file('../out/data/DataIDW/2021-01-01.shp',encoding='latin1')
bd = gpd.read_file('../shpHaNoi/HaNoi_2.shp',encoding='latin1')

# fig, ax = plt.subplots(figsize=(10,9))
# bd.plot(ax=ax, color='c')
# gdf.plot(ax=ax, marker='D', color='r')
# plt.show()

idw.idw_interpolation(
    bd,
    gdf,
    column_name="Max_Temp",
    power=2,
    search_radious=10,
    output_resolution=250,
)