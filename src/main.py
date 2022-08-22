from AQICalculation import AQI_Aggregate,AQI
from ReadCSV import ReadDataAverageByDay,ReadDataAverageByHour
import matplotlib.pyplot as plt
import numpy as np
import re
import json
import pandas as pd
# import csv_to_point_shapefile as shp
import execnet
import geopandas as gpd
import shapefile as shp
from ExportAQI import AQIExportCSV
import os
import multiprocessing

def call_python_version(Version, Module, Function, ArgumentList):
    gw      = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec("""
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
    """ % (Module, Function))
    channel.send(ArgumentList)
    return channel.receive()

def plot(self):
    plt.figure()
    plt.subplot(221)
    plt.plot(self.PM2_5_AQI,'r',marker = 'o')
    plt.title('PM2.5')

    plt.subplot(222)
    plt.plot(self.PM10_AQI, 'g',marker = '*' )
    plt.title('PM10')

    plt.subplot(223)
    plt.plot(self.CO_AQI, 'b',marker = '.' )
    plt.title('CO')

    plt.subplot(224)
    plt.plot(self.AQI_1h,'y',marker = '+')
    plt.title('AQI')
    plt.show()
    pass

def plot_file_shp():
    hanoi = gpd.read_file('../shpHaNoi/HaNoi_2.shp',encoding='latin1')
    point = gpd.read_file('../shpHaNoi/locationFairKit-point.shp',encoding='latin1')
    ax = point.plot(color='red',markersize=2)
    hanoi.boundary.plot(axes=ax,linewidth=0.5)
    plt.show()

def shapefile_location_export(pathJsonFile):
    data = pd.read_csv(pathJsonFile,encoding='utf-8')
    kitID = data['KitID']
    address = data['Address']
    location = data['Location']
    name = data['Name']
    outdoor = data['outdoor']
    latitude = np.array([])
    longitude = np.array([])
    for i in location:
        temp = i.replace('[',', ').replace(']',', ').split(', ')
        latitude = np.append(latitude,temp[1])
        longitude = np.append(longitude,temp[2])

    dict = {'Kit ID':kitID,'Địa chỉ':address,'Tên':name,'Latitude':latitude,'Longitude':longitude,'outdoor':outdoor}
    df = pd.DataFrame(dict)
    df.to_csv('../out/locationFairKit.csv',encoding='utf-8')
    result = call_python_version("2.7", "csv_to_point_shapefile", "ExportShapeFile",  
                             ['../out/locationFairKit.csv', '../out/locationFairKit.shp']) 
    

def main():

    pass
        
        
def calculationData():
    # printing main program process id
    print("ID of main process: {}".format(os.getpid()))
    ImportKitID = AQIExportCSV('../out/locationFairKit.csv')
    # creating processes
    p1 = multiprocessing.Process(target=ImportKitID.averageByDay)
    p2 = multiprocessing.Process(target=ImportKitID.averageByHour)
    # starting processes
    p1.start()
    p2.start()
  
    # process IDs
    print("ID of process p1: {}".format(p1.pid))
    print("ID of process p2: {}".format(p2.pid))
  
    # wait until processes are finished
    p1.join()
    p2.join()
  
    # both processes finished
    print("Both processes finished execution!")
  
    # check if processes are alive
    print("Process p1 is alive: {}".format(p1.is_alive()))
    print("Process p2 is alive: {}".format(p2.is_alive()))

if __name__ == "__main__":

    calculationData()
