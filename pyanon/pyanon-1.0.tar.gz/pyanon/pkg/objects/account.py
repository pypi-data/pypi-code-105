class Account:
    def __init__(self, 
                login: str, 
                password: str,
                id: str,
                email: str,
                rocketId: str,
                rocketKey: str,
                isDisabled: bool,
                isGcmMissing: bool,
                level: int,
                token: str) -> None:
        self.login: str = login
        self.password: str = password
        self.id: str = id
        self.email: str = email
        self.rocketId: str = rocketId
        self.rocketKey: str = rocketKey
        self.isDisabled: bool = isDisabled
        self.isGcmMissing: bool = isGcmMissing
        self.level: int = level
        self.token: str = token
        self.rocketId: str = None
        self.rocketToken: str = None