__all__ = [
    'Person',
    'Patient',
    'Doctor',
    'Psychoterapist',
    'Physiotherapist',
    'Nurse',
    'Assistant',
    'Relative',
    'Employee',
    'Profile'
]

from collections import namedtuple
from metadoctor import base as mt
from metadoctor import enumeration

from metadoctor.db import Connection 
from metadoctor.models.general import Contact, Professional, City


connection = Connection()
userdb = connection.user 
basedb = connection.base 
clientdb = connection.client 
logdb = connection.log

BaseEnum = enumeration.BaseEnum
        
class Person(mt.BaseModel):
    __project__ = 'user'
    __pt_singular__ = 'Pessoa'
    __pt_plural__ = 'Pessoas'
    __table__ = 'Person'
    
    fullname = mt.Title(title='Nome completo')
    class Gender(BaseEnum):
        M = 'Masculino'
        F = 'Feminino'
        N = 'Não Binário'
    gender = mt.Choice(Gender, title='Região')
    birthdate = mt.Date(title='Nascimento')
    cpf = mt.String(title='CPF', required=False)
    
    
    def __init__(self, fullname, gender, birthdate, cpf=None, **kwargs) -> None:
        super().__init__(fullname=fullname, gender=gender, birthdate=birthdate, cpf=cpf, **kwargs)
        
    @property
    def name(self):
        return self.fullname 
    
    @property
    def bdate(self):
        return self.birthdate 

    
class Profile(mt.BaseModel):
    __table__ = 'Profile'
    __pt_singular__ = 'Perfil'
    __project__ = 'user'
    
    person_key = mt.String()
    telephones = mt.SemicolonStrToList(title='Telefones')
    addresses = mt.ArrayOfKeys('Address', 'base')
    
    
    
    def __init__(self, model_table, model_key, model_project=None,  **kwargs) -> None:
        super().__init__(model_table=model_table, model_key=model_key, model_project=model_project,**kwargs)
        
    async def person(self):
        async with userdb.Get('Person', self.person_key) as result:
            return Person(**result)
        
#     async def from_db(self, connection = connection):
#         async with getattr(connection, self.model_project).Get(self.model_table, self.model_key) as result:
#             if result:
#                 return namedtuple(self.model_table, ' '.join(result.keys()))(**result)
#             return None
        

class Patient(Person):
    __table__ = 'Patient'
    __pt_singular__ = 'Paciente'
    __pt_plural__ = 'Pacientes'
    __project__ = 'client'


class Doctor(Person):
    __table__ = 'Doctor'
    __pt_singular__ = 'Médico'
    __pt_plural__ = 'Médicos'
    __project__ = 'client'
    
    licence = mt.String()
    
    
    def __init__(self, fullname, gender, birthdate, cpf, **kwargs) -> None:
        kwargs.pop('profession', None)
        kwargs['profession'] = 'Medicina'
        super().__init__(fullname, gender, birthdate, licence=licence, **kwargs)
        
    def __str__(self) -> str:
        return f'Dra. {self.fullname} ({self.licence})' if str(self.gender).startswith('F') else f'Dr. {self.fullname} ({self.licence})'

class Nurse(Person, Professional, Contact):
    def __init__(self, fullname, gender, birthdate, licence, **kwargs) -> None:
        kwargs.pop('profession', None)
        kwargs['profession'] = 'Enfermagem'
        super().__init__(fullname, gender, birthdate, licence=licence, **kwargs)
        
    def __str__(self) -> str:
        return f'Dra. {self.fullname} ({self.licence} | {enumeration.Profession[self.profession]})' if str(self.gender).startswith('F') else f'Dr. {self.fullname} ({self.licence} | {enumeration.Profession[self.profession]})'

class Psychoterapist(Person, Professional, Contact):
    def __init__(self, fullname, gender, birthdate, licence, **kwargs) -> None:
        kwargs.pop('profession', None)
        kwargs['profession'] = 'Psicologia'
        super().__init__(fullname, gender, birthdate, licence=licence, **kwargs)
        
    def __str__(self) -> str:
        return f'Dra. {self.fullname} ({self.licence})' if str(self.gender).startswith('F') else f'Dr. {self.fullname} ({self.licence})'


class Physiotherapist(Person, Professional, Contact):
    def __init__(self, fullname, gender, birthdate, licence, **kwargs) -> None:
        kwargs.pop('profession', None)
        kwargs['profession'] = 'Fisioterapia'
        super().__init__(fullname, gender, birthdate, licence=licence, **kwargs)
        
    def __str__(self) -> str:
        return f'Dra. {self.fullname} ({self.licence})' if str(self.gender).startswith('F') else f'Dr. {self.fullname} ({self.licence})'


class Assistant(Person, Contact):
    pass 


class Employee(Person, Contact):
    pass 


class Relative(Person, Contact):
    pass 





