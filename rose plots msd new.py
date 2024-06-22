import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import math

#define aspect of rose plot
fig1 = plt.figure(figsize = (5,5))
ax = plt.axes()
ax.set_xlabel('x/um')
ax.set_ylabel('y/um')
ax.set_xlim(-30,30)
ax.set_ylim(-30,30)

#define aspect of double-logarithmic msd plot
fig2 = plt.figure(figsize = (5,5))
ax2 = plt.axes()
ax2.set_xlabel('Log(tau/min)')
ax2.set_ylabel('Log(msd/um²)')
ax2.set_xlim(0,2.3)
ax2.set_ylim(-1,3)

#read in data from spreadsheet, *.txt file
f = open('Bcells_OPA_day2.txt','r')
l = []
l = [line.split() for line in f]
l=np.array(l)

ll = np.transpose(l)

#read the columns indicating x, y positions, time (t) and cell ID (num)
x = ll[0]
x = x.astype(np.float)
y = ll[1]
y = y.astype(np.float)
t = ll[6]
t = t.astype(np.float)
num = ll[8]
num = num.astype(np.int)

#organize x, y and t of all tracks in a 3xN matrix
position = x
position = np.c_[position, y]
position = np.c_[position, t]

ind_list = [0]
len_list = []

#retrive the number of tracks and the position where a new track beginns by identifying changes in cell ID along the cell ID string (num)
for i in range(1,len(num)):
    if num[i] == num[i-1]:
        j = i + 1
    else:
        ind_list = np.append(ind_list, j)
ind_list = ind_list.astype(np.int)

for i in range(len(ind_list)-1):
    len_list = np.append(len_list, ind_list[i+1]-ind_list[i])
len_list = np.append(len_list, len(num) - ind_list[len(ind_list)-1])
len_list = len_list.astype(np.int)
alpha = []

#split the matrix in x,y,t for all tracks (position) in single matrices x,y,t for each track
for i in range(len(ind_list)):
    k = ind_list[i]
    track = position[k] - position[k]
    #define track origin as (0,0)
    for j in range(len_list[i]): 
        track = np.c_[track, position[k+j] - position[k]]
    #plot cell tracks, all with origin in (0,0)
    if len(track[0]) > 1:
        ax.plot(track[0],track[1])
    # calculate mean square displacement (msd) and its logarithm (logmsd)
    msd = []
    tau = []
    logmsd = []
    logtau = []
    for l in range(1,len(track[0])-10):
        dummyr = 0.0
        for m in range(2,len(track[0])-1-l):
            dummyr += (track[0][m+l]-track[0][m])**2 + (track[1][m+l]-track[1][m])**2
        dummyr = dummyr/(len(track[0])-1-l)
        msd = np.append(msd,dummyr)
        #calculate time in minutes, relying on the time bin of image acquisition
        tau = np.append(tau,l*2.0)
        logmsd = np.append(logmsd,math.log10(dummyr))
        logtau = np.append(logtau,math.log10(l*2.0))
    #plot msd versus time-log in double logarithmic representation
    ax2.plot(logtau,logmsd)
    # #linear regression of logmsd as a function of log-time for each track
    # summ1 = 0.0
    # summ2 = 0.0
    # summ3 = 0.0
    # summ4 = 0.0
    # for j in range(len(logtau)):
    #     summ1 += logtau[j]
    #     summ2 += logtau[j]*logtau[j]
    #     summ3 += logmsd[j]
    #     summ4 += logmsd[j]*logtau[j]
    # exponent1 = (summ4*len(logtau) - summ3*summ1)
    # exponent2 = (len(logtau)*summ2 - summ1*summ1)
    # if exponent2 == 0.0:
    #     print('no result!')
    # else:
    #     exponent = exponent1/exponent2
    #     alpha = np.append(alpha, exponent)
    # #export msd dependence on time-log (tau) of each single track
    # # f = open('track'+ str(i) +'.txt','w')
    # # for n in range(len(tau)):
    # #     f.write(str(tau[n]) + '\t' + str(msd[n]) + '\n')
    # # f.close()
    # #export of the slopes (exponent alpha list) of logmsd as a function of log-time for all tracks
    # f = open('exponents_alpha.txt','w')
    # for n in range(len(alpha)):
    #     f.write(str(alpha[n]) + '\n')
    # f.close()

            
