from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import math
import os

def unpatchfly(img_patches, img_size, patch_size):
    recon_img = np.zeros(img_size, dtype=np.uint8)
    for h in range(img_patches.shape[0]):
        if (h+1) != img_patches.shape[0]:
            for w in range(img_patches.shape[1]):
                if (w+1) != img_patches.shape[1]:
                    recon_img[h*patch_size[1]:(h+1)*patch_size[1], w * patch_size[0] : (w+1)*patch_size[0], :] = img_patches[h][w][0]
                else:
                    recon_img[h*patch_size[1]:(h+1)*patch_size[1], -1 * (patch_size[0] + 1) : -1, :] = img_patches[h][w][0]
        else:
            for w in range(img_patches.shape[1]):             
                if (w+1) != img_patches.shape[1]:
                    recon_img[-1 * (patch_size[1]+1):-1, w * patch_size[0] : (w+1)*patch_size[0], :] = img_patches[h][w][0]
                else:
                    recon_img[-1 * (patch_size[1] + 1):-1, -1 * (patch_size[0] + 1) : -1, :] = img_patches[h][w][0]
            
    return recon_img