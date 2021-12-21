from torchvision.transforms import ColorJitter, Grayscale, GaussianBlur
import torchvision.transforms.functional as FT
import random

default_kwargs = {}
transform_dict = {'ColorJitter':ColorJitter, 'Grayscale':Grayscale}

