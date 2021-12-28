# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
import random
from PIL import ImageFilter

import torch
import torch.nn as nn


class SimSiam(nn.Module):
    """
    Build a SimSiam model.
    """

    def __init__(self, base_encoder, dim=1024, pred_dim=512):
        super(SimSiam, self).__init__()
        self.dim = dim  # dim: feature dimension (default: 128)
        self.pred_dim = pred_dim  # pred_dim: hidden dimension of the predictor (default: 512)
        self.online_network = base_encoder(num_classes=self.dim, zero_init_residual=True)
        self.target_network = base_encoder(num_classes=self.dim, zero_init_residual=True)

        prev_dim = self.online_network.fc.weight.shape[1]
        self.online_network.fc = nn.Sequential(
            nn.Linear(prev_dim, prev_dim, bias=False),
            nn.BatchNorm1d(prev_dim),
            nn.ReLU(inplace=True),  # first layer
            nn.Linear(prev_dim, prev_dim, bias=False),
            nn.BatchNorm1d(prev_dim),
            nn.ReLU(inplace=True),  # second layer
            nn.Linear(prev_dim, self.dim, bias=False),
            nn.BatchNorm1d(self.dim, affine=False),  # third layer

            nn.Linear(self.dim, self.pred_dim, bias=False),
            nn.BatchNorm1d(self.pred_dim),
            nn.ReLU(inplace=True),  # fourth layer
            nn.Linear(self.pred_dim, self.dim))  # output layer

        self.target_network.fc = nn.Sequential(
            nn.Linear(prev_dim, prev_dim, bias=False),
            nn.BatchNorm1d(prev_dim),
            nn.ReLU(inplace=True),  # first layer
            nn.Linear(prev_dim, prev_dim, bias=False),
            nn.BatchNorm1d(prev_dim),
            nn.ReLU(inplace=True),  # second layer
            nn.Linear(prev_dim, self.dim, bias=False),
            nn.BatchNorm1d(self.dim, affine=False),  # third layer

            nn.Linear(self.dim, self.pred_dim, bias=False),
            nn.BatchNorm1d(self.pred_dim),
            nn.ReLU(inplace=True),  # fourth layer
            nn.Linear(self.pred_dim, self.dim))  # output layer

    def forward(self, img):
        predictions_from_img = self.online_network(img)
        targets_to_img = self.target_network(img)

        return predictions_from_img, targets_to_img


class TwoCropsTransform:
    """Take two random crops of one image as the query and key."""

    def __init__(self, base_transform):
        self.base_transform = base_transform

    def __call__(self, x):
        q = self.base_transform(x)
        k = self.base_transform(x)
        return [q, k]


class GaussianBlur(object):
    """Gaussian blur augmentation in SimCLR https://arxiv.org/abs/2002.05709"""

    def __init__(self, sigma=[.1, 2.]):
        self.sigma = sigma

    def __call__(self, x):
        sigma = random.uniform(self.sigma[0], self.sigma[1])
        x = x.filter(ImageFilter.GaussianBlur(radius=sigma))
        return x
