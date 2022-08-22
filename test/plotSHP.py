import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

shp = gpd.read_file(
    '../shpHaNoi/vnm_adm_gov_20201027_shp/vnm_admbnda_adm1_gov_20201027.shp')
point = gpd.read_file(
    '../shpHaNoi/locationFairKit-point.shp', encoding='latin1')

ax = shp.plot()
# point.plot(axes=ax, color='red')
plt.show()