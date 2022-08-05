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
          print(debitos)
          iContent=0
          placaArray = [placa]
          placaParte1 = placa[0:3]
          placaParte2 =  placa[3:]
          placaReplaced = placaParte1+"-"+placaParte2
          book = openpyxl.load_workbook(filename="C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")
          book.create_sheet("Multas")
          page_multas = book['Multas']
          while iContent < len(debitos):
            results = debitos[iContent].contents[1].text
            if re.search("Licenciamento", results):
                print("\n\nNão é uma multa ------->>> "+results+"")
            else:
                page_multas.append([placaReplaced, renavan, results])
                book.save(filename="C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")
                print("\n\nMulta identificada ------->>> "+results+"")
                time.sleep(1)
                connecta = context.new_page()
                connecta.goto("http://www16.itrack.com.br/cmatrix/controlemonitoramento")
                connecta.locator("input[name='usuario']").fill("GEAD")
                connecta.locator("input[name='senha']").fill("33312976")
                connecta.locator("button[name='Submit']").click()
                time.sleep(2)
                connecta.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/a").hover()
                connecta.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/ul/li[1]/a").hover()
                connecta.locator("a[href='controlerelatoriodeslocamento']").click()
                time.sleep(2)
                # connecta.close()
                # time.sleep(1)
                # connecta.locator("/html/body/div/table/tbody/tr[2]/td/div/form/div[1]/table/tbody/tr[4]/td[2]/input").fill("")
                # time.sleep(1)
                # connecta.locator("/html/body/div/table/tbody/tr[2]/td/div/form/div[1]/table/tbody/tr[6]/td/button").click()
                # time.sleep(5)
            iContent+=1
        except: 
          print("Não existem dados") 
          continue
      except:
        print("Consulta concluída")
        continue  
      browser.close()