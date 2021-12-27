from .env_openx import EnvOpenx

def make(path,output_dir,plot=False):
    env = EnvOpenx(output_dir,plot=plot)
    observation = env.init(path)
    return env,observation