class PublicKey:
    def __init__(self:object, p:object, curve:object) -> None:
        self.p = p
        self.curve = curve

    def to_string (self:object, encoded=False) -> str:
        base = 2 * (1 + len("%x" % self.curve.n))

        x = str(hex(self.p.x)).zfill(base)
        y = str(hex(self.p.y)).zfill(base)

        if encoded:
            return "0004" + x + y
        return x + y 

    def from_strin(self:object) -> str:
        pass

    def to_der (self:object) -> str:
        pass

    def from_der (self:object) -> str:
        pass

    def __str__(self:object) -> str:
        return f"curve: {self.curve.name}\npoint: {self.p}"
