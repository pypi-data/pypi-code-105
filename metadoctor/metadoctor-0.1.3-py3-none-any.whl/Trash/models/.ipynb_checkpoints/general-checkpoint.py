__all__ = [
    'Contact', 
    'Professional',
    'Address',
    'Region',
    'City'
    ]

from metadoctor import base as mt
from metadoctor import enumeration as en
from metadoctor.db import connection


class Region(mt.BaseModel):
    __table__ = 'Region'
    __project__ = 'base'
    __pt_singular__ = 'Região'
    __pt_plural__ = 'Regiões'
    name = mt.Title()
    abbrev = mt.String()
    cowntry = mt.Choice(en.Cowntry)

    def __init__(self, name, abbrev, cowntry, **kwargs) -> None:
        super().__init__(name=name, abbrev=abbrev, cowntry=cowntry, **kwargs)


class City(mt.BaseModel):
    __table__ = 'City'
    __project__ = 'base'
    __pt_singular__ = 'Cidade'
    __pt_plural__ = 'Cidades'
    
    name = mt.Title(title='Nome')
    region = mt.KeyData(*Region.table_project())
    
    def __init__(self, name, region, **kwargs) -> None:
        super().__init__(name=name, region=region, **kwargs)
        
    def __str__(self):
        return f'{self.name}/{self.region.get("abbrev")}'

    
class Address(mt.BaseModel):
    __table__ = 'Address'
    __project__ = 'client'
    __pt_singular__ = 'Endereço'
    __pt_plural__ = 'Endereços'
    
    street = mt.Title(title='Logradouro', required=False)
    number = mt.String(title='Número', required=False)
    complement = mt.String(title='Complemento', required=False)
    district = mt.Title(title='Bairro', required=False)
    cep = mt.String(title='CEP', required=False)
    city = mt.KeyData(*City.table_project(), title='Cidade')
    
    def __init__(self, street, number, complement, district, cep, city, **kwargs) -> None:
        super().__init__(street=street, number=number, complement=complement, district=district, cep=cep, city=city, **kwargs)


class Contact(mt.BaseModel):
    __pt_singular__ = 'Contato'
    __pt_plural__ = 'Contatos'
    telephones = mt.Array(title='Telefones', placeholder='números de telefone separados por ponto e vírgula (;)')
    email = mt.String(required=False, title='Email')
    
    def __init__(self, telephones, email, **kwargs) -> None:
        super().__init__(telephones=telephones, email=email, **kwargs)


class Professional(mt.BaseModel):
    licence = mt.String(title='Licença Profissional')
    profession = mt.Choice(en.Profession, title='Profissão')
    specialties = mt.SemicolonStrToList(title='Especialidades', placeholder='separados por ponto e vírgular (;)', required=False)

    def __init__(self, licence, profession, specialties, **kwargs) -> None:
        super().__init__(licence=licence, profession=profession, specialties=specialties, **kwargs)