from tkinter.font import names
from unicodedata import name
import pyautogui
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
import re
import openpyxl
from dotenv import load_dotenv
import os
load_dotenv()

t1 = time.time()
dnit = "DNIT"
dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y").replace("/", "-")
planilha = pd.read_excel("base_de_dados/Controle - Frota.xlsx",
                         "Vencimento Documentação", skiprows=1, usecols=['PLACA', 'RENAVAN'])
try:
    planilha_formatada = pd.read_excel(
        "consultas/Consulta dia "+formatData+".xlsx")
except:
    planilha.to_excel("consultas/Consulta dia "+formatData+".xlsx")
    planilha_formatada = pd.read_excel(
        "consultas/Consulta dia "+formatData+".xlsx")
for index, row in planilha_formatada.iterrows():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, timeout=5000)
        context = browser.new_context()
        page = context.new_page()
        page.goto(os.environ['DENI'])
        try:
            placa = row["PLACA"]
            renavan = row["RENAVAN"]
            page.locator('#placa').fill(str(placa))
            page.locator('#renavam').fill(str(renavan).replace(".0", ""))
            page.locator(
                '//*[@id="app"]/div[3]/div[1]/div/div/div/div/div/form/div[4]/button').click()
            time.sleep(0.5)
            filtro_dnit = pyautogui.locateOnScreen(
                'images/sem_infos_dnit.png', confidence=0.6)
            if(filtro_dnit == None):
                try:
                    time.sleep(1)
                    url = page.inner_html(
                        "//*[@id='app']/div[3]/div[3]/div[1]/div")
                    soup = BeautifulSoup(url, 'html.parser')
                    multas = soup.find_all(
                        'span', string=True)
                    print("___________________")
                    print(placa)
                    cont = 0
                    cont2 = 0
                    while cont <= len(multas):
                        if cont == 0:
                            situacao = multas[7].text
                            data = multas[9].text
                            local = multas[13].text
                            municipio = multas[17].text
                            payed = multas[20].text
                        elif cont == 1:
                            situacao = multas[cont2+7].text
                            data = multas[cont2+9].text
                            local = multas[cont2+13].text
                            municipio = multas[cont2+17].text
                            payed = multas[cont2+20].text
                        elif cont == 2:
                            situacao = multas[cont2+5].text
                            data = multas[cont2+7].text
                            local = multas[cont2+11].text
                            municipio = multas[cont2+15].text
                            payed = multas[cont2+18].text
                        elif cont == 3:
                            situacao = multas[cont2+4].text
                            data = multas[cont2+6].text
                            local = multas[cont2+10].text
                            municipio = multas[cont2+14].text
                            payed = multas[cont2+17].text
                        elif cont == 4:
                            situacao = multas[cont2+3].text
                            data = multas[cont2+5].text
                            local = multas[cont2+9].text
                            municipio = multas[cont2+13].text
                            payed = multas[cont2+16].text
                        else:
                            situacao = multas[cont2+7].text
                            data = multas[cont2+4].text
                            local = multas[cont2+13].text
                            municipio = multas[cont2+17].text
                            payed = multas[cont2+20].text
                        if payed == "Pagar":
                            print(
                                "Situação ativa e necessária de pagamento ------->>>>>")
                            print("\nRecebida no dia: "+data +
                                  " em "+municipio+" "+local+"")
                            localizacao = "Recebida no dia: "+data+" em "+municipio+" "+local+""
                            data_as = str(data).replace("às ", "")
                            data_h = data_as.replace("h", ":")
                            data_replace = data_h.replace("min", "")
                            data = re.search(
                                "[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", data_replace).group(0)
                            hour = re.search(
                                "[0-9][0-9]:[0-9][0-9]", data_replace).group(0)
                            hour_first_part = hour[0:2]
                            hour_second_part = hour[2:]
                            if (int(hour_first_part) == 0):
                                acres = '0.1'
                                sumHour = int(hour_first_part)+float(acres)
                            else:
                                hora_acres = int(hour_first_part)+1
                                if hora_acres < 10:
                                    sumHour = '0'+str(hora_acres)
                                else:
                                    sumHour = hora_acres
                            hora_adicionada = str(
                                sumHour)+str(hour_second_part)
                            data_hora_acres = data + " " + hora_adicionada
                            placaArray = [placa]
                            placaParte1 = placa[0:3]
                            placaParte2 = placa[3:]
                            placaReplaced = placaParte1+"-"+placaParte2
                            time.sleep(1)
                            connecta = context.new_page()
                            connecta.goto(os.environ['CONNECTA'])
                            time.sleep(1)
                            connecta.locator("input[name='usuario']").fill(
                                os.environ['USER_NAME'])
                            connecta.locator("input[name='senha']").fill(
                                os.environ['PASSWORD'])
                            time.sleep(1)
                            connecta.locator(
                                "button[name='Submit']").click()
                            connecta.locator(
                                "//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/a").hover()
                            connecta.locator(
                                "//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/ul/li[1]/a").hover()
                            connecta.locator(
                                "a[href='controlerelatoriodeslocamento']").click()
                            connecta.locator(
                                "//*[@id='formfiltro']/fieldset/span[1]/button").click()
                            time.sleep(1)
                            filtro = pyautogui.locateOnScreen(
                                'images/filtro.png', confidence=0.7)
                            time.sleep(1)
                            pyautogui.moveTo(filtro)
                            time.sleep(1)
                            pyautogui.click()
                            pyautogui.write(placaReplaced)
                            time.sleep(1)
                            pyautogui.moveTo(
                                x=filtro.left+50, y=filtro.top+45)
                            time.sleep(1)
                            pyautogui.click()
                            time.sleep(1)
                            dataIniti = connecta.locator(
                                "//*[@id='dtI']").click()
                            time.sleep(1)
                            pyautogui.hotkey('ctrl', 'a')
                            pyautogui.press('del')
                            pyautogui.write(data_replace)
                            time.sleep(1)
                            pyautogui.press('Tab')
                            time.sleep(1)
                            dataFinal = connecta.locator(
                                "//*[@id='dtF']").click()
                            pyautogui.hotkey('ctrl', 'a')
                            pyautogui.press('del')
                            pyautogui.write(data_hora_acres)
                            time.sleep(1)
                            pyautogui.press('Tab')
                            time.sleep(1)
                            connecta.locator(
                                "//*[@id='formfiltro']/fieldset/div/button[2]").click()
                            time.sleep(1)
                            book = openpyxl.load_workbook(
                                filename="consultas/Consulta dia "+formatData+".xlsx")
                            time.sleep(1)
                            try:
                                page_multas = book['Multas']
                            except:
                                book.create_sheet("Multas")
                                page_multas = book['Multas']
                            try:
                                identificado = pyautogui.locateOnScreen(
                                    'images/sem_dados.png', confidence=0.9)
                                if(identificado == None):
                                    time.sleep(1)
                                    newUrl = connecta.inner_html(
                                        "//body/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody")
                                    newSoup = BeautifulSoup(
                                        newUrl, 'html.parser')
                                    nome = newSoup.find_all(
                                        'td', attrs={'style': 'text-align: center'}, string=re.compile(r"[A-Z]"))
                                    contador = 0
                                    while contador < len(nome):
                                        name = nome[contador].text
                                        if re.search(r"[a-z]", name) == None and re.search("CEP", name) == None:
                                            print(
                                                "Nome do condutor --> ", name)
                                            condutor = name
                                        contador += 1
                                    time.sleep(1)
                                    page_multas.append(
                                        [placaReplaced, renavan, localizacao, condutor, dnit])
                                    book.save(
                                        filename="consultas/Consulta dia "+formatData+".xlsx")
                                    print("Dados salvos com sucesso")
                                else:
                                    print('Condutor não identificado\n')
                                    condutor = 'Condutor não identificado'
                                    time.sleep(1)
                                    page_multas.append(
                                        [placaReplaced, renavan, localizacao, condutor, dnit])
                                    book.save(
                                        filename="consultas/Consulta dia "+formatData+".xlsx")
                                    print('Dados salvos sem o condutor')
                            except:
                                print('Sem dados')
                            connecta.locator(
                                "//*[@id='li-sair']/a").click()
                            connecta.close()

                        cont2 += 29
                        cont += 1

                except:
                    print('Não Existem dados')
            else:
                continue
        except:
            print("Consulta concluída")
            tempoExec = time.time() - t1
            print("\nTempo de execução: {} segundos".format(tempoExec))
        browser.close()
