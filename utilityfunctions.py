import numpy as np
# to determine correlation/TDOA between mics
from scipy.signal import correlate, correlation_lags

from math import tan

###############################################################################

def constructPairs(input_list):
    '''Returns a list of unique pairs and its length
       generates a list of pairs of the inputs and returns this list along
       with the length of the list'''
    if np.isscalar(input_list):
        amntItems = input_list
        input_list = np.transpose(np.arange(input_list))
    else:
        amntItems = len(input_list)

    paircount = int(amntItems*(amntItems-1)/2)
    
    pairs = np.zeros((paircount, 2))
    
    cntr = 0
    for i in range(amntItems):
        for j in range(i+1, amntItems):
            pairs[cntr] = np.array([input_list[i], input_list[j]])
            cntr = cntr + 1

    return pairs.astype(int), paircount

###############################################################################

def getLag (sigOne, sigTwo, fs):
    correlation = correlate(sigOne, sigTwo, mode="full")
    lags = correlation_lags(sigOne.size, sigTwo.size, mode="full")
    return lags[np.argmax(correlation)] / fs

###############################################################################

def getIntercepts(X,Y,theta):
    if len(X) == 2:
        m1 = tan(theta[0])
        c1 = Y[0] - m1*X[0]

        m2 = tan(theta[1])
        c2 = Y[1] - m2*X[1]

        intersectsX = (c2-c1)/(m1-m2)
        intersectsY = m1*intersectsX + c1
        pairs = 0

        return intersectsX, intersectsY, pairs

    else:
        [pairs, numPairs] = constructPairs(len(X))

        intersectsX = np.zeros(numPairs,)
        intersectsY = np.zeros(numPairs,)
        print(f"intersectsX = {intersectsX}, intersectsY = {intersectsY}")

        for idx, pair in enumerate(pairs):
            print(f"idx = {idx}, pair = {pair}")
            intersectsX[idx], intersectsY[idx], _ = getIntercepts(
                    np.append(X[pair[0]], X[pair[1]]),
                    np.append(Y[pair[0]], Y[pair[1]]),
                    np.append(theta[pair[0]], theta[pair[1]])
                    )

        return intersectsX, intersectsY, pairs