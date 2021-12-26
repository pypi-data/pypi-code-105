import abc
import typing
from datetime import datetime
from typing import Any, Dict, Optional, Tuple  # noqa

import numpy as np
import torch
import tqdm
from torch.utils.tensorboard import SummaryWriter

from supply_depot.cluster import Cluster


class Trainer(metaclass=abc.ABCMeta):
    def __init__(
        self,
        cluster: Cluster = None,
        log_base_path: str = "tensorboard_logs",
        device: torch.device = None,
    ):
        self.cluster = cluster

        self.log_base_path = log_base_path
        self.log_path = "{}/{}".format(log_base_path, datetime.now())
        print("Writing to {}".format(self.log_path))
        self.train_writer = SummaryWriter(self.log_path, flush_secs=10)
        self.device = device
        if self.device is not None:
            self.device = torch.device("cpu")

    def checkpoint(self) -> Any:
        pass

    @abc.abstractmethod
    def train_iter(self, batch_size: int, epoch: int) -> Dict[str, Any]:
        pass

    def pre_train(self):
        pass

    def post_train(self):
        pass

    def emit_metrics(self, metrics: Dict[str, Any], step: int) -> None:
        scalars = metrics.get("scalars", {})
        images = metrics.get("images", {})

        for key in scalars:
            self.train_writer.add_scalar(key, scalars[key], step)
        for key in images:
            self.train_writer.add_images(key, images[key], step, dataformats="NHWC")

    def train(
        self, batch_size: int, epochs: int, reset: bool = True
    ) -> typing.Dict[str, Any]:
        """Main training function, should call train_iter
        """
        if reset:
            self.current_iteration = 0
        self.pre_train()
        bar = tqdm.tqdm(np.arange(epochs))
        for i in bar:
            output = self.train_iter(batch_size, self.current_iteration)
            metrics = output.get("metrics", {})
            self.emit_metrics(metrics, self.current_iteration)
            self.current_iteration += 1

            scalars = metrics.get("scalars", {})
            description = "--".join(["{}:{}".format(k, scalars[k]) for k in scalars])
            bar.set_description(description)
        self.post_train()
        return metrics
