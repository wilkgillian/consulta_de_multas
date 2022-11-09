import re
from bs4 import BeautifulSoup
from termcolor import colored
from playwright.async_api import BrowserContext, Page
from connecta.buscadorConnecta import connecta_actions

from utils.acresHourConnecta import hour_for_connecta
from utils.excelGenerator import excel_generator_multas
from utils.formatPlacaForConnecta import formatPlacaForConnecta


async def extractor_denit(page: Page, context: BrowserContext, placa, path, orgao):
    url = await page.inner_html("//*[@id='app']/div[3]/div[3]/div[1]/div")
    soup = BeautifulSoup(url, 'html.parser')
    multas = soup.find_all(
        'span', string=True)
    infracao = soup.find_all(
        'span', string=True, attrs={'title': 'Descrição'})
    cont = 0
    cont2 = 0
    while cont <= len(multas):
        mul = infracao[cont].text
        print(mul)
        if cont == 0:
            data = multas[9].text
            local = multas[13].text
            municipio = multas[17].text
            payed = multas[20].text
        elif cont == 1:
            data = multas[cont2+9].text
            local = multas[cont2+13].text
            municipio = multas[cont2+17].text
            payed = multas[cont2+20].text
        elif cont == 2:
            data = multas[cont2+7].text
            local = multas[cont2+11].text
            municipio = multas[cont2+15].text
            payed = multas[cont2+18].text
        elif cont == 3:
            data = multas[cont2+6].text
            local = multas[cont2+10].text
            municipio = multas[cont2+14].text
            payed = multas[cont2+17].text
        elif cont == 4:
            data = multas[cont2+5].text
            local = multas[cont2+9].text
            municipio = multas[cont2+13].text
            payed = multas[cont2+16].text
        else:
            data = multas[cont2+4].text
            local = multas[cont2+13].text
            municipio = multas[cont2+17].text
            payed = multas[cont2+20].text
        if payed != "Pagar":
            print(colored("Débito encontrado em: "+data +
                  " em "+municipio+" "+local+"", 'red'))
            localizacao = "em "+data+" "+municipio+" "+local+""
            data_as = str(data).replace("às ", "")
            data_h = data_as.replace("h", ":")
            data_replace = data_h.replace("min", "")
            debito = {"local": localizacao, "data": data_replace}
            hours = hour_for_connecta(debito)
            connecta = await context.new_page()
            condutor = await connecta_actions(page=connecta, hours=hours, placa=formatPlacaForConnecta(str(placa)))
            await excel_generator_multas(placa=str(placa).upper(), multa=str(mul).upper(), local_data=str(debito['local']).upper(), condutor=str(condutor).upper(), path=path, orgao=str(orgao).upper())
        cont2 += 29
        cont += 1
pass
