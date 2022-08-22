import pandas as pd 
import geopandas as gpd

def ExportShapeFile(dataPathCSV,dataSHP):
    # Read the .csv file using Pandas 
    dataCSV = pd.read_csv(dataPathCSV,encoding='utf-8')
    airport_data = dataCSV

    # Creating GeoPandas GeoDataFrame using the Pandas Dataframe 
    airport_gdf = gpd.GeoDataFrame(airport_data, geometry = gpd.points_from_xy(airport_data['Longtitude'],airport_data['Latitude'] ))

    # Obtain the ESRI WKT
    ESRI_WKT = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'

    # Save the file as an ESRI Shapefile
    airport_gdf.to_file(filename = dataSHP, driver = 'ESRI Shapefile', crs_wkt = ESRI_WKT,encoding='utf-8')

datayymmdd = pd.read_csv('../out/yymmdd.csv')
for yymmdd in datayymmdd['yymmdd']:
    pathFileRead = '../out/data/DataIDW/' + str(yymmdd) + '.csv'
    pathFileSave = '../out/data/DataIDW/' + str(yymmdd) + '.shp'

    ExportShapeFile(pathFileRead,pathFileSave)