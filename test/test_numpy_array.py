import numpy as np
# NumPy Array
# numpyArr = np.arange(0,200,1)
# print(len(numpyArr))
# for i in range(0,len(numpyArr)-24,24):
#     # print("i = ",i)
#     temp = numpyArr[i:i+24]
#     print(temp)
#     print(np.max(temp))


# 1D array 
arr = [np.nan, np.nan, np.nan, np.nan, np.nan]
print("arr : ", arr) 
print("max of arr : ", np.amax(arr))
  
# nanmax ignores NaN values. 
print("nanmax of arr : ", np.nanmax(arr))