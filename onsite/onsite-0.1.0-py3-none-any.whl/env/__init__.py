from .env_openx import EnvOpenx

def make(path,output_dir):
    env = EnvOpenx(output_dir)
    observation = env.init(path)
    return env,observation