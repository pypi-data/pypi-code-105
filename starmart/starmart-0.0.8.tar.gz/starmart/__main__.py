import os
import time
import argparse
import webbrowser
from halo import Halo
from starmart.config.config import Config
from git import Repo, InvalidGitRepositoryError


def main():
    config = Config.default_config()
    parser = parse_arguments_and_environment()
    repo = initialize_repository_object()
    clone_default_code_if_needed(parser, repo, config)
    remote = get_or_configure_starmart_git_remote(repo, parser, config)
    if is_deploy(parser):
        remote.push()


def parse_arguments_and_environment():
    # configuring arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs=1, help='Run init on a new project, or deploy to push the code', default='None')
    args = parser.parse_args()
    if args.action[0] == 'test':
        spinner = Halo(text='Testing', spinner='dots')
        spinner.start()
        time.sleep(3)
        spinner.stop()
        print('starmart works')
        exit(0)
    return args


@Halo(text='Initializing git repo', spinner='dots')
def initialize_repository_object():
    try:
        repo = Repo('.')
    except InvalidGitRepositoryError:
        repo = Repo.init('.')
    return repo


def clone_default_code_if_needed(args, repo: Repo, config: Config):
    # cloning the default repository
    if is_init(args):
        @Halo(text='Cloning default code', spinner='dots')
        def loading():
            if len(list(filter(lambda x: not x.startswith('.'), os.listdir()))) > 0:
                raise ValueError('Directory is not empty. Please initialize on empty directory')
            repo.clone(config.github_repo())
            # starts the git repository without anyting
            repo.remotes.remove(repo.remote('origin'))

        loading()


def get_or_configure_starmart_git_remote(repo, args, config: Config):
    # checking if there's already a remote called starmart
    remote = None
    for r in repo.remotes:
        if r.name == 'starmart':
            remote = r
            break
    # if there's not, add one
    if remote is None:
        from starmart.server.Server import server
        webbrowser.open(f'{config.authentication_host()}/development/login')

        def callback(url):
            remote_host = 'https://gitlab.com/starmart'
            if not url.startswith(remote_host):
                raise ValueError(f'URL does not match the authentication host: {remote_host}')
            remote = repo.create_remote('starmart', url=url)
            if is_deploy(args):
                spinner = Halo(text='Pushing code', spinner='dots')
                spinner.start()
                remote.push()
                spinner.stop()
                print('Happy coding!')
                exit(0)  # this is needed to exit flask server

        # this blocks because of the server. that's why I set a callback
        server(callback)
    return remote


def is_action(args, action):
    return args.action[0] == action


def is_deploy(args):
    return is_action(args, 'deploy')


def is_init(args):
    return is_action(args, 'init')


if __name__ == '__main__':
    main()
