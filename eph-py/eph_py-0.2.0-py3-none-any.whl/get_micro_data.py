import requests
from datetime import datetime
import pandas as pd
import zipfile
import os
import warnings
import wget


MODULE_PATH = os.getcwd()

def _download_url(url, zipe_file_path, chunk_size=128):
    # Delete file if already exists
    if os.path.exists(zipe_file_path):
        os.remove(zipe_file_path)
    # Download zip file
    r = requests.get(url, stream=True)
    with open(zipe_file_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def _get_url(year,trimester,wave,base_type):
    url = f'https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_usu_{trimester}_Trim_{year}_txt.zip'
    zip_file_name = url.split('/')[-1]
    return url, zip_file_name

def _get_microdata_s3(year,trimester,wave,base_type):
    if year >= 2003 and trimester is not None:
        url = f'https://datasets-humai.s3.amazonaws.com/eph/{base_type}/base_{base_type}_{year}T{trimester}.csv'
    if year <= 2003 and wave is not None:
        url = f'https://datasets-humai.s3.amazonaws.com/eph/{base_type}/base_{base_type}_{year}O{wave}.csv'
        
    filename = url.split('/')[-1]
    if os.path.exists(filename):
            os.remove(filename)
            
    print(filename)
    
    filename = wget.download(url)
    df = pd.read_csv(filename, low_memory=False, encoding='unicode_escape')
    return df

def _download_microdata_internal(year,trimester,wave,base_type):
    #
    url,zip_file_name = _get_url(year,trimester,wave,base_type)
    #
    unzip_folder = zip_file_name.replace(".zip","")
    #
    zip_file_path = os.path.join(MODULE_PATH,zip_file_name)
    #
    _download_url(url,zip_file_path)
    #
    return zip_file_path,unzip_folder

    
def unzip_file(zip_file_path,unzip_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(f'{os.path.join(MODULE_PATH,unzip_folder)}/')

        
def _get_microdata_internal(year,trimester,wave,base_type):
    #
    zip_file_path,unzip_folder = _download_microdata_internal(year,trimester,wave,base_type)
    #
    unzip_file(zip_file_path,unzip_folder)
    #
    for file in os.listdir(os.path.join(MODULE_PATH,unzip_folder)):
        if base_type == 'hogar' and "hogar" in file:
            return_file = file
        if base_type == 'individual' and "individual" in file:
            return_file = file
    df = pd.read_csv(os.path.join(MODULE_PATH,unzip_folder,return_file),sep=';',low_memory=False)
    return df


def _handle_exceptions_warnings(year,trimester,wave,base_type):
    if not isinstance(year,int):
        raise ValueError("El año debe ser un valor entero")
    if not isinstance(trimester,int) and not isinstance(wave,int) :
        raise ValueError("Se debe informar el mes o la onda")
    if isinstance(trimester,int) and isinstance(wave,int) :
        raise ValueError("Se debe informar el la onda o el trimestre no ambas")
    if isinstance(trimester,int) and trimester not in [1,2,3,4]:
        raise ValueError("Por favor ingresa un numero de trimeste valido: 1,2,3,4")
    if isinstance(wave,int) and wave not in [1,2]:
        raise ValueError("Por favor ingresa un numero de onda valido: 1,2")
    if base_type not in ['individual','hogar']:
        raise ValueError("Seleccione un tipo de base válido: individual u hogar")
    if year < 2003 and wave is None:     
        raise ValueError("para antes de 2003, es necesario definir la onda (wave) de la EPH puntual")
    if year==2007 and trimester==3:
        warnings.warn("INDEC advierte: La informacion correspondiente al tercer trimestre \
                 2007 no esta disponible ya que los aglomerados Mar del Plata-Batan, \
                 Bahia Blanca-Cerri y Gran La Plata no fueron relevados por causas \
                 de orden administrativo, mientras que los datos correspondientes al \
                 Aglomerado Gran Buenos Aires no fueron relevados por paro del \
                 personal de la EPH.")
    if (year ==2015 and trimester in [3,4]) |  (year ==2016 and trimester==1):
        raise ValueError("En el marco de la emergencia estadistica el INDEC no publico la base solicitada. \
                 mas informacon en: https://www.indec.gob.ar/ftp/cuadros/sociedad/anexo_informe_eph_23_08_16.pdf")
    if year >= 2007 and year <= 2015:
        warnings.warn('''INDEC advierte:
              Advertencia sobre el uso de series estadisticas
Se advierte que las series estadisticas publicadas con posterioridad a enero 2007 y hasta diciembre 2015 deben ser consideradas con reservas, excepto las que ya hayan sido revisadas en 2016 y su difusion lo consigne expresamente. El INDEC, en el marco de las atribuciones conferidas por los decretos 181/15 y 55/16, dispuso las investigaciones requeridas para establecer la regularidad de procedimientos de obtencion de datos, su procesamiento, elaboracion de indicadores y difusion.
mas informacon en: https://www.indec.gob.ar/ftp/cuadros/sociedad/anexo_informe_eph_23_08_16.pdf''')
        
        
def get_micro_data(year = 2018, trimester = None, wave = None, base_type='individual', vars = 'all',
                  destfile = None):
        _handle_exceptions_warnings(year,trimester,wave,base_type)
        
        if year <= 2018:
            df = _get_microdata_s3(year,trimester,wave,base_type)
        else:
            df = _get_microdata_internal(year,trimester,wave,base_type)
        return df
        