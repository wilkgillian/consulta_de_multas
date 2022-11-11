import datetime
import re
from bs4 import BeautifulSoup
from termcolor import colored

from utils.excelGenerator import excel_generator_condutores


async def extractor_connecta(url):
    newSoup = BeautifulSoup(url, 'html.parser')
    nome = newSoup.find_all(
        'td', attrs={'style': 'text-align: center'}, string=re.compile(r"[A-Z]"))
    contador = 0
    while contador < len(nome):
        infrator = nome[contador].text
        if re.search(r"[a-z]", infrator) == None and re.search("CEP", infrator) == None:
            nomeInfrator = infrator
        contador += 1
    return nomeInfrator


async def extractor_condutores(url: str, path: str):
    soup = BeautifulSoup(url, 'html.parser')
    names = soup.find_all("td")
    while contador < len(names):
        motorista = names[contador].text
        date = names[contador].text
        if re.search('[a-zA-Z]', motorista) and re.search('SENAC', motorista) == None and re.search('Editar', motorista) == None:
            motorista_x = str(motorista.upper())
            print(motorista_x)
        if re.search("(\\d{2}\\/\\d{2}\\/\\d{4})", date):
            date_veciment = date
            data = datetime.strptime(str(date_veciment), '%d/%m/%Y')
            if data < datetime.now():
                situacao = 'CNH VENCIDA'
                print(colored("Situação da CNH: VENCIDA EM " +
                              date_veciment+"", 'red'))
                excel_generator_condutores(
                    motorista=motorista_x, data_vencimento=date_veciment, situacao=situacao, path=path)
            else:
                situacao = 'CNH REGULAR'
                print(
                    colored("Situação da CNH: REGULAR ATÉ "+date_veciment+"", 'green'))
                excel_generator_condutores(
                    motorista=motorista_x, data_vencimento=date_veciment, situacao=situacao, path=path)
        contador += 1
    pass
