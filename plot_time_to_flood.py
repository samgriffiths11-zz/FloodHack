#Script to plot the time to the next flood event with forecast probability > 50%

#Input array of probabilities "data_in" has dims () - assume [lead_time,lat,lon] for now. Assume there is also lat and lon values.

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import numpy as np

import pickle
import shapefile as shp

from gen_functions import make_fake_data_lat_lon
#from plot_shapefile import plot_shapefile

##Making fake data for testing
n_leads=30
#lonmin=-11
#lonmax=3
#latmin=49
#latmax=60
#nlons=(lonmax-lonmin+1)
#nlats=(latmax-latmin+1)
#lons=np.arange(lonmin,lonmax+1)
#lats=np.arange(latmin,latmax+1)
##nonzero_coords=[[0,0],[0,1],[1,1],[2,2],[2,3],[3,3]]
#nonzero_coords=[[0,0],[0,1],[1,1],[2,2],[2,3],[3,3],[2,10]]
#data_in=make_fake_data_lat_lon(n_leads=n_leads,nlons=nlons,nlats=nlats,nonzero_coords=nonzero_coords)

#Real data
f=open('day_test_07.pkl','rb')
data_in=pickle.load(f)
f.close()
nlons=141
nlats=111
lats=49+10/40000.*360*np.arange(111)
lons=-11+10/40000.*360*np.arange(141)


#Get lon and lat bounds of each gridbox
lon_bounds=np.array([[lons[i],lons[i+1]] for i in range(nlons-1)])
lat_bounds=np.array([[lats[i],lats[i+1]] for i in range(nlats-1)])

no_flood_val=9999.  #value to use when no floods are forecasted in time horizon

first_day_prob_gt_50=data_in
first_day_prob_gt_50[first_day_prob_gt_50>50]=no_flood_val
first_day_prob_gt_50[first_day_prob_gt_50<0]=no_flood_val

#Get substation data and determine which grid boxes have substations that may be at risk.
flood_inds=np.where(first_day_prob_gt_50!=no_flood_val)

sf = shp.Reader("Substation_Site/substations_centroids_transform.shp")

substation_x=[]
substation_y=[]
for shape in sf.shapeRecords():
    substation_x.append([i[0] for i in shape.shape.points[:]][0])
    substation_y.append([i[1] for i in shape.shape.points[:]][0])

subst_flood_x=[]
subst_flood_y=[]
subst_flood_day=[]
subst_noflood_x=[]
subst_noflood_y=[]
subst_noflood_day=[]
first_day_prob_gt_50_plot=np.zeros(first_day_prob_gt_50.shape)  #for collecting flood warning time where there are substations
first_day_prob_gt_50_plot.fill(no_flood_val)
for x,y in zip(substation_x,substation_y):
    x_ind=np.where((lon_bounds[:,0]<x) & (x<=lon_bounds[:,1]))[0]
    y_ind=np.where((lat_bounds[:,0]<y) & (y<=lat_bounds[:,1]))[0] 
    if first_day_prob_gt_50[y_ind,x_ind]!=no_flood_val:  #identify substations at risk
        subst_flood_x.append(x)
        subst_flood_y.append(y)
        subst_flood_day.append(first_day_prob_gt_50[y_ind,x_ind])
        first_day_prob_gt_50_plot[y_ind,x_ind]=first_day_prob_gt_50[y_ind,x_ind]
    else:  #identify substations not at risk
        subst_noflood_x.append(x)
        subst_noflood_y.append(y)
        subst_noflood_day.append(first_day_prob_gt_50[y_ind,x_ind])
        

fig,ax=plt.subplots()
levels=[0,2,4,7,14,21,n_leads,no_flood_val]  #add no_flood_val to levels to stop the previous contour being shaded black

cmap = plt.cm.hot_r
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

#Plotting time to next flood of each area
#p=ax.pcolor(lons,lats,first_day_prob_gt_50_plot,cmap=cmap,norm=norm,vmin=levels[0],vmax=levels[-2])
#plt.sca(ax)
##cbar = fig.colorbar(p, boundaries=levels[:-1])  #colorbar with no_flood_val excluded

if len(subst_flood_x)>0:
    p=ax.scatter(subst_flood_x,subst_flood_y,c=subst_flood_day,cmap=cmap,norm=norm)  #substations at risk, coloured to indicate the time to the next expected flood.
    cbar = fig.colorbar(p, boundaries=levels[:-1])
ax.scatter(subst_noflood_x,subst_noflood_y,color='k')  #substations not at risk in black

fig.savefig('plot_time_to_flood.png')

plt.show()