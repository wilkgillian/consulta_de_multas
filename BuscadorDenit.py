import pyautogui
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
import re
import openpyxl

t1 = time.time()
dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y").replace("/", "-")
planilha = pd.read_excel("base_de_dados/Controle - Frota.xlsx", "Vencimento Documentação", skiprows=1, usecols=['PLACA', 'RENAVAN'])
planilha.to_excel("consultas/Dnit/Consulta dia "+formatData+".xlsx")
planilha_formatada = pd.read_excel("consultas/Dnit/Consulta dia "+formatData+".xlsx")
for index,row in planilha_formatada.iterrows():
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=False, timeout=5000)
      context = browser.new_context()
      page = context.new_page()
      page.goto("https://servicos.dnit.gov.br/multas/")
      try:
        placa = row["PLACA"]
        renavan = row["RENAVAN"]
        page.locator('#placa').fill(str(placa))
        page.locator('#renavam').fill(str(renavan).replace(".0",""))
        page.locator('//*[@id="app"]/div[3]/div[1]/div/div/div/div/div/form/div[4]/button').click()
        time.sleep(0.5)
        filtro_dnit = pyautogui.locateOnScreen('sem_infos_dnit.png', confidence=0.6)
        if(filtro_dnit == None):
         try: 
             time.sleep(1)
             url = page.inner_html("//*[@id='app']/div[3]/div[3]/div[1]/div")
             soup = BeautifulSoup(url, 'html.parser')
             multas = soup.find_all('span', attrs={'style': 'font-weight: bold;'})
             url2 = page.inner_html("//*[@id='app']/div[3]/div[3]/div[1]/div")
             soup2 = BeautifulSoup(url2, 'html.parser')
             pago = soup2.find_all('span', attrs={'style':False}, string=re.compile("(PAGO)"))
             print("___________________")
             print(placa)
             controller = 0
             while controller <= len(multas):
               print("\nEstá pago? ======>>> ",pago[controller].text)
               results = multas[controller].text
               situacao = multas[1].text
               data = multas[2].text
               local = multas[4].text
               municipio = multas[6].text
               if re.search("ATIVO", results) and pago[1].text != "(PAGO)":
                 print("Situação ativa ------->>>>>")
                 print("\nRecebida no dia: "+data+" em "+municipio+" "+local+"") 
                 localizacao = "Recebida no dia: "+data+" em "+municipio+" "+local+""
                 data_as = str(data).replace("às ", "")
                 data_h = data_as.replace("h", ":")
                 data_replace = data_h.replace("min", "")
                 print(data_replace)
                 data = re.search("[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", data_replace).group(0)
                 print("Só a data ----->>  ",data)
                 hour = re.search("[0-9][0-9]:[0-9][0-9]",data_replace).group(0)
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
                 hora_adicionada = str(sumHour)+str(hour_second_part)
                 data_hora_acres = data+ " " +hora_adicionada
                 print(hora_adicionada)
                 placaArray = [placa]
                 placaParte1 = placa[0:3]
                 placaParte2 =  placa[3:]
                 placaReplaced = placaParte1+"-"+placaParte2
                 time.sleep(1)
                 connecta = context.new_page()
                 connecta.goto("http://www16.itrack.com.br/cmatrix/controlemonitoramento")
                 time.sleep(1)
                 connecta.locator("input[name='usuario']").fill("GEAD")
                 connecta.locator("input[name='senha']").fill("33312976")
                 time.sleep(1)
                 connecta.locator("button[name='Submit']").click()
                 connecta.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/a").hover()
                 connecta.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[3]/ul/li[1]/a").hover()
                 connecta.locator("a[href='controlerelatoriodeslocamento']").click()
                 connecta.locator("//*[@id='formfiltro']/fieldset/span[1]/button").click()
                 time.sleep(1)
                 filtro = pyautogui.locateOnScreen('filtro.png', confidence=0.7)
                 time.sleep(1)
                 pyautogui.moveTo(filtro)
                 time.sleep(1)
                 pyautogui.click()
                 pyautogui.write(placaReplaced)
                 time.sleep(1)
                 pyautogui.moveTo(x= filtro.left+50, y= filtro.top+45)
                 time.sleep(1)
                 pyautogui.click()
                 time.sleep(1)
                 dataIniti = connecta.locator("//*[@id='dtI']").click()
                 time.sleep(1)
                 pyautogui.hotkey('ctrl','a')
                 pyautogui.press('del')
                 pyautogui.write(data_replace)
                 time.sleep(1)
                 pyautogui.press('Tab')
                 time.sleep(1)
                 dataFinal = connecta.locator("//*[@id='dtF']").click()
                 pyautogui.hotkey('ctrl','a')
                 pyautogui.press('del')
                 pyautogui.write(data_hora_acres)
                 time.sleep(1)
                 pyautogui.press('Tab')
                 time.sleep(1)
                 connecta.locator("//*[@id='formfiltro']/fieldset/div/button[2]").click()
                 time.sleep(1)
                 book = openpyxl.load_workbook(filename="consultas/Dnit/Consulta dia "+formatData+".xlsx")
                 time.sleep(1)
                 try:
                  page_multas = book['Multas']
                 except:
                  book.create_sheet("Multas")
                  page_multas = book['Multas']
                 try:
                     identificado = pyautogui.locateOnScreen('sem_dados.png', confidence=0.9)
                     if(identificado == None):
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
                       time.sleep(1)
                       page_multas.append([placaReplaced, renavan, localizacao, nomeInfrator])
                       book.save(filename="consultas/Dnit/Consulta dia "+formatData+".xlsx")   
                     else:
                       print('Condutor não identificado\n')
                       condutor = 'Condutor não identificado'
                       time.sleep(1)
                       page_multas.append([placaReplaced, renavan, localizacao, condutor])
                       book.save(filename="consultas/Dnit/Consulta dia "+formatData+".xlsx")
                       print('Dados salvos sem o condutor')
                 except:
                     continue
                 connecta.locator("//*[@id='li-sair']/a").click()
                 connecta.close()
               controller +=1
         except: 
           print('Não Existem dados')  
        else:
          continue 
      except:
        print("Consulta concluída")
        tempoExec = time.time() -t1
        print("\nTempo de execução: {} segundos".format(tempoExec))  
      browser.close()