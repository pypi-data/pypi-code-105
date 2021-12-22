from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Numeric
    
class CharFields(Column):
    
    def __init__(self, max_length:int, *args, **kwargs):
        super().__init__(String(max_length), *args, **kwargs)
        
class IntFields(Column):
    
    def __init__(self, *args, **kwargs):
        super().__init__(Integer, *args, **kwargs)
        
class FloatFields(Column):
    
    def __init__(self, *args, **kwargs):
        super().__init__(Float, *args, **kwargs)

class DateTimeFields(Column):
    
    def __init__(self, *args, **kwargs):
        super().__init__(DateTime, *args, **kwargs)
        
class DateFields(Column):
    
    def __init__(self, *args, **kwargs):
        super().__init__(Date, *args, **kwargs)
        
class NumericFields(Column):
    
    def __init__(self, digits:int, decimalDigits:int, *args, **kwargs):
        super().__init__(Numeric(digits, decimalDigits), *args, **kwargs)