import sys
import click
from meu_contracheque.scraping_mg import (scraping_process_begin,
                                         scraping_login_process,
                                         csv_register,
                                         clean_full_process,
                                         find_last_period,
                                         scraping_full_process,
                                         clean_process)


def scraping_mg_initial_period(masp, senha, stop_period):
  """
  Função responsável pela busca de informações dos contracheques dos servidores do Estado de Minas Gerais até o período desejado.
  Parâmetros:
  -------
  masp: string
    Masp do servidor do Estado de Minas Gerais
  senha: string
    Senha de acesso ao Portal do servidor do Estado de Minas Gerais
  stop-period: string
    Período final para a qual a busca será realizada
  Retorna:
  -------
  Arquivo "contracheques.csv" atualizado com as informações de todos os contracheque disponíveis no Portal do Servidor.
  """
  try:
    click.echo('Iniciando processo de extração de todos contracheques...')
    clean_full_process()
    start = scraping_process_begin()
    driver = start[0]
    period = start[1]
    scraping_login_process(driver, period, masp, senha)
    scraping_full_process(driver, period, False, stop_period)
    csv_register()
    clean_process()
  except:
    click.echo('Não foi possível finalizar o processo de busca de todos contracheques.')
    sys.exit(1)

@click.command(name='ate-periodo-inicial')
@click.option('--masp', '-m', envvar='MASP', required=True,
              help="Masp do servidor do Estado de Minas Gerais")
@click.option('--senha', '-s', envvar='PORTAL_PWD', required=True,
              help="Senha de acesso ao Portal do servidor do Estado de Minas Gerais")
@click.option('--stop-period', '-sp', required=True,
              help="Último período a ser pesquisado. Exemplo: 02/2008")
def scraping_mg_initial_period_cli(masp, senha, stop_period):
  """
  Função CLI responsável pela busca de informações dos contracheques dos servidores do Estado de Minas Gerais até o período desejado.
  Por padrão, função buscará masp e senha nas variáveis de ambiente MASP e PORTAL_PWD cadastradas na máquina ou
  em arquivo .env.
  Parâmetros:
  ----------
  masp: string
      Masp do servidor do Estado de Minas Gerais
  senha: string
    Senha de acesso ao Portal do servidor do Estado de Minas Gerais
  stop-period: string
    Período final para a qual a busca será realizada
  Retorna:
  -------
  Arquivo "contracheques.csv" atualizado com as informações de todos os contracheques disponíveis no Portal do Servidor.
  """
  scraping_mg_initial_period(masp, senha, stop_period)
