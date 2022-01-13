# %%
import numpy as np
import scipy.io as sio

from scipy.signal import (
    correlate,
    correlation_lags
    )

from math import sqrt
from time import time
from matplotlib.pyplot import (
    subplots,
    plot,
    show
    )

from utilityfunctions import (
    constructPairs,
    getLag,
    getIntercepts,
    getMicData
    )

# %%
datang60 = 0
plot=False

if datang60:
    fname = "S19_VT_60.txt"

else: 
    fname = "S19_VT_15.txt"

fs, mics = getMicData(fname, 2000)


sampleLength = 200


# %%
mics_norm = mics
for idx, raw_voltage in enumerate(mics):
    volt_mean = np.mean(raw_voltage)
    mics_norm[idx] = mics[idx] - volt_mean

# %%
# speed of sound in air
c = 340;            # [metres per second]

# mic array parameters/dimensions
mic_locations = np.array([
                 [0, 0.2],
                 [0.26, 0],
                 [0.52, 0],
                 [0.78, 0]
                 ]); # [metres]

#########################################################
# %%
num_mics = len(mic_locations)
pairs, num_pairs = constructPairs(num_mics)

# %%
pair_locations = np.zeros((num_pairs, 2))
pairSpace = np.zeros((num_pairs, ))
pairTau = np.zeros((num_pairs, ))


t=time()

for pair_idx, pair in enumerate(pairs):
    each_mic_locations = [mic_locations[pair[0]], mic_locations[pair[1]]]
    pair_locations[pair_idx] = np.mean(each_mic_locations, 0)

    pairSpace[pair_idx] = sqrt((each_mic_locations[0][0] - each_mic_locations[1][0])**2 + (each_mic_locations[0][1] - each_mic_locations[1][1])**2)

    # first mic signal
    sigOne = mics_norm[pair[0], :]
    # second mic signal
    sigTwo = mics_norm[pair[1], :]

    pairTau[pair_idx] = getLag(sigOne, sigTwo, fs)


pairThetas = np.arccos( np.divide( (pairTau*c), pairSpace ) )

print(time()-t)

for i, theta in enumerate(pairThetas):
    print((f"pair {i}: theta = {theta}")) 

# %% [markdown]
# We now have the direction of the sound source from each mic pair.\
# We can plot this using ```matplotlib``` to graphically verify the result.

# %%
if plot:
    ###############################################################################
    ## Plot results

    # the X and Y locations of the midpoints between each pair of mics are in the pair_locations variable
    X1 = pair_locations[:,0]
    Y1 = pair_locations[:,1]

    # to plot a quiver diagram, we need the U and V components of the vectors:
    U = np.cos(pairThetas)
    V = np.sin(pairThetas)

    # get another point on the ray off in the distance
    scaleLine = 100
    X2 = X1 + scaleLine*U
    Y2 = Y1 + scaleLine*V

    # create the figure, axes
    fig, ax = subplots()

    # plot the mic locations
    micPosPlot = plot(mic_locations[:,0], mic_locations[:,1], 'xr', ms=15)

    # plot the "pair locations" 
    micPairMeanPosPlot = plot(X1,Y1, 'og')

    # plot a ray to represent the estimated angle of arrival "at" each mic pair
    # for line, _ in enumerate(X1):
    #     plot([X1[line], X2[line]], [Y1[line], Y2[line]])

    for line, _ in enumerate(X1):
        x = np.append(X1[line], X2[line])
        y = np.append(Y1[line], Y2[line])
        plot(x, y)

    Xintercept, Yintercept, _ = getIntercepts(X1, Y1, pairThetas)
    # print(f"Xintercept = {Xintercept}, \nYintercept = {Yintercept}")

    # plot the estimates of the location of the source 
    micPairMeanPosPlot = plot(Xintercept, Yintercept, 'ok', ms=5)

    # find mean location of estimates
    meanx = np.nanmean(Xintercept)
    # print(meanx)
    meany = np.nanmean(Yintercept)
    # print(meany)
    range_of_estimate = ( (max(Xintercept) - min(Xintercept))**2 + (max(Xintercept) - min(Xintercept))**2 )**0.5

    plot(meanx, meany, 'ob', ms=15, fillstyle="none")

    ax.axis('equal')

    if datang60:
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.5, 3)
    else:
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.5, 5)
    show()



