# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 20:39:00 2020

@author: MARCOS TIEPPO
"""

import os
import numpy as np
from math import sqrt

#Define working directory
os.chdir('C:/working_directory')
#Open file with slope values for one model
f=open("slope_values_for_one_model.txt","r")
lines2=f.readlines()[1:]
result=[]

#Sponge position in the model given by Metashape
x1 = -0.96774710378546902
y1 = 0.0415895246857588
sp = 'Sp'   #Species name for file name (Sp or Ph)
reef = 'Cacela'   # Reef name for file name (Cacela or Lacem)

mean_slope = 0
cont = 0
cont2 = 0
cont3 = 0
cont4 = 0
values = []
step = .25
xsum = x1-1
ysum = y1-1
stdev = []
mean = np.zeros((64,3),dtype=float)
mean[:] = np.nan

#Calculating the mean slope values for the small squares around the sponge
while cont2 < 8:
    while cont3 < 8:
        for m in lines2:
            if float(m.split(',')[3]) <= xsum+step and float(m.split(',')[3]) >= xsum and float(m.split(',')[4]) <= ysum+step and float(m.split(',')[4]) >= ysum:
                mean_slope = mean_slope + float(m.split(',')[2])
                cont += 1
                values.append(float(m.split(',')[2]))
        if cont > 0:
            stdev.append(np.std(values))        
            mean[cont4,0] = (mean_slope/cont)
            mean[cont4,1] = (xsum + step)
            mean[cont4,2] = (ysum + step)
        cont4 += 1
        xsum = xsum + step
        cont3 += 1
        cont = 0
        mean_slope=0
        values = []
    ysum = ysum + step
    xsum = x1-1
    cont2 += 1
    cont3 = 0

print ('Areas mean slopes = ',mean)
print ('Standard deviation = ',stdev)

mean_areas = np.nanmean(mean[:,0])
stdev_areas = np.nanstd(mean[:,0])
print('Average of all areas = ',mean_areas)
print ('Average standard deviation = ',stdev_areas)

#Calculating the minimum distance between sponge and high slope area
cont=0
dist_min = 100
dist = 171
for x in mean[:,0]:
    if x != 'nan' and x >= (np.nanmax(mean[:,0])-5):
        dist = sqrt((mean[cont,1] - x1)**2 + (mean[cont,2] - y1)**2 )
        if dist < dist_min:
            dist_min = dist
    cont += 1        
print ('Minimal distance between sponge and high slope feature = ',dist_min)

#Saving the values in a txt file
with open("C:/Users/MARCOS TIEPPO/Documents/TESE_MESTRADO_MESHES/BATCHS/SLOPES_AND_MDs.txt", "a") as myfile:
    myfile.write('\n' + reef + ' ' + sp + ' ' + str(mean_areas) + ' ' + str(stdev_areas) + ' ' + str(dist_min) + ' ' + str(x1) + ' ' + str(y1))


