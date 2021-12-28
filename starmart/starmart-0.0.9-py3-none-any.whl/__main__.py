import argparse
import webbrowser

from git import Repo, InvalidGitRepositoryError
from halo import Halo

from starmart.config.config import Config


def main():
    config = Config.default_config()
    args = parse_arguments_and_environment()
    repo = initialize_repository_object(args, config)
    clone_default_code_if_needed(args, repo, config)
    remote = get_or_configure_starmart_git_remote(repo, args, config)
    if is_deploy(args):
        remote.push()


def parse_arguments_and_environment():
    # configuring arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs=1, help='Run init on a new project, or deploy to push the code', default='None')
    args = parser.parse_args()
    if args.action[0] not in ['deploy', 'init']:
        raise ValueError('Action should be deploy or init')
    return args


def initialize_repository_object(args, config: Config):
    if is_init(args):
        return clone_default_code_if_needed(config)
    elif is_deploy(args):
        try:
            return Repo('.')
        except InvalidGitRepositoryError:
            raise ValueError('Github repository not initialized. Call starmart init before calling starmart deploy.')
    else:
        raise ValueError('Action should be deploy or init')


@Halo(text='Cloning starter code repo', spinner='dots')
def clone_default_code_if_needed(config: Config):
    return Repo.clone_from(config.github_repo(), '.')


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
