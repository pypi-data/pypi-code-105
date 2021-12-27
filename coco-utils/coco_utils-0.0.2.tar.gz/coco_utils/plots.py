from pathlib import Path
from typing import Union

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
from PIL import Image, ImageDraw

from coco_utils.coco import COCO
from coco_utils.utils import xywh2xyxy


class Colors:
    # Ultralytics color palette https://ultralytics.com/
    def __init__(self):
        # hex = matplotlib.colors.TABLEAU_COLORS.values()
        hex = (
            "FF3838",
            "FF9D97",
            "FF701F",
            "FFB21D",
            "CFD231",
            "48F90A",
            "92CC17",
            "3DDB86",
            "1A9334",
            "00D4BB",
            "2C99A8",
            "00C2FF",
            "344593",
            "6473FF",
            "0018EC",
            "8438FF",
            "520085",
            "CB38FF",
            "FF95C8",
            "FF37C7",
        )
        self.palette = [self.hex2rgb("#" + c) for c in hex]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):  # rgb order (PIL)
        return tuple(int(h[1 + i : 1 + i + 2], 16) for i in (0, 2, 4))


colors = Colors()  # create instance for 'from utils.plots import colors'


def plot_labels(labels, names=(), save_dir=Path("")):
    ## labels N, 5 0-> label x, y, w, h-> all scaled to (w, h, w, h) of images
    ## names is the labels names. labels also start from 0
    # plot dataset labels
    print("Plotting labels... ")
    cc, b = labels[:, 0], labels[:, 1:].transpose()  # classes, boxes
    nc = int(cc.max())
    # nc = int(cc.max() + 1)  # number of classes
    x = pd.DataFrame(b.transpose(), columns=["x", "y", "width", "height"])

    # seaborn correlogram
    sn.pairplot(
        x,
        corner=True,
        diag_kind="auto",
        kind="hist",
        diag_kws=dict(bins=50),
        plot_kws=dict(pmax=0.9),
    )
    plt.savefig(save_dir / "labels_correlogram.jpg", dpi=200)
    plt.close()

    # matplotlib labels
    plt.style.use("bmh")
    # matplotlib.use('svg')  # faster
    ax = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)[1].ravel()
    # zero is backgroud. so our classes are labelled from 1 onwards
    y = ax[0].hist(cc - 1, bins=np.linspace(0, nc, nc + 1) - 0.5, rwidth=0.8)
    # [y[2].patches[i].set_color([x / 255 for x in colors(i)]) for i in range(nc)]  # update colors bug #3195
    ax[0].set_ylabel("instances")
    if 0 < len(names) < 30:
        # breakpoint()
        ax[0].set_xticks(range(len(names)))
        ax[0].set_xticklabels(names, rotation=90, fontsize=10)
    else:
        ax[0].set_xlabel("classes")
    sn.histplot(x, x="x", y="y", ax=ax[2], bins=50, pmax=0.9)
    sn.histplot(x, x="width", y="height", ax=ax[3], bins=50, pmax=0.9)

    # rectangles
    labels[:, 1:3] = 0.5  # center
    labels[:, 1:] = xywh2xyxy(labels[:, 1:]) * 2000
    img = Image.fromarray(np.ones((2000, 2000, 3), dtype=np.uint8) * 255)
    for cls, *box in labels[:1000]:
        ImageDraw.Draw(img).rectangle(box, width=1, outline=colors(cls))  # plot
    ax[1].imshow(img)
    ax[1].axis("off")

    for a in [0, 1, 2, 3]:
        for s in ["top", "right", "left", "bottom"]:
            ax[a].spines[s].set_visible(False)

    plt.savefig(save_dir / "labels.jpg", dpi=200)
    matplotlib.use("Agg")
    plt.close()


def _get_bbox_names(cc: COCO):
    bbox = cc.get_bbox()
    wh_all = cc.getwh()
    bbox[:, 1:3] = bbox[:, 1:3] / wh_all
    bbox[:, 3:] = bbox[:, 3:] / wh_all
    bbox = bbox[np.isin(bbox[:, 0], cc.label_ids)]
    name = [i["name"] for i in cc.dataset["categories"]]
    name = {name[num]: n for num, n in enumerate(cc.label_ids)}
    return bbox, name


def _plot_coco_labels_str_or_coco(loc: Union[str, COCO]):
    cc = COCO(loc) if isinstance(loc, str) else loc
    bbox, name = _get_bbox_names(cc)
    return bbox, name


def plot_coco_labels(loc: str, save_dir: str)->None:
    Path(save_dir).mkdir(exist_ok=True)
    bboxes, names = _plot_coco_labels_str_or_coco(loc)
    plot_labels(bboxes, list(names.keys()), save_dir=Path(save_dir))
