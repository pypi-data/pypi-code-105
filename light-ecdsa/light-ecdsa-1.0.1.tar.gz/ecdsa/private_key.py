from ecdsa.curves import secp256k1
from ecdsa.public_key import PublicKey

from ecdsa.utils import File

from random import randint

class PrivateKey():
    def __init__(self, curve=secp256k1, secret=None):
        self.curve = curve
        self.secret = secret or randint(1, curve.n-1)

    def generate_public_key(self):
        public_key_point = self.curve.scalar_multiplication(self.secret, self.curve.g)
        public_key = PublicKey(public_key_point, self.curve)

        return public_key

    def load_from_pem_file(self, path:str):
        pem_file_data = File.read(path)
        pem = None # base64.decode(pem_file.split("\n")[0])

    def to_string(self) -> str:
        pass

    def to_pem(self) -> str:
        pass

    def __str__(self):
        return f"curve:  {self.curve.name}\nsecret: {hex(self.secret)}"
