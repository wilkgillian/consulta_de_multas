from datetime import datetime
import time
from playwright.async_api import BrowserContext
from bs4 import BeautifulSoup
import re
import openpyxl
from dotenv import load_dotenv
import os

from utils.excelGenerator import excel_generator_condutores
load_dotenv()

t1 = time.time()
detran = "DETRAN"
dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y").replace("/", "-")


async def condutores(path, context: BrowserContext):
    page = await context.new_page()
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
    new_url = await page.inner_html('//*[@id="box-table-b"]/tbody/tr[16]/th/form')
    new_soup = BeautifulSoup(new_url, 'html.parser')
    next_page = new_soup.find('a').get('href')
    book = openpyxl.load_workbook(
        filename="consultas/Consulta dia "+formatData+".xlsx")
    try:
        page_base_condutores = book['Motoristas']
    except:
        book.create_sheet('Motoristas')
        page_base_condutores = book['Motoristas']
        page_base_condutores.append(
            ['MOTORISTAS CADASTRADOS', 'VENCIMENTO DA CNH', 'SITUAÇÃO'])

    async def extrator():
        contador = 0
        time.sleep(2)
        url = await page.inner_html('//*[@id="box-table-b"]/tbody')
        soup = BeautifulSoup(url, 'html.parser')
        names = soup.find_all("td")
        while contador < len(names):
            motorista = names[contador].text
            date = names[contador].text
            if re.search('[a-zA-Z]', motorista) and re.search('SENAC', motorista) == None and re.search('Editar', motorista) == None:
                motorista_x = str(motorista.upper())
                print(motorista_x)
            if re.search("[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", date):
                date_veciment = date
                data = datetime.strptime(str(date_veciment), '%d/%m/%Y')
                if data < datetime.now():
                    situacao = 'CNH VENCIDA'
                    print("Situação da CNH ---->>  VENCIDA EM ", date_veciment)
                    excel_generator_condutores(
                        motorista_x, date_veciment, situacao, path)
                else:
                    situacao = 'CNH REGULAR'
                    print("Situação da CNH ---->>  REGULAR ATÉ ", date_veciment)
                    excel_generator_condutores(
                        motorista_x, date_veciment, situacao, path)
            contador += 1
    while next_page is not None:
        try:
            extrator()
            page.locator(
                "//*[@id='box-table-b']/tbody/tr[16]/th/form/a", has_text="Próxima").click()
        except:
            next_page = None
tempoExec = time.time() - t1
print("\nTempo de execução: {} segundos".format(tempoExec))
