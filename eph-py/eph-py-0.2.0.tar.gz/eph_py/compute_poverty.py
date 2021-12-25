import pandas as pd
import datetime
from get_micro_data import get_micro_data
from get_poverty_lines import get_poverty_lines


def _get_ae():
    return pd.read_csv('csv_data/adulto_equivalente.csv')


def _compute_situ(row):
    if row['ITF'] is None:
        return None
    if row['ITF'] < row['CBA_hogar']:
        return 'indigente'
    if row['ITF'] < row['CBT_hogar']:
        return 'pobre'
    else:
        return 'no pobre'
    
    
def compute_poverty(base, basket, print_summary=True):
    year = base['ANO4'].iloc[0]
    trimester = base['TRIMESTRE'].iloc[0]
    periodo = '.'.join([str(year),str(trimester)])
    basket = basket.query("periodo == @periodo")    
    df_adulto_equivalente = _get_ae()
    base = base.merge(df_adulto_equivalente,how="left", on=["CH04", "CH06"])
    base = base.merge(basket,how="left", left_on="REGION",right_on="codigo")
    base['adequi_hogar'] = base.groupby(['CODUSU', 'NRO_HOGAR', 'periodo'])['adequi'].transform('sum')
    base['CBA_hogar'] = base['CBA'] * base['adequi_hogar']
    base['CBT_hogar'] = base['CBT'] * base['adequi_hogar']
    base['situacion'] = base.apply(_compute_situ,axis=1)
    pobreza = sum(base[base['situacion'].isin(['pobre','indigente'])]['PONDIH'])
    total = sum(base['PONDIH'])
    indigencia = sum(base[base['situacion'].isin(['indigente'])]['PONDIH'])   
    print_summary = True
    if (print_summary):
        str_report = \
        f"""
        Tasa_pobreza    = {"{:.2f}".format(pobreza/total)}
        Tasa_indigencia    = {"{:.2f}".format(indigencia/total)}
        """
        print(str_report)
        
    return ({'pobreza':pobreza/total,'indigencia':indigencia/total}, base)