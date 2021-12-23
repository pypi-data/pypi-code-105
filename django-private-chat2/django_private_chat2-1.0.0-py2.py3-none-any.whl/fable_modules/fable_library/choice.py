from .types import Union
from .reflection import union_type
from .option import some

def expr_0(gen0, gen1):
    return union_type("FSharp.Core.FSharpResult`2", [gen0, gen1], FSharpResult_2, lambda: [[["ResultValue", gen0]], [["ErrorValue", gen1]]])


class FSharpResult_2(Union):
    def __init__(self, tag=None, *fields):
        super().__init__()
        self.tag = tag | 0
        self.fields = fields
    
    @staticmethod
    def cases():
        return ["Ok", "Error"]
    

FSharpResult_2_reflection = expr_0

def Result_Map(mapping, result):
    if result.tag == 0:
        return FSharpResult_2(0, mapping(result.fields[0]))
    
    else: 
        return FSharpResult_2(1, result.fields[0])
    


def Result_MapError(mapping, result):
    if result.tag == 0:
        return FSharpResult_2(0, result.fields[0])
    
    else: 
        return FSharpResult_2(1, mapping(result.fields[0]))
    


def Result_Bind(binder, result):
    if result.tag == 0:
        return binder(result.fields[0])
    
    else: 
        return FSharpResult_2(1, result.fields[0])
    


def expr_16(gen0, gen1):
    return union_type("FSharp.Core.FSharpChoice`2", [gen0, gen1], FSharpChoice_2, lambda: [[["Item", gen0]], [["Item", gen1]]])


class FSharpChoice_2(Union):
    def __init__(self, tag=None, *fields):
        super().__init__()
        self.tag = tag | 0
        self.fields = fields
    
    @staticmethod
    def cases():
        return ["Choice1Of2", "Choice2Of2"]
    

FSharpChoice_2_reflection = expr_16

def expr_17(gen0, gen1, gen2):
    return union_type("FSharp.Core.FSharpChoice`3", [gen0, gen1, gen2], FSharpChoice_3, lambda: [[["Item", gen0]], [["Item", gen1]], [["Item", gen2]]])


class FSharpChoice_3(Union):
    def __init__(self, tag=None, *fields):
        super().__init__()
        self.tag = tag | 0
        self.fields = fields
    
    @staticmethod
    def cases():
        return ["Choice1Of3", "Choice2Of3", "Choice3Of3"]
    

FSharpChoice_3_reflection = expr_17

def expr_18(gen0, gen1, gen2, gen3):
    return union_type("FSharp.Core.FSharpChoice`4", [gen0, gen1, gen2, gen3], FSharpChoice_4, lambda: [[["Item", gen0]], [["Item", gen1]], [["Item", gen2]], [["Item", gen3]]])


class FSharpChoice_4(Union):
    def __init__(self, tag=None, *fields):
        super().__init__()
        self.tag = tag | 0
        self.fields = fields
    
    @staticmethod
    def cases():
        return ["Choice1Of4", "Choice2Of4", "Choice3Of4", "Choice4Of4"]
    

FSharpChoice_4_reflection = expr_18

def expr_19(gen0, gen1, gen2, gen3, gen4):
    return union_type("FSharp.Core.FSharpChoice`5", [gen0, gen1, gen2, gen3, gen4], FSharpChoice_5, lambda: [[["Item", gen0]], [["Item", gen1]], [["Item", gen2]], [["Item", gen3]], [["Item", gen4]]])


class FSharpChoice_5(Union):
    def __init__(self, tag=None, *fields):
        super().__init__()
        self.tag = tag | 0
        self.fields = fields
    
    @staticmethod
    def cases():
        return ["Choice1Of5", "Choice2Of5", "Choice3Of5", "Choice4Of5", "Choice5Of5"]
    

FSharpChoice_5_reflection = expr_19

def expr_20(gen0, gen1, gen2, gen3, gen4, gen5):
    return union_type("FSharp.Core.FSharpChoice`6", [gen0, gen1, gen2, gen3, gen4, gen5], FSharpChoice_6, lambda: [[["Item", gen0]], [["Item", gen1]], [["Item", gen2]], [["Item", gen3]], [["Item", gen4]], [["Item", gen5]]])


class FSharpChoice_6(Union):
    def __init__(self, tag=None, *fields):
        super().__init__()
        self.tag = tag | 0
        self.fields = fields
    
    @staticmethod
    def cases():
        return ["Choice1Of6", "Choice2Of6", "Choice3Of6", "Choice4Of6", "Choice5Of6", "Choice6Of6"]
    

FSharpChoice_6_reflection = expr_20

def expr_21(gen0, gen1, gen2, gen3, gen4, gen5, gen6):
    return union_type("FSharp.Core.FSharpChoice`7", [gen0, gen1, gen2, gen3, gen4, gen5, gen6], FSharpChoice_7, lambda: [[["Item", gen0]], [["Item", gen1]], [["Item", gen2]], [["Item", gen3]], [["Item", gen4]], [["Item", gen5]], [["Item", gen6]]])


class FSharpChoice_7(Union):
    def __init__(self, tag=None, *fields):
        super().__init__()
        self.tag = tag | 0
        self.fields = fields
    
    @staticmethod
    def cases():
        return ["Choice1Of7", "Choice2Of7", "Choice3Of7", "Choice4Of7", "Choice5Of7", "Choice6Of7", "Choice7Of7"]
    

FSharpChoice_7_reflection = expr_21

def Choice_makeChoice1Of2(x=None):
    return FSharpChoice_2(0, x)


def Choice_makeChoice2Of2(x=None):
    return FSharpChoice_2(1, x)


def Choice_tryValueIfChoice1Of2(x):
    if x.tag == 0:
        return some(x.fields[0])
    
    else: 
        return None
    


def Choice_tryValueIfChoice2Of2(x):
    if x.tag == 1:
        return some(x.fields[0])
    
    else: 
        return None
    


