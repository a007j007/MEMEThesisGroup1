import scipy.io as sio
import numpy as np
import pandas as pd



if 1:
    given_data_txt = pd.read_csv("S19_VT_60.txt",delimiter=",", encoding="utf8")

else: 
    given_data_txt = pd.read_csv("S19_VT_15.txt",delimiter=",", encoding="utf8")

# print(f"given_data_txt = \n{given_data_txt}")


# time = given_data_txt["Time"]


# print(f"given data time = \n{ time }")


# fs = float(time[1].split(" ")[0]) - float(time[0].split(" ")[0])
# print(f"fs = {fs}")



mics = given_data_txt.columns[1:]
print(mics)

data = given_data_txt[mics].to_numpy()



# for i, _ in enumerate(data):
#     data[i][0] = float(data[i][0].split(" ")[0])