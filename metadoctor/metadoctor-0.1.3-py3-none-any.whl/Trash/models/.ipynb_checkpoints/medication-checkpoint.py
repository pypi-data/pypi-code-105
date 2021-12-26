__all__ = ['ActiveDrug', 'ActiveDrugSet', 'BrandDrug']

from metadoctor import model
from metadoctor import field
from metadoctor import enumeration as enu
from metadoctor import utils


class ActiveDrug(model.BaseModel):
    __project__ = 'default'
    __instance__ = 'active_drug'
    
    name = field.Title(title='Composto Ativo')


class ActiveDrugSet(model.BaseModel):
    __project__ = 'default'
    __instance__ = 'active_drug_set'
    
    active_drug = field.Title(title='Composto Ativo')
    strength = field.Real()
    measure_unit = field.Choice(enu.DosageUnit)


class BrandDrug(model.BaseModel):
    __project__ = 'default'
    __instance__ = 'brand_drug'

    name = field.Title(title='Marca')
    drugs = field.String(title='Compostos Ativos')
    sets = field.String(title='Apresentações')
    content = field.String(title='Quantidade')
    recipe = field.Choice(enu.RecipeType, default=enu.RecipeType.C, title='Tipo de Receita')
    pharmaceutical = field.Choice(enu.Pharmaceutical, title='Fabricante')
    
