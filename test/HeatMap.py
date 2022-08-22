import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
import matplotlib as mpl

# parameters
n = 250                     # number of points
lat0 = 40.7                 # coordinates will be generated uniformly with
lon0 = -73.9                # lat0 - eps <= lat < lat0 + eps
eps = 0.1                   # lon0 - eps <= lon < lon0 + eps
v_min, v_max = 0, 100       # min, max values

# generating values
lat = np.random.uniform(lat0 - eps, lat0 + eps, n)
lon = np.random.uniform(lon0 - eps, lon0 + eps, n)
value = np.random.uniform(v_min, v_max, n)
df = pd.DataFrame({'lat': lat, 'lon': lon, 'value': value})

# to demonstrate the effect of weights on the heatmap,
# we'll divide values below the center of the box by K = 5
K = 5
df.loc[df['lat'] < lat0, 'value'] /= K

# plotting the map, both the points themselves and the heatmap
m = folium.Map(location = [lat0, lon0], tiles="OpenStreetMap",
               zoom_start=11, width=400, height=400)
for elt in list(zip(df.lat, df.lon, df.value)):
    folium.Circle(elt[:2], color="white", radius=elt[2]).add_to(m)

# df.values used here is a (250, 3) numpy.ndarray
# with (lat, lon, weight) for each data point
HeatMap(data=df.values, min_opacity=0.1).add_to(m)
