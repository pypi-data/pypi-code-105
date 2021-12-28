class Config(object):
    def github_repo(self) -> str:
        raise NotImplementedError(f'github_repo not implemented in {self.__name__}')

    def authentication_host(self) -> str:
        raise NotImplementedError(f'authentication_host not implemented in {self.__name__}')

    def git_remote_host(self):
        raise NotImplementedError(f'git_remote_host not implemented in {self.__name__}')

    @classmethod
    def default_config(cls) -> 'Config':
        try:
            from starmart.config.development_config import DevelopmentConfig
            return DevelopmentConfig()
        except ModuleNotFoundError:
            from starmart.config.production_config import ProductionConfig
            return ProductionConfig()
