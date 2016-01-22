import numpy as np

#Function to make fake probability data for a number of lead times on a lat-lon grid for GloFAS hack
def make_fake_data_lat_lon(n_leads=30,nlons=40,nlats=30,nonzero_coords=[[0,0],[0,1],[1,1],[2,2],[2,3],[3,3]]):
    arr=np.zeros((n_leads,nlats,nlons))
    
    for i,coord in enumerate(nonzero_coords):
        arr[:n_leads/2,coord[0],coord[1]]=((i+1)/2*np.arange(0,1,1./(n_leads/2))).clip(0,1)
        arr[n_leads/2:,coord[0],coord[1]]=((i+1)/2*np.arange(1,0,-1./(n_leads/2))).clip(0,1)
    
    return arr


#Function to make fake data for an ensemble at one point
def make_fake_data_pt(n_leads=30,n_ens=50):
    assert n_ens % 2 == 0, 'n_ens should be even'    
    
    ens_mean=np.sin(np.arange(n_leads)/n_leads*3./2*np.pi/180)
    
    rnd=np.zeros((n_leads,n_ens))
    rnd[:,:n_ens/2]=abs(np.random.normal(0,1,n_ens/2))
    rnd[:,n_ens/2:]=-rnd[:,:n_ens/2]  #make sure errors are symmetric about mean
    
    arr=np.tile(ens_mean[:,np.new_axis], (1,n_ens))+rnd
    
    return arr