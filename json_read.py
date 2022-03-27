import json
import array
import requests
import pandas as pd

acc_url_averageByHour = "http://api2.fairnet.vn/data/averageByHour?KitID=1037&start=1609459200000&finish=1625097600000"
acc_url_averageByDay = "http://api2.fairnet.vn/data/averageByDay?KitID=1037&start=1609459200000&finish=1625097600000"

def loadAPI():
    jsonFile = open('FAirKit.json')

    dataJsonFile = json.load(jsonFile)

    kitID = []
    for d in dataJsonFile:
        kitID.append(d['KitID'])

    for i in kitID:
        fileNameAverageByDay = "dataFairnet_averageByDay_KitID" + str(i) + ".txt"
        fileNameAverageByHour = "dataFairnet_averageByHour_KitID" + str(i) + ".txt"

        fileDataAverageByDay = open(fileNameAverageByDay,'w')
        fileDataAverageByHour = open(fileNameAverageByHour,'w')
        
        fileDataAverageByDay.write(requests.get(acc_url_averageByDay).text)
        fileDataAverageByHour.write(requests.get(acc_url_averageByHour).text)

        fileDataAverageByDay.close()
        fileDataAverageByHour.close()

        # print(dataJsonFile)

        # format json file write 
        # dataFormat = (json.dumps(dataJsonFile,indent = 4,sort_keys=True,ensure_ascii=False).encode('utf8')).decode()
        # with open("FAirKitFormat.json", "w") as outfile:
        #     outfile.write(dataFormat)
    jsonFile.close()

def formatTextToCSV():
    jsonFile = open('FAirKit.json')

    dataJsonFile = json.load(jsonFile)

    kitID = []
    for d in dataJsonFile:
        kitID.append(d['KitID'])

    for i in kitID:
        # DataAverageByDay
        # textFileName = 'DataAverageByDay/dataFairnet_averageByDay_KitID' + str(i) +'.txt'
        # csvFileName = 'DataAverageByDay/dataFairnet_averageByDay_KitID' + str(i) +'.csv'

        # DataAverageByHour
        textFileName = 'DataAverageByHour/dataFairnet_averageByHour_KitID' + str(i) +'.txt'
        csvFileName = 'DataAverageByHour/dataFairnet_averageByHour_KitID' + str(i) +'.csv'

        csvFile = pd.read_csv(textFileName,delimiter =',',engine='python')

        # csvFile.columns['Time','PM1','PM2.5','PM10','Temperature','Humidity','CO']
        csvFile.to_csv(csvFileName,index=None)

formatTextToCSV()