import os
import time

from halo import Halo


def main():
    parser = parse_arguments_and_environment()
    repo = initialize_repository_object()
    clone_default_code_if_needed(parser, repo)
    remote = get_or_configure_starmart_git_remote(repo, parser)
    if is_deploy(parser):
        remote.push()


def parse_arguments_and_environment():
    import argparse
    from dotenv import load_dotenv
    [load_dotenv(env_file) for env_file in filter(lambda x: x.startswith('.env'), os.listdir())]  # loading .env files
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
    from git import Repo, InvalidGitRepositoryError
    try:
        repo = Repo('.')
    except InvalidGitRepositoryError:
        repo = Repo.init('.')
    return repo


def clone_default_code_if_needed(args, repo):
    # cloning the default repository
    if is_init(args):
        @Halo(text='Cloning default code', spinner='dots')
        def loading():
            if len(list(filter(lambda x: not x.startswith('.'), os.listdir()))) > 0:
                raise ValueError('Directory is not empty. Please initialize on empty directory')
            repo.clone(os.environ['GITHUB_REPO'])
            # starts the git repository without anyting
            repo.remotes.remove(repo.remote('origin'))

        loading()


def get_or_configure_starmart_git_remote(repo, args):
    # checking if there's already a remote called starmart
    remote = None
    for r in repo.remotes:
        if r.name == 'starmart':
            remote = r
            break
    # if there's not, add one
    if remote is None:
        import webbrowser
        from starmart.server.Server import server
        webbrowser.open(f'{os.environ["AUTHENTICATION_HOST"]}/development/login')

        def callback(url):
            authentication_host = os.environ['AUTHENTICATION_HOST']
            if not url.startswith(authentication_host):
                raise ValueError(f'URL does not match the authentication host: {authentication_host}')
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
