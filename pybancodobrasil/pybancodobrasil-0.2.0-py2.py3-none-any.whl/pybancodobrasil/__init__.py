"""This module do web crawler of banco do brasil."""
__version__ = "0.2.0"

import socket
import time
from datetime import datetime
from random import randrange

import chardet
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def _is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def _get_free_port():
    port = randrange(1058, 65535)
    while _is_port_in_use(port):
        port = randrange(1058, 65535)
    return port


def _get_driver(headless=True, driver_name='chrome'):
    if driver_name == 'firefox':
        options = webdriver.FirefoxOptions()
        options.headless = headless
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        driver.implicitly_wait(10)
        return driver
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options,
                              port=_get_free_port())
    driver.implicitly_wait(10)
    return driver


def _decode(_bytes):
    return _bytes.decode(chardet.detect(_bytes)['encoding'])


def _parse_pt_br_value(str_value):
    multiplier = 1
    if 'D' in str_value:
        multiplier = -1
    value = str_value.replace('.', '').replace(',', '.').replace('D', '').replace('*', '').replace('C', '').replace(
        '\xa0', '').strip()
    return float(value) * multiplier


def _parse_pt_br_date_time(str_date):
    return time.mktime(datetime.strptime(str_date, "%d/%m/%Y %H:%M:%S").timetuple())


def _parse_pt_br_date(str_date):
    return time.mktime(datetime.strptime(str_date, "%d/%m/%Y").timetuple())


def _parse_transaction(array):
    total_columns = len(array)
    if total_columns <= 4:
        return None
    str_value = ' '.join(array[4])
    if not str_value:
        str_value = ' '.join(array[5])
    if not str_value:
        return None
    transaction = Transaction()
    date_pt_br = ' '.join(array[0])
    description = ''
    if len(array[2]) > 1:
        transaction.title = array[2][0]
        transaction.description = ' '.join(array[2][1:])
    else:
        transaction.title = ' '.join(array[2])
    transaction.document_id = ' '.join(array[3])
    transaction.value = _parse_pt_br_value(str_value)
    hour = '00:00:00'
    for desc in description.split(' '):
        if ':' in desc:
            hour = desc + ":00"
    transaction.timestamp = _parse_pt_br_date_time(date_pt_br + ' ' + hour)
    if 'Saldo' in transaction.title or 'S A L D O' in transaction.title:
        transaction.balance = True
    return transaction


class Transaction:
    def _init__(self):
        self.description = None
        self.document_id = None
        self.timestamp = None
        self.title = None
        self.value = None
        self.balance = False

        self.parc = None
        self.city = None
        self.card = None
        self.validity = None


class BrazilBank:
    def __init__(self, driver=None, headless=True, driver_name='chrome'):
        self._location = None
        self.driver = driver if driver else _get_driver(headless, driver_name)
        if not hasattr(self.driver, 'requests'):
            raise Exception('You need to use selenium-wire')

    def login(self, agency, account, password, timeout=15, retry=False):
        self.driver.get("https://www2.bancobrasil.com.br/aapf/login.html?1624286762470#/acesso-aapf-agencia-conta-1")
        while True:
            el_agency = self.driver.find_element(By.ID, "dependenciaOrigem")
            el_agency.clear()
            el_agency.send_keys(agency)
            time.sleep(1)
            el_account = self.driver.find_element(By.ID, "numeroContratoOrigem")
            el_account.clear()
            el_account.send_keys(account)
            time.sleep(1)
            self.driver.find_element(By.ID, "botaoEnviar").click()
            errors = self.driver.find_elements(By.CSS_SELECTOR, '.erro')
            if not len(errors):
                break
            hide = 0
            for error in errors:
                try:
                    if 'hide' in error.get_attribute('class'):
                        hide += 1
                except:
                    hide += 1
            if len(errors) == hide:
                break
            time.sleep(1)
        self.driver.find_element(By.ID, "senhaConta").send_keys(password)
        self.driver.find_element(By.ID, "botaoEnviar").click()
        time.sleep(timeout)
        if not self.logged and retry:
            self.login(agency, account, password, retry)

    @property
    def logged(self):
        return 'https://www2.bancobrasil.com.br/aapf/principal.jsp?ambienteLayout=completo' in self.driver.current_url

    def _check(self):
        if not self.logged:
            raise Exception('User not logged')

    def get_transactions(self, month=1, year=1993, callback=None):
        self._check()
        if self._location != 'transactions':
            self._location = 'transactions'
            time.sleep(10)
        self.driver.execute_script("document.querySelector('[codigo=\"32456\"]').click()")
        url = "/aapf/extrato/009-00-N.jsp"
        period = "00{}{}".format(str(month).zfill(2), year)
        script = '$.ajaxApf({atualizaContadorSessao:!0,cache:!1,funcaoSucesso:()=>null,funcaoErro:()=>null,' \
                 'parametros:{ambienteLayout:"internoTransacao",confirma:"sim",periodo:"{}",tipoConta:"",' \
                 'novoLayout:"sim"},simbolo:"30151696898430647187469639762490",tiporetorno:"html",type:"post",' \
                 'url:"{}"}); '
        self.driver.execute_script(script.format(period, url))
        already_checked = []
        while True:
            requests = self.driver.requests
            transaction_requests = list(filter(
                lambda r: url in r.url and period in _decode(r.body), requests))
            for request in transaction_requests:
                if not request.response or request.url in already_checked:
                    continue
                already_checked.append(request.url)
                html = _decode(request.response.body)
                if 'SEM LANCAMENTOS NO PERIODO' in html:
                    return []
                if 'Erro ao exportar dados da transação' in html:
                    self.driver.execute_script(script)
                else:
                    parsed_html = BeautifulSoup(html)
                    table = parsed_html.find('table', attrs={'class': 'tabelaExtrato'})
                    if table:
                        transactions = []
                        lines = table.find_all('tr')
                        for line in lines:
                            columns = line.find_all('td')
                            if len(columns):
                                values = []
                                for column in columns:
                                    values.append(list(map(lambda c: c.text, column.children)))
                                transaction = _parse_transaction(values)
                                if transaction:
                                    if callback:
                                        callback(transaction)
                                    transactions.append(transaction)
                        return transactions

    def get_cards(self, callback=None):
        self._check()
        if self._location != 'cards':
            self._location = 'cards'
            self.driver.execute_script("document.querySelector('[codigo=\"32715\"]').click()")
            time.sleep(10)
        total_child = self.driver.execute_script("return document.querySelector('#carousel-cartoes').childElementCount")

        def _get_xhr_response(driver, url, check_url=None):
            script_xhr_request = 'var url="{}",req=configura();req.open("GET",url,!0),req.send(null);'
            driver.execute_script(script_xhr_request.format(url))
            check_url = check_url if check_url else url
            while True:
                cards_requests = list(filter(lambda r: check_url in r.url and r.response, driver.requests))
                if len(cards_requests):
                    for request in cards_requests:
                        return BeautifulSoup(_decode(request.response.body))

        transactions = []
        for index in range(0, total_child):
            card_parsed_html = _get_xhr_response(self.driver,
                                                 "/aapf/cartao/v119-01e2.jsp?indice={}&pagina=json".format(index))
            invoice_index = 0
            while card_parsed_html.find('li', {'indicetabs': invoice_index}):
                invoice_parsed_html = _get_xhr_response(self.driver,
                                                        "/aapf/cartao/v119-01e3.jsp?indice={}&pagina=normal".format(
                                                            invoice_index), '/aapf/cartao/v119-03r1.jsp')
                card_text = invoice_parsed_html.find_all('span', attrs={'class': 'textoIdCartao'})
                if len(card_text) > 1:
                    card_number = card_text[1].text
                    validity_pt_br = invoice_parsed_html.find('div', attrs={'class': 'vencimentoFatura'}).text.replace(
                        'Vencimento', '').strip()
                    lines = invoice_parsed_html.find_all('tr')
                    for line in lines:
                        columns = list(map(lambda td: td.text.strip(), line.find_all('td')))
                        if len(columns) == 4 and '/' in columns[0]:
                            dd, mm, yy = validity_pt_br.split('/')
                            date = '{}/{}'.format(columns[0], yy)
                            _title = ''.join(columns[1])
                            if 'PARC' in _title:
                                title = _title[0:13].strip()
                                parc = _title[19:24].strip()
                                city = _title[25:].strip()
                            elif 'PGTO' in _title:
                                title = _title
                                parc = '01/01'
                                city = ''
                            else:
                                title = _title[0:23].strip()
                                parc = '01/01'
                                city = _title[23:].strip()
                            transaction = Transaction()
                            transaction.title = title
                            transaction.parc = parc
                            transaction.city = city
                            transaction.card = card_number
                            transaction.timestamp = _parse_pt_br_date(date)
                            transaction.validity = _parse_pt_br_date(validity_pt_br)
                            transaction.value = _parse_pt_br_value(columns[3]) * -1
                            if callback:
                                callback(transaction)
                            transactions.append(transaction)
                invoice_index += 1
        return transactions
