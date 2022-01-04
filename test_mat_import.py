import scipy.io as sio
import numpy as np
import pandas as pd



def getMicData(filename):
    given_data_txt = pd.read_csv(filename, delimiter=",", encoding="utf8")

    time_column = given_data_txt.columns[0]
    mic_columns = given_data_txt.columns[1:]

    fs = 1/ (float(given_data_txt[time_column][1].split(" ")[0]) - float(given_data_txt[time_column][0].split(" ")[0]))
    mic_data = given_data_txt[mic_columns].to_numpy()

    return fs, mic_data

if __name__ == '__main__':
    
    if 1:
        fname = "S19_VT_60.txt"

    else: 
        fname = "S19_VT_15.txt"
    
    
    fs, data = getMicData(fname)

    print(f"fs = {fs}")
    print(f"data shape = {np.shape(data)}")