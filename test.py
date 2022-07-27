from locale import windows_locale
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import asyncio
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup


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
        page.locator('.closer').click()
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
          # newTab.locator('select#cmbTipoDebito').select_option('Multas')
          time.sleep(2)
          # select.locator('//*[@id="cmbTipoDebito"]/option[2]').click()
          # select.select_option('Multas')
          # locator('//*[@id="cmbTipoDebito"]').click()
          print("Existem dados")
          # tabela = newTab.locator('//*[@id="Integral"]/table/tbody')
          # content = tabela.get_attribute('outerHtml')
          # soup = BeautifulSoup(content, 'html.parser')
          # print(tabela)
          # time.sleep(1)
          browser.close()
        except: 
          print("Não existem dados")
          continue 
        browser.close()
      except:
        print("Consulta concluída")
        continue
      browser.close()   
# driver = webdriver.Chrome()
#     driver.get("https://www.detran.mt.gov.br/")
#     time.sleep(2)
#     assert "Início - DETRAN" in driver.title
#     driver.maximize_window
#     openSystem = driver.find_element(By.XPATH, "//*[@id='myPopup']/span").click()
#     time.sleep(2)
#     placa = row["PLACA"]
#     renavan = row["RENAVAN"]
#     driver.find_element(By.ID, "input_placa").send_keys(placa)
#     driver.find_element(By.ID, "input_renavam").send_keys(int(renavan))
#     time.sleep(1)
#     driver.find_element(By.XPATH, "//*[@id='formVeiculo']/div[4]/input[2]").click()
#     time.sleep(5)
#     print(window)
#     # select = Select(driver.find_element(By.ID, "cmbTipoDebito"))
#     # select.select_by_visible_text("Multas").click()
# # # time.sleep(1)
# # driver.switch_to.window(driver.window_handles[1])
# # print("Linha "+str(index)+" Coluna "+str(row)+" \n")
#     driver.quit
# # planilha.to_excel("C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")