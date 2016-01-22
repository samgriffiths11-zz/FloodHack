#Script to find flooding statistics within counties -not finished

#The following assumes data_in will be an array containing probabilities that a given area will pass the discharge threshold on a given day. To use data where the "time to flood" has been computed, replace first_day_prob_gt_50 with this data.

import matplotlib.pyplot as plt
import matplotlib.collections as collections
from matplotlib.colors import BoundaryNorm
import matplotlib.patches as mpatches
from matplotlib import path
import numpy as np

import fiona

from gen_functions import make_fake_data_lat_lon

#Making fake data for testing
lonmin=-11
lonmax=3
latmin=49
latmax=60
n_leads=30
nlons=(lonmax-lonmin+1)
nlats=(latmax-latmin+1)
lons=np.arange(lonmin,lonmax+1)
lats=np.arange(latmin,latmax+1)
nonzero_coords=[[0,0],[0,1],[1,1],[2,2],[2,3],[3,3],[2,10]]
data_in=make_fake_data_lat_lon(n_leads=n_leads,nlons=nlons,nlats=nlats,nonzero_coords=nonzero_coords)

data_in=data_in.transpose(0,2,1)  #make dims (leads, lons, lats)

grid=np.zeros((nlons*nlats,2))
for i in range(nlons):
    for j in range(nlats):
        grid[i*nlats+j,:]=[lons[i],lats[j]]

no_flood_val=9999  #value to use when no floods are forecasted in time horizon

#Set up plotting
fig,ax=plt.subplots()
cmap = plt.cm.hot_r
levels=np.arange(1,9)
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

#Calculate stats here - don't know what yet
fc = fiona.open('England_ct_2001/England_ct_2001_area_WGS84.shp')
score={}  #put stats for each region in here
patches=[]
scores=[]
for i,feature in enumerate(fc):
    
    p=path.Path(feature['geometry']['coordinates'][0])
    points_inds=p.contains_points(grid)
    
    score=0
    print np.count_nonzero(points_inds)
    if np.count_nonzero(points_inds)>0:

        first_day_prob_gt_50=np.zeros((np.count_nonzero(points_inds)))
        for j in range(np.count_nonzero(points_inds)):
            days_gt_50=np.where(data_in.reshape(n_leads,nlats*nlons)[:,j]>0.5)[0]  #mistake here, need to index the right element of points_inds
            if len(days_gt_50)>0:
                first_day_prob_gt_50[j]=np.min(days_gt_50)
            else:
                first_day_prob_gt_50[j]=np.inf

        min_time_to_flood=np.min(first_day_prob_gt_50)
        if min_time_to_flood<np.inf:
            score1=(n_leads-min_time_to_flood)/n_leads
        else:
            score1=0
        
        if np.count_nonzero(first_day_prob_gt_50<np.inf)<0:
            score2=np.mean(first_day_prob_gt_50[first_day_prob_gt_50<np.inf])
        else:
            score2=0

        score3=0
        for lead_ind in range(n_leads):
            score3+=len(np.where(data_in[lead_ind].ravel()[points_inds]!=0)[0])
        score3/=float(np.count_nonzero(points_inds)*n_leads)
        
        score=2**(score1+score2+score3)
        
        score*=4  #this is just to give a large range of scores with the fake data
        
    scores.append(score)

    poly = mpatches.Polygon(feature['geometry']['coordinates'][0], closed=True, fill=True, color=cmap(score))
    patches.append(poly) 
    
p = collections.PatchCollection(patches, cmap=cmap, norm=norm)
p.set_array(np.array(scores))
ax.add_collection(p)

ax.set_xlim(lons.min(),lons.max())
ax.set_ylim(lats.min(),lats.max())

plt.colorbar(p, boundaries=levels)
plt.show()

                
                