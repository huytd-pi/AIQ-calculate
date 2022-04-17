import numpy as np
import pandas as pd

dataCSV = pd.read_csv('DataAverageByHour/dataFairnet_averageByHour_KitID1037.csv')

CO          = dataCSV['CO']
CO          = CO.to_numpy()
CO          = np.delete(CO,         [len(CO)-1,len(CO)-2,len(CO)-3,len(CO)-4,len(CO)-5])

print(dataCSV)