from ecdsa.point import INF_POINT
from ecdsa.public_key import PublicKey
from ecdsa.private_key import PrivateKey
from ecdsa.curves import reduce_mod, inverse_mod
from ecdsa.signature import Signature

from hashlib import sha256
from random import randint

# Error codes
ERROR_NOT_SAME_HASH_FUNCTION       = 0x0001
ERROR_NOT_SAME_CURVE               = 0x0002
ERROR_SIGNATURES_VALUES_NOT_VALID  = 0x0003
ERROR_PRIVATE_KEY_VALUES_NOT_VALID = 0x0004

# https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
def sign (private_key:PrivateKey, message:bytes) -> Signature:
    curve  = private_key.curve
    secret = private_key.secret

    e = int(sha256(message).hexdigest(), 16)
    r, s = 0, 0
    while r == 0 or s == 0:
        k  = randint(1, curve.n-1)
        kp = curve.scalar_multiplication(k, curve.g)
        
        r  = reduce_mod(kp.x, curve.n)
        s  = reduce_mod(inverse_mod(k, curve.n) * (e + r*secret), curve.n)
    
    r_id = kp.y & 1
    if kp.y > curve.n:
        r_id += 2
    
    return Signature(r, s, r_id)

def verify (public_key:PublicKey, message:bytes, signature:Signature) -> bool:
    curve = public_key.curve
    q = public_key.p
    
    r = signature.r
    s = signature.s

    e = int(sha256(message).hexdigest(), 16)

    iv = inverse_mod(s, curve.n)
    u1 = reduce_mod(e * iv, curve.n)
    u2 = reduce_mod(r * iv, curve.n)

    p1 = curve.scalar_multiplication(u1, curve.g)
    p2 = curve.scalar_multiplication(u2, q)

    p3 = curve.add(p1, p2)
    
    return p3.x % curve.n == r
