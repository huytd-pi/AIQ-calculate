# Python program to solve JSONDecodeError: Expecting value: line 1 column 1 (char 0)
from email import header
import requests, json
import pandas as pd
file = open("dataFairnet_averageByDay.txt","w")
# acc_url = "http://api2.fairnet.vn/data/averageByHour?KitID=1037&start=1609459200000&finish=1625097600000"
acc_url = "http://api2.fairnet.vn/data/averageByDay?KitID=1037&start=1609459200000&finish=1625097600000"
acc_info = requests.get(acc_url).text
file.write(acc_info)
file.close

