from .util import (equals, structural_hash, dispose, ignore)
from .fsharp_collections import (ComparisonIdentity_Structural, HashIdentity_Structural)
from .system_text import StringBuilder__Append_Z721C83C5

class ObjectExpr2:
    def System_Collections_IEqualityComparer_Equals541DA560(self, x, y):
        return equals(x, y)
    
    def System_Collections_IEqualityComparer_GetHashCode4E60E31B(self, x_1):
        return structural_hash(x_1)
    

LanguagePrimitives_GenericEqualityComparer = ObjectExpr2()

class ObjectExpr3:
    def System_Collections_IEqualityComparer_Equals541DA560(self, x, y):
        return equals(x, y)
    
    def System_Collections_IEqualityComparer_GetHashCode4E60E31B(self, x_1):
        return structural_hash(x_1)
    

LanguagePrimitives_GenericEqualityERComparer = ObjectExpr3()

def LanguagePrimitives_FastGenericComparer():
    return ComparisonIdentity_Structural()


def LanguagePrimitives_FastGenericComparerFromTable():
    return ComparisonIdentity_Structural()


def LanguagePrimitives_FastGenericEqualityComparer():
    return HashIdentity_Structural()


def LanguagePrimitives_FastGenericEqualityComparerFromTable():
    return HashIdentity_Structural()


def Operators_Failure(message):
    return Exception(message)


def Operators_FailurePattern(exn):
    return str(exn)


def Operators_NullArg(x):
    raise Exception(x)


def Operators_Using(resource, action):
    try: 
        return action(resource)
    
    finally: 
        if equals(resource, None):
            pass
        
        else: 
            dispose(resource)
        
    


def Operators_Lock(_lockObj, action):
    return action()


def ExtraTopLevelOperators_LazyPattern(input):
    return input.Value


def PrintfModule_PrintFormatToStringBuilderThen(continuation, builder, format):
    def append(s, continuation=continuation, builder=builder, format=format):
        ignore(StringBuilder__Append_Z721C83C5(builder, s))
        return continuation()
    
    return format.cont(append)


def PrintfModule_PrintFormatToStringBuilder(builder, format):
    def arrow_7(builder=builder, format=format):
        ignore()
    
    return PrintfModule_PrintFormatToStringBuilderThen(arrow_7, builder, format)


