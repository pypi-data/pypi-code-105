from starmart.config.config import Config


class ProductionConfig(Config):
    def github_repo(self) -> str:
        return 'https://github.com/starmart-io/starmart.git'

    def authentication_host(self) -> str:
        return 'https://starmart.io'
