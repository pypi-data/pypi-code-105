import time
from typing import Callable, Optional, Tuple

import gym
import numpy as np
import torch

from supply_depot.cluster import Execution
from supply_depot.rl import GymAgent


class GymRolloutExecution(Execution):
    def __init__(
        self,
        env: Optional[gym.Env] = None,
        env_name: str = "LunarLander-v2",
        env_creation: Optional[Callable] = None,
        max_env_steps: int = 10 ** 10,
        stop_criteria: Optional[Callable] = None,
        observation_wrapper: Optional[Callable] = None,
        action_wrapper: Optional[Callable] = None,
    ):
        super().__init__()
        self.env = env
        self.env_name = env_name
        self.env_creation = env_creation
        self.max_env_steps = max_env_steps
        self.stop_criteria = stop_criteria
        self.observation_wrapper = observation_wrapper
        self.action_wrapper = action_wrapper

        if self.env is None:
            if self.env_creation is not None:
                self.env = self.env_creation()
            else:
                self.env = gym.make(self.env_name)
            if self.observation_wrapper is not None:
                self.env = self.observation_wrapper(self.env)
            if self.action_wrapper is not None:
                self.env = self.action_wrapper(self.env)

    def execute(
        self, agent: GymAgent = None, render: bool = False, close: bool = False
    ) -> Tuple[np.array, np.array, np.array]:
        """Evaluates  env and model until the env returns "Done".
        Returns:
            xs: A list of observations
            hs: A list of model hidden states per observation
            dlogps: A list of gradients
            drs: A list of rewards.
        """
        if agent is None:
            agent = GymAgent()  # random actions
        with torch.no_grad():
            # Reset the game.
            observation = self.env.reset()
            observations, actions, rewards, dones, rendered_obs = [], [], [], [], []
            done = False
            i = 0
            while not done:
                rendered = None
                if render:
                    rendered = self.env.render(mode="rgb_array")
                    time.sleep(0.01)
                if agent is None:
                    action = self.env.action_space.sample()
                else:
                    action, policy_out = agent.act(observation, self.env.action_space)

                actions.append(action)
                observations.append(observation)
                rendered_obs.append(rendered)
                observation, reward, done, info = self.env.step(action)
                rewards.append(reward)
                dones.append(float(done))
                i += 1
                if i >= self.max_env_steps:
                    done = True
                elif self.stop_criteria is not None:
                    if self.stop_criteria(observation, reward, done, info):
                        done = True

            observations = np.array(observations)
            rendered_obs = np.array(rendered_obs)
            actions = np.array(actions)
            rewards = np.array(rewards)
            dones = np.array(dones)

            return observations, rendered_obs, actions, rewards, dones
