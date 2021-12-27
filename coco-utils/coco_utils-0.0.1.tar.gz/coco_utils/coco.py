import numpy as np 

from pycocotools.coco import COCO 
from fastcore.basics import patch_to

@patch_to(COCO, as_prop=True)
def label_counts(self):
    """count of labels in the dataset. Ex: 'microwave_|_total_count': 55 
    """
    cat2img: dict = dict()
    for cat_id, img_ids in self.catToImgs.items():
        cat2img[self.cats[cat_id]["name"]+ "_|_" + "total_count"] = len(img_ids)
    return cat2img

@patch_to(COCO, as_prop=True)
def label_presence(self):
    """total images in which the label is present. 
    """
    cat2img: dict = dict()
    for cat_id, img_ids in self.catToImgs.items():
        cat2img[self.cats[cat_id]["name"]+ "_|_" + "images_present"] = np.unique(img_ids).shape[0]
    return cat2img

@patch_to(COCO, as_prop=True)
def img_wise_counts(self):
    """total objects present in a image.
    """ 
    return [len(i) for _, i in self.imgToAnns.items()]

@patch_to(COCO, as_prop=True)
def label_names(self):
    """labels presents in the dataset 
    """
    return [i["name"] for _, i in self.cats.items()]

@patch_to(COCO, as_prop=True)
def label_names_available(self):
    """labels for which images are present. 
    This often when u happen to annotate images using your own tools. some labels might not have any instances in the dataset.
    """
    return [i.rsplit("_|_")[0] for i in list(self.label_counts.keys())]

@patch_to(COCO, as_prop=True)
def count_images(self):
    """total count of images in the dataset. 
    """
    return len(self.imgs)