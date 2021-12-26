__all__ = ['Service']

from metadoctor import base as mt
from metadoctor import enumeration as en

class Service(mt.BaseModel):
    __project__ = 'default'
    __instance__ = 'service'
    
    name = mt.Title()
    type = mt.Choice(en.VisitType)
    revisit = mt.Choice(en.Permission)
    
class Invoice(mt.BaseModel):
    services = mt.ArrayOfKeys('Service')
    method = mt.Choice(en.PaymentMethod)
    
class Payment(mt.BaseModel):
    value = mt.Real()
    method = mt.Choice(en.PaymentMethod)