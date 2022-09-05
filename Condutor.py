import pyautogui
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
import re
import openpyxl

t1 = time.time()
detran = "DETRAN"
dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y").replace("/", "-")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, timeout=5000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://www16.itrack.com.br/cmatrix/controlemonitoramento")
    page.locator(
        "input[name='usuario']").fill("GEAD")
    page.locator(
        "input[name='senha']").fill("33312976")
    time.sleep(1)
    page.locator(
        "button[name='Submit']").click()
    page.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/a").hover()
    page.locator(
        "//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/ul/li[2]/a").click()
    time.sleep(2)
    new_url = page.inner_html('//*[@id="box-table-b"]/tbody/tr[16]/th/form')
    new_soup = BeautifulSoup(new_url, 'html.parser')
    next_page = new_soup.find('a').get('href')
    time.sleep(3)
    parametro = 0
    book = openpyxl.load_workbook(
        filename="consultas/Consulta dia "+formatData+".xlsx")
    try:
        page_base_condutores = book['Motoristas']
    except:
        book.create_sheet('Motoristas')
        page_base_condutores = book['Motoristas']
        page_base_condutores.append(
            ['MOTORISTAS CADASTRADOS', 'VENCIMENTO DA CNH', 'SITUAÇÃO'])

    def extrator():
        contador = 0
        time.sleep(2)
        url = page.inner_html('//*[@id="box-table-b"]/tbody')
        soup = BeautifulSoup(url, 'html.parser')
        names = soup.find_all("td")
        while contador < len(names):
            motorista = names[contador].text
            date = names[contador].text
            sec = 'SENAC'
            if re.search('[a-zA-Z]', motorista):
                if motorista != sec:
                    if re.search('Editar', motorista) == None:
                        motorista_x = str(motorista.upper())
                        page_base_condutores.append(
                            [motorista_x, None, None])
                        book.save(filename="consultas/Consulta dia " +
                                  formatData+".xlsx")
            if re.search("[0-9]", date):
                date_veciment = date
                if date_veciment.count('') == 11:
                    date_venc = date_veciment
                    print("Data de vencimento ---->> ", date_venc)
                    data_atual = dataAtual.strftime("%d/%m/%Y")
                    page_base_condutores.append(
                        [None, date_venc, None])
                    book.save(filename="consultas/Consulta dia " +
                              formatData+".xlsx")
                    if str(date_venc) < data_atual:
                        situacao_cnh = "CNH VENCIDA"
                    else:
                        situacao_cnh = "CNH REGULAR"
                    page_base_condutores.append(
                        [None, None, situacao_cnh])
                    book.save(filename="consultas/Consulta dia " +
                              formatData+".xlsx")
            contador += 1
    while next_page is not None:
        try:
            extrator()
            page.locator(
                "//*[@id='box-table-b']/tbody/tr[16]/th/form/a", has_text="Próxima").click()
        except:
            next_page = None
    browser.close()
tempoExec = time.time() - t1
print("\nTempo de execução: {} segundos".format(tempoExec))
