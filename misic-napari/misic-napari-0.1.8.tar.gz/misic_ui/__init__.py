try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

## import required functions
import os
# ignore gpu: this needs to rectfied incase there is gpu access to tensorflow
# os.environ["CUDA_VISIBLE_DEVICES"]="-1" 
import tensorflow as tf
try:
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
    pass

import numpy as np
from skimage.transform import rescale,resize
from skimage.feature import shape_index
from skimage.util import random_noise

# import MiSiC Stuff
from misic_ui.misic.misic import *
from misic_ui.misic.extras import *
from misic_ui.misic.utils import *
# get helper functions
from misic_ui.misic_helpers import *

from napari_plugin_engine import napari_hook_implementation
from magicgui import magic_factory
from magicgui.tqdm import trange
from napari import Viewer
from napari.layers import Image

import pathlib
import json

# make misic
mseg = MiSiC()

# make default params dictionary
params = {}
params['invert'] = True
params['scale'] = 1.0
params['gamma'] = 0.5
params['sharpness_sigma'] = 0
params['sharpness_amount'] = 2
params['gaussian_laplace'] = False
params['sensitivity'] = 0.001
params['local_noise'] = True
params['post_process'] = True
params['roi'] = [0,0,256,256]
params['use_roi'] = False


mean_width = 10
standard_width = 9.87

def segment_single_image(im,params):
    '''
    Segments single iamge using the parameters dictionary.
    '''
    sr,sc = im.shape
    roi = params['roi'] 
    roi[0] = int(max(roi[0],0))
    roi[1] = int(max(roi[1],0))
    roi[2] = int(min(roi[2],sr))
    roi[3] = int(min(roi[3],sc))
    params['roi']  = roi
    
    if params['use_roi']:
        roi = params['roi']
        tmp = im[roi[0]:roi[2],roi[1]:roi[3]]
        tsr,tsc = tmp.shape
        tmp = preprocess(tmp,params)
        yp = mseg.segment(tmp,exclude = 16)[:,:,0]
        yp = resize(yp,(tsr,tsc))   
        if params['post_process']:
            yp = postprocessing(im[roi[0]:roi[2],roi[1]:roi[3]] if params['invert'] else -im[roi[0]:roi[2],roi[1]:roi[3]],yp,int(standard_width/params['scale']))                
        #res = np.zeros((sr,sc),dtype = yp.dtype)
        #res[roi[0]:roi[2],roi[1]:roi[3]] = yp
    else:
        tmp = preprocess(im,params)
        yp = mseg.segment(tmp,exclude = 16)[:,:,0]
        yp = resize(yp,(sr,sc))    
        if params['post_process']:
            yp = postprocessing(im if params['invert'] else -im,yp,int(standard_width/params['scale']))   
        #res = yp

    if np.max(yp) == 1:
        yp = yp *255

    return yp #(yp*255).astype(np.uint8)



@magic_factory(result_widget=True,call_button='get cell-width')
def get_width(viewer: Viewer) -> int:    
    '''
    Make a Shapes layer named 'cell_width' if it doesnt exists.
    Get the mean width of multiple lines to obtain the working scale
    '''
    try:
        lines = viewer.layers['cell_width'].data    
        mean_width0 = 0
        for l in lines:
            mean_width0 += np.sqrt((l[0][0]-l[1][0])**2 + (l[0][1]-l[1][1])**2)
        mean_width0/=len(lines)
        mean_width0 = round(mean_width0,2)
        params['scale'] = standard_width/mean_width0   
    except:
        viewer.add_shapes(shape_type='lines',name = 'cell_width')
        mean_width0 = standard_width

    return mean_width0   

# @magic_factory(call_button='get roi')
# def get_roi(viewer: Viewer):    
#     '''
#     Make a Shapes layer named 'cell_width' if it doesnt exists.
#     Get the mean width of multiple lines to obtain the working scale
#     '''
#     try:
#         roi = viewer.layers['roi'].data[0]
#         roi = np.array(roi)
#         params['roi'] = [np.min(roi[:,0]),np.min(roi[:,1]),np.max(roi[:,0]),np.max(roi[:,1])]
#         print(roi)
#         print(params['roi'])
#     except:
#         roi = np.array([[0,0],[256,256]])
#         viewer.add_shapes(roi, shape_type='rectangle', name = 'roi',edge_width=5,edge_color='coral', face_color='royalblue')    

## MagicGui widget for single image segmentation
@magic_factory(auto_call=True,
adjust_scale = {"widget_type": "FloatSlider", "max": 1.2,"min": 0.8,"step":0.025,'tracking': False,'readout' : True,'tooltip': 'Fine-tune the scale around the mean cell width.'}, 
noise_var = {"widget_type": "FloatSlider", "max": 0.50,"min": 0.00,"step":0.0001,'tracking': False,'readout' : True,'tooltip': 'Reduce false positives by adding noise.'},
gamma = {"widget_type": "FloatSlider", "max": 3.0,"min": 0.1,"step":0.1,'tracking': False,'readout' : True,'tooltip': 'Gamma correction.'},
sharpness_sigma = {"widget_type": "FloatSlider", "max": 3,"min": 0,"step":0.25,'tracking': False,'readout' : True,'tooltip': 'Sharpness scale in unsharp mask.'},
sharpness_amount = {"widget_type": "FloatSlider", "max": 5,"min": 0.5,"step":0.5,'tracking': False,'readout' : True,'tooltip': 'Sharpness amount in unsharp mask.'},
run = {"widget_type": "PushButton", 'value': True,'tooltip': 'Run again.'})
def segment(viewer: Viewer,data: 'napari.types.ImageData',
use_roi = True, 
light_background=True,
use_local_noise = False,
gaussian_laplace = False,
adjust_scale = 1,
noise_var = 0.0001, 
gamma= 0.5,
sharpness_sigma= 0,
sharpness_amount = 0.6,
post_process= True,
run = False,) -> 'napari.types.LayerDataTuple':
    '''
    Get parameters for a single image and output segmented image.
    '''
    # Make ROI
    try:
        roi = viewer.layers['roi'].data[0]
    except:
        roi = np.array([[0,0],[256,256]])
        viewer.add_shapes(roi, shape_type='rectangle', name = 'roi',edge_width=2,edge_color='red', face_color='black')

    # get roi and parameters dictionary
    roi = viewer.layers['roi'].data[0]
    roi = np.array(roi)
    params['roi'] = [np.min(roi[:,0]),np.min(roi[:,1]),np.max(roi[:,0]),np.max(roi[:,1])]
    scale = min(standard_width/mean_width,2.5)*adjust_scale 
    params['invert'] = light_background
    params['scale'] = scale
    params['gamma'] = gamma
    params['sharpness_sigma'] = sharpness_sigma
    params['sharpness_amount'] = sharpness_amount
    params['gaussian_laplace'] = gaussian_laplace
    params['sensitivity'] = noise_var
    params['local_noise'] = use_local_noise
    params['post_process'] = post_process
    params['use_roi'] = use_roi

    sr,sc = data.shape[-2],data.shape[-1]
    if viewer.dims.ndim == 3:
        fnum = viewer.dims.current_step[0]
        im = np.copy(data[fnum])        
    else:
        im = np.copy(data)            
    #status = 'MiSiC: processing ...'
    yp = segment_single_image(im,params)        

    if params['post_process']:
        if params['use_roi']:
            roi = params['roi']
            try:
                res = viewer.layers['segmentation'].data
                res[roi[0]:roi[2],roi[1]:roi[3]] = yp
            except:
                res = np.zeros((sr,sc),dtype = yp.dtype)
                res[roi[0]:roi[2],roi[1]:roi[3]] = yp
        else:
            res = yp

        try:
            del viewer.layers['probability-map']
            return (res,{'name': 'segmentation','opacity': 0.75}, 'labels')
        except:
            return (res,{'name': 'segmentation','opacity': 0.75}, 'labels')

    else:
        if params['use_roi']:
            roi = params['roi']
            try:
                res = viewer.layers['probability-map'].data
                res[roi[0]:roi[2],roi[1]:roi[3]] = yp
            except:
                res = np.zeros((sr,sc),dtype = yp.dtype)
                res[roi[0]:roi[2],roi[1]:roi[3]] = yp
        else:
            res = yp

        try:
            del viewer.layers['segmentation']
            return (res,{'name': 'probability-map','opacity': 0.75, 'blending': 'additive', 'colormap' : 'green'}, 'image') 
        except:
            return (res,{'name': 'probability-map','opacity': 0.75, 'blending': 'additive', 'colormap' : 'green'}, 'image') 

# once the parameters are the selected for single image, then process the stack
@magic_factory()
def segment_stack(data: "napari.types.ImageData") -> 'napari.types.LayerDataTuple':
    '''
    Segment the entire stack using the parameters obtained before
    '''
    params['scale'] = min(params['scale'],2.5)
    use_roi = params['use_roi']
    params['use_roi'] = False
        
    if len(data.shape) < 3:
        yp = segment_single_image(np.copy(data),params)
    else:
        im = np.copy(data)
        yp = np.array([segment_single_image(im[i],params) for i in trange(len(im))])  
    params['use_roi'] = use_roi       

    try:
        del viewer.layers['misic-seg']
    except:
        pass
    if params['post_process']:
        return (yp,{'name': 'misic-seg','opacity': 0.75}, 'labels')
    else:        
        return (yp,{'name': 'misic-seg','opacity': 0.75, 'blending': 'additive', 'colormap' : 'green'}, 'image') 


############ Save or Load parameters file
@magic_factory(output_folder={'mode': 'd'},call_button='Save')
def save_params(output_folder =  pathlib.Path.home(),filename = 'params'):
    '''
    Save parameters to file
    '''
    output_folder = os.path.normpath(output_folder)
    filename = output_folder + os.path.sep + filename + '.json'
    
    json.dump( params, open( filename, 'w' ) )

@magic_factory(filename={'mode': 'r','filter':'.json'},call_button='Load')
def load_params(filename =  pathlib.Path.home()):
    '''
    Load parameters to file
    '''
    output_folder = os.path.normpath(output_folder)
    filename = output_folder + os.path.sep + filename + '.json'
    
    params = json.load( open( filename) )
    
############ napari hooks
@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return [get_width,segment,segment_stack,save_params,load_params]

