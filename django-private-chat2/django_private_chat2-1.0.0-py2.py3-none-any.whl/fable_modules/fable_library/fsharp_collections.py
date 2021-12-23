from .util import (structural_hash, equals, physical_hash, compare)

def HashIdentity_FromFunctions(hash_1, eq):
    class ObjectExpr2:
        def Equals(self, x, y=None, hash_1=hash_1, eq=eq):
            return eq(x, y)
        
        def GetHashCode(self, x_1=None, hash_1=hash_1, eq=eq):
            return hash_1(x_1)
        
    return ObjectExpr2()


def HashIdentity_Structural():
    return HashIdentity_FromFunctions(lambda obj=None: structural_hash(obj), lambda e1, e2=None: equals(e1, e2))


def HashIdentity_Reference():
    return HashIdentity_FromFunctions(lambda obj=None: physical_hash(obj), lambda e1, e2=None: e1 is e2)


def ComparisonIdentity_FromFunction(comparer):
    class ObjectExpr4:
        def Compare(self, x, y=None, comparer=comparer):
            return comparer(x, y)
        
    return ObjectExpr4()


def ComparisonIdentity_Structural():
    return ComparisonIdentity_FromFunction(lambda e1, e2=None: compare(e1, e2))


