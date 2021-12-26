__all__ = ['Organ', 'Cid10']

from metadoctor import base as mt
from metadoctor import enumeration as en

class Organ(mt.BaseModel):
    __project__ = 'default'
    __instance__ = 'organ'
    
    name = mt.Title(title='Nome do Órgão')
    system = mt.Choice(en.BodySystem, title='Sistema')
    
    
class Cid10(mt.BaseModel):
    __project__ = 'default'
    __instance__ = 'cid10'
    
    code = mt.String()
    title = mt.String(exclude=True)