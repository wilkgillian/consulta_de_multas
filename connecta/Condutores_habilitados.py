from datetime import datetime
from playwright.async_api import Page
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os

from termcolor import colored
from utils.excelGenerator import excel_generator_condutores

load_dotenv()


async def condutores(page: Page, path):
    await page.goto(os.environ['CONNECTA'])
    await page.locator(
        "input[name='usuario']").fill(os.environ['USER_NAME'])
    await page.locator(
        "input[name='senha']").fill(os.environ['PASSWORD'])

    await page.locator(
        "button[name='Submit']").click()
    await page.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/a").hover()
    await page.locator(
        "//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/ul/li[2]/a").click()

    new_url = await page.inner_html(
        '//*[@id="box-table-b"]/tbody/tr[16]/th/form')
    new_soup = BeautifulSoup(new_url, 'html.parser')
    next_page = new_soup.find('a').get('href')

    async def extrator():
        contador = 0
        url = await page.inner_html('//*[@id="box-table-b"]/tbody')
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
                    print(colored("Situação da CNH:  VENCIDA EM " +
                                  date_veciment+"", 'red'))
                    await excel_generator_condutores(motorista=motorista_x, data_vencimento=date_veciment, situacao=situacao, path=path)

                else:
                    situacao = 'CNH REGULAR'
                    print(
                        colored("Situação da CNH ---->>  REGULAR ATÉ "+date_veciment+"", 'green'))
                    await excel_generator_condutores(motorista=motorista_x, data_vencimento=date_veciment, situacao=situacao, path=path)

            contador += 1
    while next_page is not None:
        try:
            page.set_default_timeout(5000)
            await extrator()
            await page.locator(
                "//*[@id='box-table-b']/tbody/tr[16]/th/form/a", has_text="Próxima").click()
        except:
            next_page = None
pass
