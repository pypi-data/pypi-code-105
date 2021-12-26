__all__ = ['ActiveDrug', 'ActiveDrugSet', 'BrandDrug']

from metadoctor import base as mt
from metadoctor import enumeration as en
from metadoctor import utils


class ActiveDrug(mt.BaseModel):
    __project__ = 'base'
    __instance__ = 'active_drug'
    
    name = mt.Title(title='Composto Ativo')


class ActiveDrugSet(mt.BaseModel):
    __project__ = 'base'
    __instance__ = 'active_drug_set'
    
    active_drug = mt.Title(title='Composto Ativo')
    strength = mt.Real()
    measure_unit = mt.Choice(en.DosageUnit)


class BrandDrug(mt.BaseModel):
    __project__ = 'base'
    __instance__ = 'brand_drug'

    name = mt.Title(title='Marca')
    drugs = mt.String(title='Compostos Ativos')
    sets = mt.String(title='Apresentações')
    content = mt.String(title='Quantidade')
    recipe = mt.Choice(en.RecipeType, default=en.RecipeType.C, title='Tipo de Receita')
    pharmaceutical = mt.Choice(en.Pharmaceutical, title='Fabricante')
    
