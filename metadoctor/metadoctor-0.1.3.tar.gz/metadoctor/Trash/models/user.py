# __all__ = [
#     'User'
# ]

# from metadoctor.model import BaseModel 
# from metadoctor.enumeration import BaseEnum
# from metadoctor import field


# class User(BaseModel):
#     __project__ = 'users'
#     __pt_singular__ = 'Usuário'
#     __pt_plural__ = 'Usuários'
#     class Scope(BaseEnum):
#         PUBLIC = 'Público'
#         PROVIDER = 'Provedor'
#         PATIENT = 'Paciente'
#         ASSISTANT = 'Assistente'
#     scope: str = field.Choice(Scope, default=Scope.PUBLIC, title='Escopo')
#     class YesOrNo(BaseEnum):
#         YES = 'Sim'
#         NO = 'Não'
#     is_admin: YesOrNo = field.Choice(YesOrNo, default=YesOrNo.NO, title='Perfil Administrador', readonly=True)
#     username: str = field.String(default='Indefinido', title='Nome de Usuário')