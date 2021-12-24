from gym.envs.registration import register

register(
    id='thormang-v0',
    entry_point='thormang.envs:ThormangEnv',
)