class Signature:
    def __init__(self:object, r:int, s:int, r_id:int):
        self.r = r
        self.s = s
        self.r_id = r_id

    def __str__(self:object) -> str:
        return f"r: {self.r} \ns: {self.s}\nr_id: {self.r_id}"
