from numpy import (
    append,
    arange,
    argmax,
    array,
    isscalar,
    mean,
    transpose,
    zeros
    )

from scipy.signal import (
    correlate,
    correlation_lags
    )

from pandas import read_csv

from math import tan

###############################################################################

def constructPairs(input_list):
    '''Returns a list of unique pairs and its length
       generates a list of pairs of the inputs and returns this list along
       with the length of the list'''
    if isscalar(input_list):
        amntItems = input_list
        input_list = transpose(arange(input_list))
    else:
        amntItems = len(input_list)

    paircount = int(amntItems*(amntItems-1)/2)
    
    pairs = zeros((paircount, 2))
    
    cntr = 0
    for i in range(amntItems):
        for j in range(i+1, amntItems):
            pairs[cntr] = array([input_list[i], input_list[j]])
            cntr = cntr + 1

    return pairs.astype(int), paircount

###############################################################################

def getLag (sigOne, sigTwo, fs):
    correlation = correlate(sigOne, sigTwo, mode="full")
    lags = correlation_lags(sigOne.size, sigTwo.size, mode="full")
    return lags[argmax(correlation)] / fs

###############################################################################

def getIntercepts(X,Y,theta):
    if len(X) == 2:
        if theta[0] == theta[1]:
            return None, None, None


        m1 = tan(theta[0])
        c1 = Y[0] - m1*X[0]

        m2 = tan(theta[1])
        c2 = Y[1] - m2*X[1]

        intersectsX = (c2-c1)/(m1-m2)
        intersectsY = m1*intersectsX + c1
        pairs = None

        return intersectsX, intersectsY, pairs

    else:
        [pairs, numPairs] = constructPairs(len(X))

        intersectsX = zeros(numPairs,)
        intersectsY = zeros(numPairs,)
        # print(f"intersectsX = {intersectsX}, intersectsY = {intersectsY}")

        for idx, pair in enumerate(pairs):
            # print(f"idx = {idx}, pair = {pair}")
            intersectsX[idx], intersectsY[idx], _ = getIntercepts(
                    append(X[pair[0]], X[pair[1]]),
                    append(Y[pair[0]], Y[pair[1]]),
                    append(theta[pair[0]], theta[pair[1]])
                    )

        return intersectsX, intersectsY, pairs

###############################################################################
        
def getMicData(filename, num_samples = None):
    given_data_txt = read_csv(filename, delimiter=",", encoding="utf8")

    time_column = given_data_txt.columns[0]
    mic_columns = given_data_txt.columns[1:]

    fs = 1/( float(given_data_txt[time_column][1].split(" ")[0]) 
             - float(given_data_txt[time_column][0].split(" ")[0])
            )
            
    mic_data = given_data_txt[mic_columns].transpose().to_numpy()
    for mic_idx, mic in enumerate(mic_data):
        temp_mean = mean(mic)

        for idx, datapoint in enumerate(mic):
            mic_data[mic_idx, idx] = datapoint - temp_mean



    if num_samples:
        mic_data = mic_data[:, :num_samples]

    return fs, mic_data