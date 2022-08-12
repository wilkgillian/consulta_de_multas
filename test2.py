import ast
from dataclasses import replace
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
      browser = p.chromium.launch(headless=False, timeout=2000)
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
          time.sleep(1)
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
            if re.search("às", results):
                print("\n\ndata e horário ------->>> "+results+"")
                findData = re.search("[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", results).group(0)
                findHour = re.search("[0-9][0-9]:[0-9][0-9]", results).group(0)
                print("\n\nData -->>"+str(findData)+" hora -->> "+str(findHour)+"")
                data_hour_for_connecta = str(findData)+" "+str(findHour)
                print(data_hour_for_connecta)
                convertHour = str(findHour)
                newHour = convertHour.replace(":", "")
                aspsHour = newHour.replace(newHour,"'"+newHour+"'")
                convertHour1 = aspsHour[1:3]
                secondPartHour = aspsHour[3:5]
                print("Slice da hora parte final--> '"+secondPartHour+"'\n")
                print(type(convertHour1))
                acres = '01'
                sumHour = int(convertHour1)+int(acres)
                print(type(sumHour))
                print(sumHour)
                horaAidicionada = str(sumHour)+":"+str(secondPartHour)
                print(horaAidicionada)
                data_hour_adicionada = str(findData)+ " " +str(horaAidicionada)
                print(data_hour_adicionada)
                connecta = context.new_page()
                connecta.goto("http://www16.itrack.com.br/cmatrix/controlemonitoramento")
                connecta.locator("input[name='usuario']").fill("GEAD")
                connecta.locator("input[name='senha']").fill("33312976")
                connecta.locator("button[name='Submit']").click()
                time.sleep(1)
                connecta.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/a").hover()
                connecta.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/ul/li[1]/a").hover()
                connecta.locator("a[href='controlerelatoriodeslocamento']").click()
                time.sleep(1)
                connecta.locator("//*[@id='formfiltro']/fieldset/span[1]/button").click()
                time.sleep(1)
                filtro = pyautogui.locateOnScreen('filtro.png', confidence=0.7)
                print(filtro)
                time.sleep(1)
                pyautogui.moveTo(filtro)
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)
                pyautogui.write(placaReplaced)
                time.sleep(1)
                pyautogui.moveTo(x= filtro.left+50, y= filtro.top+45)
                pyautogui.click()
                time.sleep(1)
                dataIniti = connecta.locator("//*[@id='dtI']").click()
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('del')
                pyautogui.write(data_hour_for_connecta)
                time.sleep(1)
                pyautogui.press('Tab')
                time.sleep(1)
                dataFinal = connecta.locator("//*[@id='dtF']").click()
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('del')
                pyautogui.write(data_hour_adicionada)
                time.sleep(1)
                pyautogui.press('Tab')
                time.sleep(1)
                connecta.locator("//*[@id='formfiltro']/fieldset/div/button[2]").click()
                time.sleep(1)
                newUrl = connecta.inner_html("//body/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr[@class='even']")
                newSoup = BeautifulSoup(newUrl, 'html.parser')
                nome =  newSoup.find_all('td', attrs={'style': 'text-align: center'}, string=re.compile("[^a-z]"))
                contador = 0
                while contador < len(nome):
                  infrator = nome[0].text
                  if re.search("[a-zA-Z]", infrator):
                    nomeInfrator = infrator
                  contador+=1  
                page_multas.append([placaReplaced, renavan, results, nomeInfrator])
                book.save(filename="C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")
            iContent+=1
        except:  
          try: 
           select = newTab.locator('//*[@id="cmbTipoDebito"]').click()
           time.sleep(1)
           pyautogui.press('down')
           pyautogui.press('down')
           time.sleep(1)
           pyautogui.press('enter')
           time.sleep(1)
           url = newTab.inner_html('//*[@id="div_servicos_Multas"]/table/tbody/tr[2]/td[2]')
           print("Existem dados")
           soup = BeautifulSoup(url, 'html.parser')
           print('\n --- soup criado --- \n')
           debitos = soup.find_all('td', attrs={'class': False, 'width': False, 'colspan':False}, string=re.compile("às"))
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
             if re.search("às", results):
                print("\n\ndata e horário ------->>> "+results+"")
                findData = re.search("[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", results).group(0)
                findHour = re.search("[0-9][0-9]:[0-9][0-9]", results).group(0)
                print("\n\nData -->>"+str(findData)+" hora -->> "+str(findHour)+"")
                data_hour_for_connecta = str(findData)+" "+str(findHour)
                print(data_hour_for_connecta)
                convertHour = str(findHour)
                newHour = convertHour.replace(":", "")
                aspsHour = newHour.replace(newHour,"'"+newHour+"'")
                convertHour1 = aspsHour[1:3]
                secondPartHour = aspsHour[3:5]
                print("Slice da hora parte final--> '"+secondPartHour+"'\n")
                print(type(convertHour1))
                sumHour = int(convertHour1)+1
                print(type(sumHour))
                print(sumHour)
                horaAidicionada = str(sumHour)+":"+str(secondPartHour)
                print(horaAidicionada)
                data_hour_adicionada = str(findData)+ " " +str(horaAidicionada)
                print(data_hour_adicionada)
                connecta = context.new_page()
                connecta.goto("http://www16.itrack.com.br/cmatrix/controlemonitoramento")
                connecta.locator("input[name='usuario']").fill("GEAD")
                connecta.locator("input[name='senha']").fill("33312976")
                connecta.locator("button[name='Submit']").click()
                time.sleep(1)
                connecta.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/a").hover()
                connecta.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/ul/li[1]/a").hover()
                connecta.locator("a[href='controlerelatoriodeslocamento']").click()
                time.sleep(1)
                connecta.locator("//*[@id='formfiltro']/fieldset/span[1]/button").click()
                time.sleep(1)
                filtro = pyautogui.locateOnScreen('filtro.png', confidence=0.7)
                print(filtro)
                time.sleep(1)
                pyautogui.moveTo(filtro)
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)
                pyautogui.write(placaReplaced)
                time.sleep(1)
                pyautogui.moveTo(x= filtro.left+50, y= filtro.top+45)
                pyautogui.click()
                time.sleep(1)
                dataIniti = connecta.locator("//*[@id='dtI']").click()
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('del')
                pyautogui.write(data_hour_for_connecta)
                time.sleep(1)
                pyautogui.press('Tab')
                time.sleep(1)
                dataFinal = connecta.locator("//*[@id='dtF']").click()
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('del')
                pyautogui.write(data_hour_adicionada)
                time.sleep(1)
                pyautogui.press('Tab')
                time.sleep(1)
                connecta.locator("//*[@id='formfiltro']/fieldset/div/button[2]").click()
                time.sleep(1)
                newUrl = connecta.inner_html("//body/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr[@class='even']")
                newSoup = BeautifulSoup(newUrl, 'html.parser')
                nome =  newSoup.find_all('td', attrs={'style': 'text-align: center'}, string=re.compile("[^a-z]"))
                contador = 0
                while contador < len(nome):
                  infrator = nome[0].text
                  if re.search("[a-zA-Z]", infrator):
                    nomeInfrator = infrator
                  contador+=1  
                page_multas.append([placaReplaced, renavan, results, nomeInfrator])
                book.save(filename="C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")
             iContent+=1
          except: 
           print("Não existem dados") 
          continue
        
      except:
        print("Consulta concluída")
        continue  
      browser.close()