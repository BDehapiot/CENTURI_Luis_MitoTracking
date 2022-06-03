#%% Imports

import pims
import napari
import numpy as np
import trackpy as tp
from skimage import io 
from pathlib import Path
import matplotlib.pyplot as plt
from joblib import Parallel, delayed 

#%% Inputs

# file_name = 'DUP_ch1Kate_20220517_7h_01_s&tCrop.tif'
file_name = 'DUP_ch2EB1_20220517_7h_01_s&tCrop.tif'
# file_name = 'DUP_ch2EB1_20220517_7h_01_s&tCrop_mod.tif'
# file_name = 'DUP_ch2EB1_20220517_7h_01_s&tCrop_mod2.tif'
# file_name = 'Mito_72_s&tCrop.tif'
# file_name = 'Mito_74_DUP_s&tCrop.tif'
# file_name = 'Mito_74_DUP_s&tCrop_mod.tif'

f_size = 7
f_min_mass = 20000
t_max_dist = 5
t_max_gap = 0
t_min_length = 20

#%% Initialize

# Create paths
root_path = Path(__file__).parents[1]
data_path = Path(root_path / 'data' )
file_path = Path(root_path / 'data' / file_name)

# Open data
stack = io.imread(file_path) 

#%% Preprocessing

# from skimage.restoration import rolling_ball

# output_list = Parallel(n_jobs=-1)(
#     delayed(rolling_ball)(
#         frame, radius=2,
#         )
#     for frame in stack
#     )

# background = np.stack(output_list, axis=0)
# processed = stack - background 

# viewer = napari.view_image(processed)

#%% Preprocessing

time_window = 31
clip = int(np.floor(time_window/2))
nan_array = np.full((clip , stack.shape[1], stack.shape[2]), np.nan)
nan_stack = np.concatenate((nan_array, stack, nan_array), axis=0)

roll_stack = np.zeros_like(stack)

for i in range(len(stack)):
    
    temp_stack = nan_stack[i:i+time_window,...]
    roll_stack[i,...] = np.nanmean(temp_stack, axis=0)

viewer = napari.view_image(roll_stack)

bgsub = np.subtract(stack.astype('int32'), roll_stack.astype('int32'))
bgsub = np.abs(bgsub)

viewer = napari.view_image(bgsub)
     
#%%

# f = tp.locate(stack[0], f_size)
# fig, ax = plt.subplots()
# ax.hist(f['mass'], bins=100)

#%%

# # Detect features (all frames)
# features = tp.batch(stack, f_size, minmass=f_min_mass)

# # Track features
# tp.quiet()

# tracking_data = tp.link(
#     features,
#     t_max_dist,
#     adaptive_stop=2.0,
#     adaptive_step=0.95,
#     memory=t_max_gap,
#     )   

# print('Before:', tracking_data['particle'].nunique())

# tracking_data = tp.filter_stubs(
#     tracking_data, 
#     t_min_length,
#     )

# print('After:', tracking_data['particle'].nunique())

#%% 

# coords = np.array(tracking_data.loc[:,['frame','y','x']])
# tracks = np.array(tracking_data.loc[:,['particle','frame','y','x']])

# my_properties = {
#     'track_id': np.full((len(tracks)), 65535)
#     }

#%%

# viewer = napari.view_image(stack)

# points_layer = viewer.add_points(
#     coords, 
#     size=f_size,
#     edge_width=0.1,
#     edge_color='red',
#     face_color='transparent',
#     opacity = 0.5,
#     )

# tracks_layer = viewer.add_tracks(
#     tracks, 
#     properties=my_properties,
#     color_by='track_id',
#     colormap='gray_r',
#     opacity=0.5,
#     )