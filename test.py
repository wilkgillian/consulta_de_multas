import pyautogui
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
import re
import openpyxl


dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y").replace("/", "-")
planilha = pd.read_excel("C:/Users/wilk.silva/Downloads/Controle - Frota.xlsx", "Vencimento Documentação", usecols=[8, 9])
planilha.to_excel("C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")
planilha_formatada = pd.read_excel("C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")
for index,row in planilha_formatada.iterrows():
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=False, timeout=5000)
      context = browser.new_context()
      page = context.new_page()
      page.goto("https://www.detran.mt.gov.br/")
      time.sleep(1)
      try:
        placa = row["PLACA"]
        renavan = row["RENAVAN"]
        try:
          page.locator('.closer').click()
        except:
          continue
        time.sleep(1)
        page.locator('#input_placa').fill(str(placa))
        page.locator('#input_renavam').fill(str(renavan).replace(".0",""))
        time.sleep(1)
        with context.expect_event("page") as event_info:
          page.locator('//*[@id="formVeiculo"]/div[4]/input[2]').click()
        newTab = event_info.value
        try: 
          select = newTab.locator('//*[@id="cmbTipoDebito"]').click()
          time.sleep(1)
          pyautogui.press('down')
          pyautogui.press('down')
          time.sleep(1)
          pyautogui.press('enter')
          time.sleep(2)
          url = newTab.inner_html('form')
          print("Existem dados")
          soup = BeautifulSoup(url, 'html.parser')
          print('\n --- soup criado --- \n')
          debitos = soup.find_all('td', attrs={'class': False, 'width': False})
          print('\n --- debitos identificados --- \n')
          print(len(debitos))
          print(debitos)
          iContent=0
          book = openpyxl.load_workbook(filename="C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")
          book.create_sheet("Multas")
          page_multas = book['Multas']
          while iContent < len(debitos):
            print('\n ---- entrou no while ----\n')
            results = debitos[iContent].contents[1].text
            print(iContent)
            if re.search("Licenciamento", results):
                print("Não é uma multa")
            else:
                page_multas.append([placa, renavan, results])
                book.save(filename="C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")
                print(results)
            iContent+=1
          browser.close()
        except: 
          print("Não existem dados")
          continue 
        browser.close()
      except:
        print("Consulta concluída")

        continue
      browser.close()   
