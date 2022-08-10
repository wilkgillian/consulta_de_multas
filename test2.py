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
          url = newTab.inner_html('//*[@id="div_servicos_Autuacoes"]/table/tbody/tr[2]/td[2]')
          print("Existem dados")
          soup = BeautifulSoup(url, 'html.parser')
          print('\n --- soup criado --- \n')
          debitos = soup.find_all('td', attrs={'class': False, 'width': False, 'colspan':False})
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
            print("entrou no while")
            results = debitos[iContent].text
            # print("\n ---> "+results+" <---\n")
            if re.search("às", results):
                print("\n\ndata e horário ------->>> "+results+"")
                findData = re.search("[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", results).group(0)
                findHour = re.search("[0-9][0-9]:[0-9][0-9]", results).group(0)
                print("\n\nData -->>"+str(findData)+" hora -->> "+str(findHour)+"")
                data_hour_for_connecta = str(findData)+" "+str(findHour)
                print(data_hour_for_connecta)
                convertHour = list(findHour)
                print("Hora em array --> "+convertHour+"\n")
                convertHour1 = convertHour[0:1]
                print("Slice da hora --> "+convertHour1+"\n")
                sumHour = int(convertHour1) +1
                print("Hora adicionada + 1 --> "+sumHour+"\n")
                # hora_mais_um = str(findHour).replace("%d%d", ""%d%d":+1")
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
                connecta.locator("//*[@id='formfiltro']/fieldset/span[1]/button").click()
                time.sleep(2)
                filtro = pyautogui.locateOnScreen('filtro.png', confidence=0.7)
                print(filtro)
                time.sleep(5)
                pyautogui.moveTo(filtro)
                time.sleep(2)
                pyautogui.click()
                time.sleep(2)
                pyautogui.write(placaReplaced)
                time.sleep(2)
                pyautogui.moveTo(x= filtro.left+50, y= filtro.top+45)
                pyautogui.click()
                time.sleep(2)
                connecta.locator("//*[@id='dtI']").fill(data_hour_for_connecta)
                connecta.locator("//*[@id='dtF']").fill()
            else:
              print("nada")
                # page_multas.append([placaReplaced, renavan, results])
                # book.save(filename="C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")
                # print("\n\nMulta identificada ------->>> "+results+"")
                # time.sleep(1)
                
                # # inputt = connecta.locator("/html/body/div[4]/div/div/input")
                # # inputt.wait_for(state= "visible").fill(placaReplaced)
                # # .fill(placaReplaced)
                # # connecta.locator("/html/body/div[4]/ul/li[2]/label/span").click(force=True)
                # # .fill(str(placaReplaced), force=True, no_wait_after=True)
                # print("localizado")
                # time.sleep(5)
                # # connecta.locator("input[title="+re.search(placaReplaced)+"]").click()
                # # time.sleep(2)
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