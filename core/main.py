#%% Imports

import napari
import numpy as np
from skimage import io 
from pathlib import Path
from joblib import Parallel, delayed 

#%%

# file_name = 'DUP_ch1Kate_20220517_7h_01_s&tCrop.tif'
# file_name = 'DUP_ch2EB1_20220517_7h_01_s&tCrop.tif'
file_name = 'Mito_72_s&tCrop.tif'
# file_name = 'Mito_74_DUP_s&tCrop.tif'

#%%

# Create paths
root_path = Path(__file__).parents[1]
data_path = Path(root_path / 'data' )
file_path = Path(root_path / 'data' / file_name)

# Open data
stack = io.imread(file_path) 

#%%

from skimage.morphology import disk, white_tophat

output_list = Parallel(n_jobs=-1)(
    delayed(white_tophat)(
        frame,
        disk(10)
        )
    for frame in stack
    )    

# process = np.stack(output_list)
process = stack.copy()
    
#%%

import pims
import trackpy as tp
import matplotlib.pyplot as plt


f = tp.locate(process[0], 5)
tp.annotate(f, process[0])

fig, ax = plt.subplots()
ax.hist(f['mass'], bins=20)

f = tp.locate(process[0], 5, minmass=150)
tp.annotate(f, process[0])

#%% 

test = 


#%%

viewer = napari.view_image(process)