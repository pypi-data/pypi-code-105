#!/usr/bin/env python3
#
# Copyright 2021 Graviti. Licensed under MIT License.
#
# pylint: disable=invalid-name

"""Dataloader of LeedsSportsPose dataset."""

import os

from tensorbay.dataset import Data, Dataset
from tensorbay.exception import ModuleImportError
from tensorbay.geometry import Keypoint2D
from tensorbay.label import LabeledKeypoints2D
from tensorbay.opendataset._utility import glob

DATASET_NAME = "LeedsSportsPose"


def LeedsSportsPose(path: str) -> Dataset:
    """`Leeds Sports Pose <http://sam.johnson.io/research/lsp.html>`_ dataset.

    The folder structure should be like::

        <path>
            joints.mat
            images/
                im0001.jpg
                im0002.jpg
                ...

    Arguments:
        path: The root directory of the dataset.

    Raises:
        ModuleImportError: When the module "scipy" can not be found.

    Returns:
        Loaded :class:`~tensorbay.dataset.dataset.Dataset` instance.

    """
    try:
        from scipy.io import loadmat  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError as error:
        raise ModuleImportError(module_name=error.name) from error

    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME)
    dataset.load_catalog(os.path.join(os.path.dirname(__file__), "catalog.json"))
    segment = dataset.create_segment()

    mat = loadmat(os.path.join(root_path, "joints.mat"))

    joints = mat["joints"].T
    image_paths = glob(os.path.join(root_path, "images", "*.jpg"))
    for image_path in image_paths:
        data = Data(image_path)
        data.label.keypoints2d = []
        index = int(os.path.basename(image_path)[2:6]) - 1  # get image index from "im0001.jpg"

        keypoints = LabeledKeypoints2D()
        for keypoint in joints[index]:
            keypoints.append(Keypoint2D(keypoint[0], keypoint[1], int(not keypoint[2])))

        data.label.keypoints2d.append(keypoints)
        segment.append(data)
    return dataset
