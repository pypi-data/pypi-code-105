#!/usr/bin/env python
import glob
import os
from os.path import expanduser
from datetime import date, timedelta
import yaml
from yaml.loader import SafeLoader
import click


@click.command()
@click.option('--retention','-r', default=15, help='Number of days. Default value 15')
@click.option('--extension','-e', default="*", help='Extension of files. Default value *')
@click.option('--path','-p', help='Path')
@click.option('--delete','-d', default=False ,help='For delete files', is_flag=True)

def main(retention, extension, path, delete):
    """ Delete files based on predefined dates """
    space = "--------------------------------------------------------------------"
    today = date.today()
    days_ago = today - timedelta(days=retention)
    home = expanduser("~")
    output_yaml = os.path.join(home, ".file_retention")
    os.makedirs(output_yaml, exist_ok = True)
    click.echo(f'{space}\nDiretório criado: {output_yaml}')

    def create_yaml(dictionary, date):
        """Recebe um dicionario e uma data para montar o arquivo yaml"""
        full_path = os.path.join(output_yaml, f'{date}.yml')
        if len(dictionary["arquivos"]) > 0:
            with open(full_path, 'w') as yaml_file:
                yaml.dump(dictionary, yaml_file, default_flow_style=False)
            click.echo(space)
            click.echo(f'Arquivo exportado: {full_path}')
        else:
            click.echo(space)
            click.echo(f"Não há arquivos no diretório ou não foi passado um diretorio.")

    def get_files(fullpath):
        """Recebe um diretorio e coleta todos os arquivos que existe no diretorio recursivamente e salva em uma lista"""
        values = [f for f in glob.glob(f"{fullpath}**/*.{extension}", recursive=True)]
        count = len(values)
        click.echo(f'{space}\n{count} arquivos encontrados!')
        return values

    def create_dict(date, fullpath):
        """Recebe uma data e cria um dicionario com a data e a lista de arquivos encontrados na funcao get_files() """
        dicts = {}
        dicts["date"] = date
        dicts["arquivos"] = get_files(fullpath)
        return dicts

    def read_yaml(date, key):
        """Recebe uma data e uma chave para ler o arquivo yaml"""
        full_path = os.path.join(output_yaml, f'{date}.yml')
        if os.path.exists(full_path):
            click.echo(f"{space}\nArquivo {full_path} Encontrado!")
            with open(full_path, "r") as config:
                data = yaml.load(config, Loader=SafeLoader)
                data = data[key]
                click.echo(f"{space}\nLendo o arquivo: {full_path}")
            return data
        else:
            click.echo(f"{space}\nAinda não existe o arquivo {full_path}.")

    def delete_yaml(files):
        ...
        
    def delete_files(date):
        """Recebe uma data deleta os arquivos consultando o yaml ~/.file_retention/yyyy-mm-dd.yml"""
        if delete:
            full_path = os.path.join(output_yaml, f'{date}.yml')
            if os.path.exists(full_path):
                files = read_yaml(date, "arquivos")
                click.echo(f"{space}\nOs arquivos de {retention} dias atrás serão excluídos!!\n{space}")
                for f in files:
                    if os.path.exists(f):
                        os.remove(f"{f}")
                        click.echo(f"Arquivo removido: {f}")
                    else:
                        click.echo(f"O Arquivo {f} não existe mais")
                click.echo(space)
            else:
                click.echo(f"{space}\nO arquivo {full_path} não existe ainda.\n{space}")
        else:
            click.echo(f"{space}\nNada será deletado.\n{space}")

    create_yaml(create_dict(today, path), today)
    delete_files(days_ago)