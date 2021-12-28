# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import logging

import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torch.utils.data.dataloader import DataLoader


class BYOL(nn.Module):
    def __init__(self, base_encoder, dim=128, mlp=True):
        super(BYOL, self).__init__()
        self.dim = dim  # dim: feature dimension (default: 128)
        self.online_network = base_encoder(num_classes=self.dim)
        self.target_network = base_encoder(num_classes=self.dim)

        if mlp:  # hack: brute-force replacement
            dim_mlp = self.online_network.fc.weight.shape[1]
            self.online_network.fc = nn.Sequential(
                nn.Linear(dim_mlp, dim_mlp),
                nn.BatchNorm1d(dim_mlp),
                nn.ReLU(),
                nn.Linear(dim_mlp, self.dim),

                nn.Linear(self.dim, self.dim),
                nn.BatchNorm1d(self.dim),
                nn.ReLU(),
                nn.Linear(self.dim, self.dim))

            self.target_network.fc = nn.Sequential(
                nn.Linear(dim_mlp, dim_mlp),
                nn.BatchNorm1d(dim_mlp),
                nn.ReLU(),
                nn.Linear(dim_mlp, self.dim),

                nn.Linear(self.dim, self.dim),
                nn.BatchNorm1d(self.dim),
                nn.ReLU(),
                nn.Linear(self.dim, self.dim))

    def forward(self, img):
        predictions_from_img = self.online_network(img)
        targets_to_img = self.target_network(img)

        return predictions_from_img, targets_to_img


class BYOLTrainer:
    def __init__(self, model, optimizer, args, **params):
        self.model = model
        self.optimizer = optimizer
        self.args = args

    @torch.no_grad()
    def _update_target_network_parameters(self):
        """
        Momentum update of the key encoder
        """
        for param_q, param_k in zip(self.model.online_network.parameters(), self.model.target_network.parameters()):
            param_k.data = param_k.data * self.args.m + param_q.data * (1. - self.args.m)

    @staticmethod
    def regression_loss(x, y):
        x = F.normalize(x, dim=1)
        y = F.normalize(y, dim=1)
        return 2 - 2 * (x * y).sum(dim=-1)

    def initializes_target_network(self):
        # init momentum network as encoder net
        for param_q, param_k in zip(self.model.online_network.parameters(), self.model.target_network.parameters()):
            param_k.data.copy_(param_q.data)  # initialize
            param_k.requires_grad = False  # not update by gradient

    def train(self, train_dataset):
        # drop_last舍去不足一个bach_size的样本
        train_loader = DataLoader(train_dataset, batch_size=self.args.batch_size, num_workers=self.args.num_workers, drop_last=False, shuffle=True)
        niter = 0
        self.initializes_target_network()

        for epoch_counter in range(self.args.epochs):
            loss = 0.
            for batch_view_1, batch_view_2 in train_loader:
                batch_view_1 = batch_view_1.to(self.args.device)
                batch_view_2 = batch_view_2.to(self.args.device)

                loss = self.L2_loss(batch_view_1, batch_view_2)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                self._update_target_network_parameters()  # update the key encoder
                niter += 1

            logging.info("End of epoch {}  loss:{}".format(epoch_counter, loss))

            # save checkpoints
            if (epoch_counter + 1) % self.args.save_freq == 0:
                save_checkpoint({'epoch': epoch_counter + 1, 'arch': self.args.arch, 'optimizer': self.optimizer.state_dict(), 'state_dict': self.model.state_dict()},
                                self.args.log_dir,
                                filename='epoch_{:04d}.pth.tar'.format(epoch_counter + 1))
                logging.info('epoch{:04d}.pth.tar saved!'.format(epoch_counter + 1))

    def L2_loss(self, batch_view_1, batch_view_2):

        # compute query feature
        predictions_from_view_1 = self.model.online_network(batch_view_1)
        predictions_from_view_2 = self.model.online_network(batch_view_2)

        # compute key features
        with torch.no_grad():
            self.model.target_network.fc[3].register_forward_hook(get_activation('projections_from_view_1'))
            self.model.target_network(batch_view_1)
            targets_to_view_1 = torch.squeeze(activation['projections_from_view_1'])

            self.model.target_network.fc[3].register_forward_hook(get_activation('projections_from_view_2'))
            self.model.target_network(batch_view_2)
            targets_to_view_2 = torch.squeeze(activation['projections_from_view_2'])

        loss = self.regression_loss(predictions_from_view_1, targets_to_view_1)
        loss += self.regression_loss(predictions_from_view_2, targets_to_view_2)
        return loss.mean()


def save_checkpoint(state, log_dir, filename):
    filename_path = os.path.join(log_dir, filename)
    torch.save(state, filename_path)
    print(filename + ' has been saved.')


activation = {}


def get_activation(name):
    def hook(model, input, output):
        activation[name] = output

    return hook


if __name__ == '__main__':
    model_names = sorted(name for name in models.__dict__
                         if name.islower() and not name.startswith("__")
                         and callable(models.__dict__[name]))

    model = BYOL(models.__dict__['resnet18'], 128, True).to(torch.device('cpu'))
    print(model)
    print("__" * 50)
    print(model.online_network)
    print("__" * 50)
    print(model.target_network)
