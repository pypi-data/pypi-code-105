from ecdsa.point import Point, INF_POINT

import math

# Helper functions 
def reduce_mod(x:int, p:int) -> int:
    return x % p

def equal_mod(x:int, y:int, p:int) -> bool:
    return reduce_mod(x - y, p) == 0

def inverse_mod(x:int, p:int) -> int:
    if reduce_mod(x, p) == 0:
        return None
    return pow(x, p-2, p)

"""
Eliptic curve formula
y^2 = x^3 + ax + b
"""
class Curve:
    """
    params:
        name -> curve name
        a, b -> curve paramets
        p    -> field(modulo p)
        g    -> generator point
        n    -> order of G (number of points generate by scalar multiplication using the point g)
    """
    def __init__(self, name:str, a:int, b:int, p:int, g:Point, n:int) -> None:
        self.name = name
        self.a = a
        self.b = b
        self.p = p
        self.g = g
        self.n = n

    # https://es.wikipedia.org/wiki/Criptograf%C3%ADa_de_curva_el%C3%ADptica
    def add(self, p1:Point, p2:Point) -> Point:
        if p1 == INF_POINT:
            return p2
        if p2 == INF_POINT:
            return p1

        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y

        # Vertical points
        if equal_mod(x2, x1, self.p) and equal_mod(y2, -y1, self.p):
            return INF_POINT

        if equal_mod(x1, x2, self.p) and equal_mod(y1, y2, self.p):
            u = reduce_mod((3*(x1**2) + self.a), self.p) * inverse_mod((2 * y1), self.p)
        else:
            u = reduce_mod((y2 - y1), self.p) * inverse_mod((x2 - x1), self.p)

        v  = reduce_mod((y1 - u * x1), self.p)
        x3 = reduce_mod((u**2 - x1 - x2), self.p)
        y3 = reduce_mod((-u * x3 - v), self.p) 

        return Point(x3, y3)

    # https://www.youtube.com/watch?v=u1VRbo_fhC8 | double-and-Add
    def scalar_multiplication (self:object, k:int, p:Point) -> Point:
        q = INF_POINT
        while k != 0:
            if k & 1 != 0:
                q = self.add(q, p)
            p = self.add(p, p)
            k >>= 1
        return q
    
    def contain (self, p:Point) -> bool:
        return equal_mod(p.y**2, p.x**3 + self.a * p.x + self.b, self.p)

secp256k1 = Curve(
    "secp256k1", 
    0x0000000000000000000000000000000000000000000000000000000000000000, # A
    0x0000000000000000000000000000000000000000000000000000000000000007, # B
    0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f, # P
    Point(                                                              # G
        0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, # G.x    
        0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8, # G.y
    ),
    0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141  # N
)

p224 = Curve(
    "p224",
    -3,                                                                     # A
    18958286285566608000408668544493926415504680968679321075787234672564,   # B
    26959946667150639794667015087019630673557916260026308143510066298881,   # P
    Point(                                                                  # G
        19277929113566293071110308034699488026831934219452440156649784352033,   # G.x
        19926808758034470970197974370888749184205991990603949537637343198772,   # G.y
    ),
    26959946667150639794667015087019625940457807714424391721682722368061    # N
)
