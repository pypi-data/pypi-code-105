import numpy as np
from fastcore.basics import patch_to
from pycocotools.coco import COCO


@patch_to(COCO, as_prop=True)
def label_counts(self):
    """count of labels in the dataset. Ex: 'microwave_|_total_count': 55"""
    cat2img: dict = dict()
    for cat_id, img_ids in self.catToImgs.items():
        cat2img[self.cats[cat_id]["name"] + "_|_" + "total_count"] = len(img_ids)
    return cat2img


@patch_to(COCO, as_prop=True)
def label_presence(self):
    """total images in which the label is present."""
    cat2img: dict = dict()
    for cat_id, img_ids in self.catToImgs.items():
        cat2img[self.cats[cat_id]["name"] + "_|_" + "images_present"] = np.unique(
            img_ids
        ).shape[0]
    return cat2img


@patch_to(COCO, as_prop=True)
def img_wise_counts(self):
    """total objects present in a image."""
    return [len(i) for _, i in self.imgToAnns.items()]


@patch_to(COCO, as_prop=True)
def label_names(self):
    """labels presents in the dataset"""
    return [i["name"] for _, i in self.cats.items()]


@patch_to(COCO)
def get_cat_ids(self, cat_names=[], sup_names=[], cat_ids=[]):
    return self.getCatIds(cat_names, sup_names, cat_ids)


@patch_to(COCO, as_prop=True)
def label_ids(self):
    return self.get_cat_ids(cat_names=self.label_names)


@patch_to(COCO, as_prop=True)
def label_names_available(self):
    """labels for which images are present.
    This often when u happen to annotate images using your own tools. some labels might not have any instances in the dataset.
    """
    return [i.rsplit("_|_")[0] for i in list(self.label_counts.keys())]


@patch_to(COCO, as_prop=True)
def count_images(self):
    """total count of images in the dataset."""
    return len(self.imgs)


@patch_to(COCO, as_prop=False)
def getwh(self):
    wh_all = []
    for i in self.dataset["annotations"]:
        img = self.imgs[self.getImgIds([i["image_id"]])[0]]
        wh = img["width"], img["height"]
        wh_all.append(wh)
    return np.asarray(wh_all)


@patch_to(COCO, as_prop=False)
def get_bbox(self):
    ## category_id in cocojson starts from 1
    return np.asarray(
        [[i["category_id"]] + i["bbox"] for i in self.dataset["annotations"]]
    )
