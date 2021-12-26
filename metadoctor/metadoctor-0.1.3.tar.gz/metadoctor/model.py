from metadoctor.base import *
from metadoctor.enumeration import *
from metadoctor import utils 

age = utils.age
now = utils.now 
today = utils.today
only_digits = utils.only_digits

class Person(BaseModel):
    """
    Profile.Person Class
    """
    __project = Project.USER
    __singular = 'Pessoa'
    __plural = 'Pessoas'

    fullname = Title(title='Nome completo')

    class Gender(BaseEnum):
        M = 'Masculino'
        F = 'Feminino'
        N = 'Não Binário'

    gender = Choice(Gender, title='Região')
    birthdate = Date(title='Nascimento')
    cpf = String(title='CPF', required=False)

    def __init__(self, fullname, gender, birthdate, cpf=None, **kwargs) -> None:
        super().__init__(fullname=fullname, gender=gender, birthdate=birthdate, cpf=cpf, **kwargs)
        if self.cpf:
            self.cpf = only_digits(self.cpf)
            assert len(self.cpf) == 11, 'CPF deve ter exatamente 11 dígitos. ' + str(len(self.cpf)) + ' foram encontrados.'

    @property
    def name(self):
        return self.fullname 

    @property
    def bdate(self):
        return self.birthdate 
    
    
    @property
    def age(self):
        return age(self.birthdate)
    
    
class User(BaseModel):
    """
    User Class
    """
    __project = Project.USER
    __singular = 'Usuário'
    __plural = 'Usuários'

    username: str = String(default='Indefinido', title='Nome de Usuário')
    is_admin = Boolean(title='Perfil Administrador', readonly=True)
    created = DateTime(factory=lambda: now().isoformat(), exclude=True, readonly=True)

    def __init__(self, username, is_admin=False, created=None, **kwargs) -> None:
        super().__init__(username=username, is_admin=is_admin, created=created,  **kwargs)
        
        
    def _autokey(self):
        return remove_accents(self.username)
        
class Profile(BaseModel):
    """
    Profile Class
    """
    __project = Project.USER
    __singular = 'Perfil'
    __plural = 'Perfis'
    
    class ProfileType(BaseEnum):
        DOCTOR = 'Médico'
        THERAPIST = 'Terapeuta'
        EMPLOYEE = 'Funcionário'
        ASSISTANT = 'Assistente'
        PATIENT = 'Paciente'
        RELATIVE = 'Familiar'

    type =  SelectEnum(ProfileType, default=ProfileType.PATIENT, title='Tipo de Perfil')
    person = Instance(Person, title='Pessoa')
    user = Instance(User, required=False, title='Usuário')
    
    def __str__(self):
        return f'{self.person.fullname} ({self.type})'
    
class PatientInfo(BaseModel):
    '''Profile.Patient Class'''
    __project = Project.CLIENT
    __pt_singular = 'Paciente'
    __plural = 'Pacientes'

    relatives = ArrayOfKeys('Profile', 'user', title='Familiares', required=False)
    health_plan = SemicolonStrToList(title='Planos de Saúde', required=False)
    curator = Key('Profile', 'user', required=False)
    notes = Text(required=False)

    def __init__(self, relatives=None, health_plan=None, curator=None,notes=None, **kwargs):
        super().__init__(relatives=relatives, health_plan=health_plan, curator=curator, notes=notes, **kwargs)
        

    
    
class ProviderInfo(BaseModel):
    '''Profile.Provider Class'''
    __project = Project.USER
    __singular = 'Profissional'
    __plural = 'Profissionais'

    class Graduation(BaseEnum):
        MED = 'Medicina'
        PSY = 'Psicologia'
        FIS = 'Fisioterapia'
        NUR = 'Enfermagem'
        FON = 'Fonoaudiologia'
        
    profile = Instance(Profile)

    graduation = Choice(Graduation, default=Graduation.MED)
    licence = String(title='Registro Profissional')
    specialties = Array(required=False, exclude=True)
    notes = Text(required=False, exclude=True)

    def __init__(self, graduation, licence, specialties=None, notes=None, **kwargs):
        super().__init__(graduation=graduation, licence=licence, specialties=specialties, notes=notes, **kwargs)
        
    
class EmployeeInfo(BaseModel):
    '''Profile.Employee Class'''
    __project = Project.CLIENT
    __singular = 'Funcionário'
    __plural = 'Funcionários'
    
    profile = Instance(Profile)
    functions = SemicolonStrToList()
    salary = Real(title='Salário', exclude=True)
    skills = SemicolonStrToList(required=False)
    notes = Text(required=False)
            
        
class Address(BaseModel):
    """
    Profile.Address Class
    """
    __project = Project.CLIENT
    __singular = 'Endereço'
    __plural = 'Endereços'

    class City(BaseModel):
        __project = Project.BASE
        __singular = 'Cidade'
        __plural = 'Cidades'
        __table = 'City'

        name = Title()
        region = KeyData('Region', 'base')
        
    profile = Instance(Profile)
    city = Instance(City, title='Cidade')
    cep = String(title='CEP', required=False)
    street = Title(title='Logradouro', required=False)
    number = String(title='Número', required=False)
    complement = String(title='Complemento', required=False)
    district = Title(title='Bairro', required=False)
    notes = Text(required=False)

    def __init__(self, profile, city, cep=None, street=None, number=None, complement=None, district=None,  notes=None, **kwargs) -> None:
        super().__init__(profile=profile, city=city, cep=cep, street=street, number=number, complement=complement, district=district,  notes=notes, **kwargs)
        
class Contact(BaseModel):
    """
    Profile.Contact Class
    """
    __project = Project.CLIENT
    __singular = 'Contato'
    __plural = 'Contatos'
    
    class Type(StrEnum):
        TELEPHONE = 'Telefone Fixo'
        MOBILE = 'Telefone Celular'
        EMAIL = 'Email Pessoal'
    
    profile = Instance(Profile)
    type = Choice(Type, default=Type.MOBILE)
    value = String()
    notes = Text(required=False)
    
    
    def __init__(self, profile, type, value, notes=None, **kwargs):
        super().__init__(profile=profile, type=type, value=value, notes=notes, **kwargs)

            
class Log(BaseModel):
    '''Log Register class'''
    __project = Project.LOG
    __singular = 'Registro'
    __plural = 'Registros'
    
    datetime = DateTime(factory=now)
    profile = Instance(Profile)
    path = String()
    method = SelectEnum(Profile.ProfileType)
    result = String()