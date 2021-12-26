import typing
from contextlib import contextmanager
from typing import Any

import numpy as np
import torch

# import torch.nn.functional as F
from gym.spaces import (  # noqa
    Box,
    Dict,
    Discrete,
    MultiBinary,
    MultiDiscrete,
    Space,
    Tuple,
)
from torch.distributions.categorical import Categorical

# internal
from supply_depot.rl import GymAgent


class MLPAgent(GymAgent, torch.nn.Module):
    def __init__(self, observation_shape: Any, action_shape: Any, net=None):
        super(MLPAgent, self).__init__()
        self.observation_shape = observation_shape
        self.action_shape = action_shape

        self.input_dims = np.prod(self.observation_shape)
        self.output_dims = np.prod(self.action_shape)

        self.net = net
        if self.net is not None:
            self.net = torch.nn.Sequential(
                torch.nn.Linear(self.input_dims, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, self.output_dims),
            )

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.net(x)
        return x.view(x.size(0), *self.action_shape)

    def policy(self, obs: Any):
        return {"action_logits": self.forward(obs)}

    def preprocess_observation_func(self, observation):
        return torch.from_numpy(observation).unsqueeze(0).float()

    def act_discrete(
        self, policy_out: typing.Dict[str, Any], action_space: Discrete
    ) -> int:
        action_logits = policy_out.get("action_logits", None)
        action_probs = policy_out.get("action_probs", None)
        if action_logits is not None:
            dist = Categorical(logits=action_logits)
        else:
            dist = Categorical(probs=action_probs)
        return dist.sample().item()

    @contextmanager
    def evaluate(self):
        with torch.no_grad():
            try:
                yield
            finally:
                pass
