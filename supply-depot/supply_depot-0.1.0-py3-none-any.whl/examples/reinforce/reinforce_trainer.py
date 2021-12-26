from typing import Any, Dict, Optional, Tuple  # noqa

import numpy as np
import torch
import torch.optim as optim
from einops import rearrange
from torch.distributions.categorical import Categorical

from supply_depot.cluster import Cluster
from supply_depot.examples.reinforce import MLPAgent
from supply_depot.rl import GymRolloutExecution
from supply_depot.trainer import Trainer
from supply_depot.utils import draw_text


class ReinforceTrainer(Trainer):
    def __init__(
        self,
        agent: MLPAgent,
        lr: float = 0.001,
        norm_gradient: bool = True,
        num_workers: int = 4,
        env_name: str = "LunarLander-v2",
        cluster: Cluster = Cluster(),
        log_base_path: str = "tensorboard_logs",
        device: torch.device = None,
    ):
        super(ReinforceTrainer, self).__init__(cluster, log_base_path, device)
        self.agent = agent
        self.lr = lr
        self.norm_gradient = norm_gradient
        self.num_workers = num_workers
        self.env_name = env_name
        self.rollout_workers = [
            self.cluster.create_execution(GymRolloutExecution, env_name=self.env_name)
            for _ in range(self.num_workers)
        ]
        self.optimizer = optim.Adam(self.agent.parameters(), lr=self.lr)

    def get_rollouts(self, num_rollouts: int = 5, render: bool = False):
        cpu = torch.device("cpu")
        args = [
            {"agent": self.agent.to(cpu), "render": render} for _ in range(num_rollouts)
        ]
        output = self.cluster.execute(self.rollout_workers, args)
        self.agent = self.agent.to(self.device)
        return output

    def discount_reward(self, rews):
        # dr = [0] * (len(reward_arr) + 1)
        # for i in range(len(reward_arr) - 1, -1, -1):
        #     dr[i] = reward_arr[i] + self.gamma * dr[i + 1]
        # dr = np.array(dr[: len(reward_arr)])
        # return dr
        n = len(rews)
        rtgs = np.zeros_like(rews)
        for i in reversed(range(n)):
            rtgs[i] = rews[i] + (rtgs[i + 1] if i + 1 < n else 0)
        return rtgs

    def emit_metrics(self, metrics: Dict[str, Any], step: int) -> None:
        scalars = metrics.get("scalars", {})
        images = metrics.get("images", None)
        for key in scalars:
            self.train_writer.add_scalar(key, scalars[key], step)
        if step % 20 == 0:
            observations, rendered, actions, rewards, dones = self.get_rollouts(
                1, render=True
            )[0]
            images = []
            for i in range(rendered.shape[0]):
                im = rendered[i]
                texted_image = draw_text(
                    img=np.copy(im), text="step: {}".format(i), pos=(5, 5),
                )
                texted_image = draw_text(
                    img=np.copy(texted_image),
                    text="reward: {}".format(rewards[i]),
                    pos=(5, 25),
                )
                images.append(texted_image)
            images = np.expand_dims(images, 0)
            self.train_writer.add_video(
                "rollout_video",
                rearrange(images, "b t h w c -> b t c h w"),
                global_step=step,
                fps=32,
            )

    def train_iter(self, batch_size, epoch) -> Dict[str, Any]:
        rollouts = self.get_rollouts(batch_size)[0]
        observations, rendered_obs, actions, rewards, dones = rollouts

        discounted_rewards = self.discount_reward(rewards)
        discounted_rewards = discounted_rewards - np.mean(discounted_rewards)
        discounted_rewards = discounted_rewards / (np.std(discounted_rewards) + 1e-10)

        torch_observations = torch.from_numpy(observations).float().to(self.device)
        torch_rewards = torch.from_numpy(discounted_rewards).float().to(self.device)
        torch_actions = torch.from_numpy(actions).to(self.device)

        out = self.agent.policy(torch_observations)
        logits = out["action_logits"]
        dist = Categorical(logits=logits)
        log_probs = dist.log_prob(torch_actions)

        self.optimizer.zero_grad()
        loss = -1 * torch.sum(torch_rewards * log_probs)

        if self.norm_gradient:
            for p in self.agent.parameters():
                if p.grad is not None:
                    p.grad /= torch.norm(p.grad) + 1e-10

        loss.backward()
        self.optimizer.step()

        grad_dict = {}
        for n, W in self.agent.named_parameters():
            if W.grad is not None:
                grad_dict["{}_grad".format(n)] = float(torch.sum(W.grad).item())

        train_dict = {
            "out": None,
            "metrics": {
                "scalars": {
                    "loss": loss.item(),
                    "sum_reward": np.sum(rewards),
                    "average_reward": np.mean(rewards),
                    "epoch": epoch,
                    **grad_dict,
                },
            },
            "loss": loss.item(),
        }
        return train_dict
