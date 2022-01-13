#%%
import numpy as np
import matplotlib.pyplot as plt

# %%
c = 340

#%%

micarray = np.array([
    (-1, 0, 0),
    (1, 0, 0)
])

d = np.linalg.norm(micarray[1] - micarray[0])

sourceloc = np.array([
    (a, b, c) for a in range(100) for b in range(100) for c in range(100)
])

#%%
tauFLAT = []
tau3D = []

for idx, source in enumerate(sourceloc):
    d1FLAT = np.linalg.norm(source[:1]-micarray[0,:1])
    d2FLAT = np.linalg.norm(source[:1]-micarray[1,:1])
    tauFLAT.append((d2FLAT-d1FLAT)/c)


    d13D = np.linalg.norm(source-micarray[0])
    d23D = np.linalg.norm(source-micarray[1])
    tau3D.append((d23D-d13D)/c)


# %%


thetaFLAT = np.arccos(tauFLAT * c / d)

theta3D = np.arccos(tau3D * c / d)

# %%
max = 0
maxi = 0
for i, _ in enumerate(thetaFLAT):
    diff = abs(theta3D[i] - thetaFLAT[i])
    err = diff / theta3D[i]

    if err > max:
        max = err
        maxdiff = diff
        maxi = i

perc = round(max * 100)
print(f"Accuracy {maxi+1}: {perc}% ({maxdiff} rad) [{sourceloc[maxi]}] ")
